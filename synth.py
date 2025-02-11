# import itertools

# # Paramètres
# num_notes = 7  # Do majeur : C, D, E, F, G, A, B
# num_steps = 8  # Nombre de temps

# # Mapping des variables
# def var(t, n):
#     """ Retourne l'index SAT pour la note n au temps t """
#     return t * num_notes + n + 1

# # Génération des contraintes
# clauses = []

# # 1. Une seule note par temps
# for t in range(num_steps):
#     clauses.append([var(t, n) for n in range(num_notes)])  # Au moins une note
#     for n1, n2 in itertools.combinations(range(num_notes), 2):
#         clauses.append([-var(t, n1), -var(t, n2)])  # Pas deux notes en même temps

# # 2. Transitions douces (évite les sauts > 2)
# for t in range(num_steps - 1):
#     for n1 in range(num_notes):
#         for n2 in range(num_notes):
#             if abs(n1 - n2) > 2:  # Saut trop grand interdit
#                 clauses.append([-var(t, n1), -var(t + 1, n2)])

# # Écriture dans un fichier CNF
# with open("music.cnf", "w") as f:
#     f.write(f"p cnf {num_steps * num_notes} {len(clauses)}\n")
#     for clause in clauses:
#         f.write(" ".join(map(str, clause)) + " 0\n")

# print("Fichier music.cnf généré.")


import random

# 🔹 Paramètres
num_notes = 14  # Do majeur (C, D, E, F, G, A, B)
num_steps = 16  # Nombre de temps
num_vars = num_notes * num_steps
note_range = list(range(1, num_vars + 1))  # Variables SAT

# 🔹 Générer les contraintes
clauses = []

# 1️⃣ Chaque temps doit avoir au moins une note jouée
for t in range(num_steps):
    clause = [t * num_notes + n for n in range(1, num_notes + 1)]
    clauses.append(clause)

# 2️⃣ Chaque temps a au plus une note jouée
for t in range(num_steps):
    for n1 in range(1, num_notes + 1):
        for n2 in range(n1 + 1, num_notes + 1):
            clauses.append([-(t * num_notes + n1), -(t * num_notes + n2)])

# 3️⃣ Éviter les grands sauts mélodiques (max ±4 demi-tons)
for t in range(num_steps - 1):
    for n in range(1, num_notes + 1):
        allowed_next_notes = [m for m in range(max(1, n - 4), min(num_notes + 1, n + 5))]
        disallowed_next_notes = [m for m in range(1, num_notes + 1) if m not in allowed_next_notes]

        for m in disallowed_next_notes:
            clauses.append([-(t * num_notes + n), -( (t + 1) * num_notes + m)])

# 4️⃣ Réduire les silences (max 5% des temps)
for t in range(num_steps):
    if random.random() < 0.05:  # Seulement 5% de chance d'être un silence
        for n in range(1, num_notes + 1):
            clauses.append([-(t * num_notes + n)])

# 5️⃣ Direction mélodique (éviter les trop grands écarts)
for t in range(num_steps - 2):
    for n in range(1, num_notes + 1):
        for m in range(1, num_notes + 1):
            if abs(n - m) > 3:  # Si trop éloigné, on pénalise
                clauses.append([-(t * num_notes + n), -(t + 2) * num_notes + m])

# 🔹 Sauvegarde du fichier CNF
with open("music.cnf", "w") as f:
    f.write(f"p cnf {num_vars} {len(clauses)}\n")
    for clause in clauses:
        f.write(" ".join(map(str, clause)) + " 0\n")

print("✅ Fichier CNF généré : music.cnf")

