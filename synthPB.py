from config import MusicConfig
import random
from gurobipy import Model, GRB, quicksum

# On ne fixe pas la graine pour obtenir des résultats différents à chaque exécution
# random.seed(42)

# Création du modèle Gurobi
model = Model("Music_PB")
model.Params.OutputFlag = 1  # Mettre à 0 pour désactiver les logs

# ------------------------------------------------------------------------------------
# Variables de décision binaires : 
# x[t,n,i] = 1 si l'instrument i joue la note n au temps t
x = {}
for t in range(MusicConfig.TOTAL_STEPS):
    for n in range(MusicConfig.TOTAL_NOTES):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            x[t, n, i] = model.addVar(vtype=GRB.BINARY, name=f"x_{t}_{n}_{i}")
model.update()

# ------------------------------------------------------------------------------------
# (0) Contrainte d'affectation unique :
# Pour chaque instant t et pour chaque instrument i, une seule note doit être jouée.
for t in range(MusicConfig.TOTAL_STEPS):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        model.addConstr(
            quicksum(x[t, n, i] for n in range(MusicConfig.TOTAL_NOTES)) <= 1,
            name=f"OneNote_t{t}_i{i}"
        )

# ------------------------------------------------------------------------------------
# (1) Éviter les grands sauts :
# Pour chaque instant t, instrument i et pour tous les couples (n1, n2) tels que |n2 - n1| > 4,
# on impose x[t,n1,i] + x[t+1,n2,i] <= 1.
for t in range(MusicConfig.TOTAL_STEPS - 1):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        for n1 in range(MusicConfig.TOTAL_NOTES):
            for n2 in range(MusicConfig.TOTAL_NOTES):
                if abs(n2 - n1) > 4:
                    model.addConstr(
                        x[t, n1, i] + x[t+1, n2, i] <= 1,
                        name=f"NoLeap_t{t}_{n1}_{n2}_i{i}"
                    )

# ------------------------------------------------------------------------------------
# (2) Harmonisation avec accords et intervalles aléatoires :
chords = {
    "I": [0, 2, 4],   # Accord de C majeur (C, E, G)
    "IV": [3, 5, 0],  # Accord de F majeur (F, A, C)
    "V": [4, 6, 1],   # Accord de G majeur (G, B, D)
    "vi": [5, 0, 2],  # Accord de A mineur (A, C, E)
}
# Progression d'accords aléatoire sur TOTAL_STEPS
chord_progression = random.choices(list(chords.values()), k=MusicConfig.TOTAL_STEPS)

# Intervalles aléatoires pendant lesquels les instruments jouent ensemble
n_interv = random.randint(0, MusicConfig.TOTAL_STEPS // 10)
together_intervals = []
for _ in range(n_interv):
    start = random.randint(0, MusicConfig.TOTAL_STEPS // 2)
    end = start + random.randint(3, max(3, MusicConfig.TOTAL_STEPS // 3))
    together_intervals.append((start, end))

# Pour chaque instant t pair (et son voisin t+1), on impose l'harmonisation
for t in range(0, MusicConfig.TOTAL_STEPS - 1, 2):
    chord = chord_progression[t]
    # Pour l'instrument 0 (piano aigu) au temps t, la note doit appartenir à l'accord
    model.addConstr(
        quicksum(x[t, n, 0] for n in chord) >= 1,
        name=f"Chord_t{t}_i0"
    )
    # Pour l'instrument 1 (piano grave)
    in_together = any(start <= t <= end for (start, end) in together_intervals)
    if in_together:
        model.addConstr(
            quicksum(x[t, n, 1] for n in chord) >= 1,
            name=f"Chord_t{t}_i1"
        )
    else:
        if t + 1 < MusicConfig.TOTAL_STEPS:
            model.addConstr(
                quicksum(x[t+1, n, 1] for n in chord) >= 1,
                name=f"Chord_t{t+1}_i1"
            )

# ------------------------------------------------------------------------------------
# (3) Éviter les répétitions trop proches :
# Pour chaque instrument i et pour chaque note n, on impose : x[t,n,i] + x[t+2,n,i] <= 1.
X = 2
for t in range(MusicConfig.TOTAL_STEPS - X):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        for n in range(MusicConfig.TOTAL_NOTES):
            model.addConstr(
                x[t, n, i] + x[t+X, n, i] <= 1,
                name=f"NoRepeat_t{t}_{n}_i{i}"
            )

# ------------------------------------------------------------------------------------
# (4) Transition harmonieuse (modélisation pseudo-booléenne) :
# On souhaite pénaliser les grandes différences entre notes successives.
# Au lieu d'utiliser des variables continues pour la différence, nous introduisons
# une variable binaire z[t, n1, n2, i] qui vaut 1 si et seulement si l'instrument i passe de la note n1 à t à la note n2 à t+1.
z = {}
for t in range(MusicConfig.TOTAL_STEPS - 1):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        for n1 in range(MusicConfig.TOTAL_NOTES):
            for n2 in range(MusicConfig.TOTAL_NOTES):
                z[t, n1, n2, i] = model.addVar(vtype=GRB.BINARY, name=f"z_{t}_{n1}_{n2}_{i}")
model.update()

# Contraintes liant z et x :
for t in range(MusicConfig.TOTAL_STEPS - 1):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        for n1 in range(MusicConfig.TOTAL_NOTES):
            for n2 in range(MusicConfig.TOTAL_NOTES):
                model.addConstr(
                    z[t, n1, n2, i] <= x[t, n1, i],
                    name=f"Link1_z_{t}_{n1}_{n2}_{i}"
                )
                model.addConstr(
                    z[t, n1, n2, i] <= x[t+1, n2, i],
                    name=f"Link2_z_{t}_{n1}_{n2}_{i}"
                )
                model.addConstr(
                    z[t, n1, n2, i] >= x[t, n1, i] + x[t+1, n2, i] - 1,
                    name=f"Link3_z_{t}_{n1}_{n2}_{i}"
                )

# ------------------------------------------------------------------------------------
# Objectif : minimiser la somme des écarts entre notes successives
# La pénalité d'une transition passant de la note n1 à la note n2 pour l'instrument i est :
# |NOTE_MAPPING[i][n2] - NOTE_MAPPING[i][n1]|
obj = quicksum(
    abs(MusicConfig.NOTE_MAPPING[i][n2] - MusicConfig.NOTE_MAPPING[i][n1]) * z[t, n1, n2, i]
    for t in range(MusicConfig.TOTAL_STEPS - 1)
    for i in range(MusicConfig.TOTAL_INSTRUMENTS)
    for n1 in range(MusicConfig.TOTAL_NOTES)
    for n2 in range(MusicConfig.TOTAL_NOTES)
)
model.setObjective(obj, GRB.MINIMIZE)

# ------------------------------------------------------------------------------------
# Optimisation du modèle
model.optimize()

# ------------------------------------------------------------------------------------
# Écriture de la solution dans "solution.txt" au même format que pour le SAT
if model.status == GRB.OPTIMAL or model.solCount > 0:
    with open("solution.txt", "w", encoding="utf-8") as f:
        solution_line = "v"
        for t in range(MusicConfig.TOTAL_STEPS):
            for n in range(MusicConfig.TOTAL_NOTES):
                for i in range(MusicConfig.TOTAL_INSTRUMENTS):
                    if x[t, n, i].X > 0.5:
                        solution_line += " " + str(MusicConfig.var(t, n, i))
        solution_line += " 0\n"
        f.write(solution_line)
    print("✅ Solution générée et écrite dans solution.txt")
else:
    print("❌ Aucune solution trouvée.")
