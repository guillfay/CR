from config import MusicConfig
import random
from gurobipy import Model, GRB, quicksum

# Ne pas fixer la graine pour obtenir des résultats différents à chaque exécution
# random.seed(42)

# Création du modèle Gurobi
model = Model("Music_PB")
model.Params.OutputFlag = 1  # Mettre à 0 pour désactiver les logs

# ------------------------------------------------------------------------------------
# Variables de décision binaires : x[t,n,i] = 1 si l'instrument i joue la note n au temps t
x = {}
for t in range(MusicConfig.TOTAL_STEPS):
    for n in range(MusicConfig.TOTAL_NOTES):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            x[t, n, i] = model.addVar(vtype=GRB.BINARY, name=f"x_{t}_{n}_{i}")
model.update()

# ------------------------------------------------------------------------------------
# (0) Contrainte d'affectation unique
# Pour chaque instant t et pour chaque instrument i, une seule note doit être jouée.
for t in range(MusicConfig.TOTAL_STEPS):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        model.addConstr(quicksum(x[t, n, i] for n in range(MusicConfig.TOTAL_NOTES)) == 1,
                        name=f"OneNote_t{t}_i{i}")

# ------------------------------------------------------------------------------------
# (1) Éviter les grands sauts
# Pour chaque instant t, instrument i, et pour tous les couples (n1, n2) tels que |n2-n1| > 4,
# on impose : x[t,n1,i] + x[t+1,n2,i] <= 1 + slack[t,n1,n2,i]
# On introduit ainsi une variable de relaxation (slack) avec une forte pénalité dans l'objectif.
slack = {}
penalty = 1000  # Coefficient de pénalité pour autoriser exceptionnellement un grand saut
for t in range(MusicConfig.TOTAL_STEPS - 1):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        for n1 in range(MusicConfig.TOTAL_NOTES):
            for n2 in range(MusicConfig.TOTAL_NOTES):
                if abs(n2 - n1) > 4:
                    slack[t, n1, n2, i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0,
                                                       name=f"slack_{t}_{n1}_{n2}_{i}")
                    model.addConstr(x[t, n1, i] + x[t+1, n2, i] <= 1 + slack[t, n1, n2, i],
                                    name=f"NoLeap_t{t}_{n1}_{n2}_i{i}")

# ------------------------------------------------------------------------------------
# (2) Harmonisation avec accords et intervalles aléatoires
chords = {
    "I": [0, 2, 4],   # Accord de C majeur (C, E, G)
    "IV": [3, 5, 0],  # Accord de F majeur (F, A, C)
    "V": [4, 6, 1],   # Accord de G majeur (G, B, D)
    "vi": [5, 0, 2],  # Accord de A mineur (A, C, E)
}
# Progression d'accords aléatoire sur TOTAL_STEPS
chord_progression = random.choices(list(chords.values()), k=MusicConfig.TOTAL_STEPS)

# Pour chaque instant t pair (et son voisin t+1), on impose l'harmonisation
for t in range(0, MusicConfig.TOTAL_STEPS - 1, 2):
    chord = chord_progression[t]
    # Pour l'instrument 0 (piano aigu) au temps t, la note doit appartenir à l'accord
    model.addConstr(quicksum(x[t, n, 0] for n in chord) >= 1, name=f"Chord_t{t}_i0")
    model.addConstr(quicksum(x[t+1, n, 1] for n in chord) >= 1, name=f"Chord_t{t}_i1")

# ------------------------------------------------------------------------------------
# (3) Éviter les répétitions trop proches
# Pour chaque instrument i et pour chaque note n, on impose : x[t,n,i] + x[t+2,n,i] <= 1.
X = 2
for t in range(MusicConfig.TOTAL_STEPS - X):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        for n in range(MusicConfig.TOTAL_NOTES):
            model.addConstr(x[t, n, i] + x[t+X, n, i] <= 1,
                            name=f"NoRepeat_t{t}_{n}_i{i}")

# ------------------------------------------------------------------------------------
# (4) Transition harmonieuse : variables pour modéliser la hauteur et la différence absolue
# y[t,i] sera égale à la note MIDI jouée par l'instrument i au temps t.
# d[t,i] modélise |y[t+1,i] - y[t,i]|
y = {}
d = {}
for t in range(MusicConfig.TOTAL_STEPS):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        y[t, i] = model.addVar(vtype=GRB.INTEGER, name=f"y_{t}_{i}")
for t in range(MusicConfig.TOTAL_STEPS - 1):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        d[t, i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"d_{t}_{i}")
model.update()

# Lien entre y[t,i] et x[t,n,i] : y[t,i] = Σ (NOTE_MAPPING[i][n] * x[t,n,i])
for t in range(MusicConfig.TOTAL_STEPS):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        model.addConstr(
            y[t, i] == quicksum(MusicConfig.NOTE_MAPPING[i][n] * x[t, n, i]
                                for n in range(MusicConfig.TOTAL_NOTES)),
            name=f"Link_y_t{t}_i{i}"
        )

# Modélisation de la valeur absolue : d[t,i] ≥ y[t+1,i] - y[t,i] et d[t,i] ≥ y[t,i] - y[t+1,i]
for t in range(MusicConfig.TOTAL_STEPS - 1):
    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        model.addConstr(y[t+1, i] - y[t, i] <= d[t, i], name=f"Abs1_t{t}_i{i}")
        model.addConstr(y[t, i] - y[t+1, i] <= d[t, i], name=f"Abs2_t{t}_i{i}")

# ------------------------------------------------------------------------------------
# Objectif : minimiser la somme des écarts entre notes consécutives (pour des transitions douces)
# plus une pénalité sur les slacks pour éviter les grands sauts non souhaités.
obj = quicksum(d[t, i] for t in range(MusicConfig.TOTAL_STEPS - 1)
               for i in range(MusicConfig.TOTAL_INSTRUMENTS))
obj += penalty * quicksum(slack[t, n1, n2, i]
                          for t in range(MusicConfig.TOTAL_STEPS - 1)
                          for i in range(MusicConfig.TOTAL_INSTRUMENTS)
                          for n1 in range(MusicConfig.TOTAL_NOTES)
                          for n2 in range(MusicConfig.TOTAL_NOTES) if abs(n2 - n1) > 4)
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
