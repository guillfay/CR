import itertools
from config import MusicConfig

def generate_cnf():
    clauses = []

    # 1️⃣ Base constraints: Une seule note active par temps
    for t in range(MusicConfig.TOTAL_STEPS):
        clauses.append([MusicConfig.var(t, n) for n in range(MusicConfig.TOTAL_NOTES)])  # Au moins une note
        for n1, n2 in itertools.combinations(range(MusicConfig.TOTAL_NOTES), 2):  # Au plus une note
            clauses.append([-MusicConfig.var(t, n1), -MusicConfig.var(t, n2)])

    # 2️⃣ Contrainte de début et fin sur la tonique (Do)
    clauses.append([MusicConfig.var(0, 0)])
    clauses.append([MusicConfig.var(MusicConfig.TOTAL_STEPS - 1, 0)])

    # 3️⃣ Éviter les grands sauts (plus de tierce)
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for n1 in range(MusicConfig.TOTAL_NOTES):
            for n2 in range(MusicConfig.TOTAL_NOTES):
                if abs(n2 - n1) > 2:
                    clauses.append([-MusicConfig.var(t, n1), -MusicConfig.var(t + 1, n2)])

    # 4️⃣ Empêcher la répétition de 3 notes identiques consécutives
    for t in range(MusicConfig.TOTAL_STEPS - 2):
        for n in range(MusicConfig.TOTAL_NOTES):
            clauses.append([-MusicConfig.var(t, n), -MusicConfig.var(t + 1, n), -MusicConfig.var(t + 2, n)])

    # 5️⃣ Ajout de contraintes spécifiques à chaque style
    if MusicConfig.STYLE == "jazz":
        add_jazz_constraints(clauses)
    elif MusicConfig.STYLE == "classical":
        add_classical_constraints(clauses)
    elif MusicConfig.STYLE == "blues":
        add_blues_constraints(clauses)
    elif MusicConfig.STYLE == "pop":
        add_pop_constraints(clauses)
    elif MusicConfig.STYLE == "electro":
        add_electro_constraints(clauses)

    # Écriture du fichier CNF
    with open("music.cnf", "w") as f:
        f.write(f"p cnf {MusicConfig.num_vars()} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

    print(f"✅ Fichier CNF généré pour le style {MusicConfig.STYLE.upper()}")

def add_jazz_constraints(clauses):
    """Ajoute des contraintes pour générer une mélodie de style jazz"""
    print("🎷 Ajout des contraintes Jazz...")
    # Favoriser des septièmes et neuvièmes
    for t in range(MusicConfig.TOTAL_STEPS):
        seventh_ninth = [MusicConfig.var(t, n) for n in [4, 6]]  # Sol (G), Si (B)
        clauses.append(seventh_ninth)  # Au moins une note jazz

def add_classical_constraints(clauses):
    """Ajoute des contraintes pour générer une mélodie classique"""
    print("🎻 Ajout des contraintes Classique...")
    # Interdire les sauts dissonants (triton, seconde mineure)
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for n1, n2 in itertools.combinations(range(MusicConfig.TOTAL_NOTES), 2):
            if abs(n1 - n2) == 6 or abs(n1 - n2) == 1:  # Triton et seconde mineure
                clauses.append([-MusicConfig.var(t, n1), -MusicConfig.var(t + 1, n2)])

def add_blues_constraints(clauses):
    """Ajoute des contraintes pour générer une mélodie blues"""
    print("🎸 Ajout des contraintes Blues...")
    # Favoriser la blue note (quinte diminuée)
    for t in range(MusicConfig.TOTAL_STEPS):
        clauses.append([MusicConfig.var(t, 3)])  # Fa# en gamme de Do

def add_pop_constraints(clauses):
    """Ajoute des contraintes pour générer une mélodie pop"""
    print("🎶 Ajout des contraintes Pop...")
    # Éviter des écarts trop complexes, favoriser les secondes et tierces
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for n1, n2 in itertools.combinations(range(MusicConfig.TOTAL_NOTES), 2):
            if abs(n1 - n2) > 3:  # Interdire les sauts trop grands
                clauses.append([-MusicConfig.var(t, n1), -MusicConfig.var(t + 1, n2)])

def add_electro_constraints(clauses):
    """Ajoute des contraintes pour générer une mélodie électro"""
    print("🎵 Ajout des contraintes Électro...")
    # Rythme régulier avec des répétitions de motifs
    for t in range(MusicConfig.TOTAL_STEPS - 2):
        for n in range(MusicConfig.TOTAL_NOTES):
            if t % 2 == 0:  # Toutes les 2 mesures, imposer une répétition
                clauses.append([MusicConfig.var(t, n), MusicConfig.var(t + 2, n)])