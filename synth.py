# synth.py

import itertools
from config import MusicConfig
import random

def random_cnf(clauses, seed=None):
    """Force quelques notes spécifiques basées sur la seed pour chaque instrument."""
    if seed is not None:
        random.seed(seed)
    
    for _ in range(MusicConfig.TOTAL_STEPS // 6):
        t = random.randint(1, MusicConfig.TOTAL_STEPS - 2)
        n = random.randint(0, MusicConfig.TOTAL_NOTES - 1)
        i = random.randint(0, MusicConfig.TOTAL_INSTRUMENTS - 1)  # Choix d'un instrument aléatoire
        clauses.append([MusicConfig.var(t, n, i)])
    
    return clauses
# synth.py

def generate_cnf(seed=None):
    if seed is not None:
        random.seed(seed)

    clauses = []
    clauses = random_cnf(clauses, seed)


    # 1️⃣ Chaque instrument joue une note à chaque temps
    for t in range(MusicConfig.TOTAL_STEPS):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            if i == 1:  # Violon : rythme cyclique (1 temps sur 3)
                if t % 3 != 0:  # Le violon ne joue que tous les 3 temps
                    for n in range(MusicConfig.TOTAL_NOTES):
                        clauses.append([-MusicConfig.var(t, n, i)])  # Forcer à ne pas jouer
                    continue
            clauses.append([MusicConfig.var(t, n, i) for n in range(MusicConfig.TOTAL_NOTES)])  # Au moins une note
            for n1, n2 in itertools.combinations(range(MusicConfig.TOTAL_NOTES), 2):
                clauses.append([-MusicConfig.var(t, n1, i), -MusicConfig.var(t, n2, i)])  # Au plus une note

    # 2️⃣ Éviter les grands sauts (chaque instrument)
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            for n1 in range(MusicConfig.TOTAL_NOTES):
                for n2 in range(MusicConfig.TOTAL_NOTES):
                    if abs(n2 - n1) > 4:  # Éviter sauts > quinte
                        clauses.append([-MusicConfig.var(t, n1, i), -MusicConfig.var(t + 1, n2, i)])

    # 3️⃣ Éviter 2 notes identiques consécutives (chaque instrument)
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            for n in range(MusicConfig.TOTAL_NOTES):
                clauses.append([-MusicConfig.var(t, n, i), -MusicConfig.var(t + 1, n, i)])

    # # 6️⃣ Contrainte d'accords simples (tierces, quartes, quintes, sixtes)
    # for t in range(MusicConfig.TOTAL_STEPS):
    #     for n_piano in range(MusicConfig.TOTAL_NOTES):
    #         for n_violon in range(MusicConfig.TOTAL_NOTES):
    #             interval = abs(MusicConfig.NOTE_MAPPING[0][n_piano] - MusicConfig.NOTE_MAPPING[1][n_violon])
    #             if interval not in [3, 4, 5, 7, 8, 9]:  # Tierces, quartes, quintes, sixtes
    #                 clauses.append([-MusicConfig.var(t, n_piano, 0), -MusicConfig.var(t, n_violon, 1)])


    # Écriture du fichier CNF
    with open("music.cnf", "w") as f:
        f.write(f"p cnf {MusicConfig.num_vars()} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

    print("✅ Fichier CNF généré avec plusieurs instruments et contraintes supplémentaires !")

generate_cnf()