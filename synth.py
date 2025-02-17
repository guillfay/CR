# synth.py

import itertools
from config import MusicConfig
import random

def random_cnf(clauses, seed=None):
    """Force une sélection plus variée de notes pour éviter la duplication de mélodie."""
    if seed is not None:
        random.seed(seed)

    for _ in range(MusicConfig.TOTAL_STEPS // 4):  # Réduit le nombre de contraintes forcées
        t = random.randint(0, MusicConfig.TOTAL_STEPS - 1)
        n1 = random.randint(0, MusicConfig.TOTAL_NOTES - 1)
        n2 = random.randint(0, MusicConfig.TOTAL_NOTES - 1)
        
        clauses.append([MusicConfig.var(t, n1, 0)])  # Force une note pour le piano 1
        clauses.append([MusicConfig.var(t, n2, 1)])  # Force une autre note pour le piano 2
    return clauses


def generate_cnf(seed=None):
    if seed is not None:
        random.seed(seed)

    clauses = []
    clauses = random_cnf(clauses, seed)

    # 2️⃣ Éviter les grands sauts (chaque instrument)
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            for n1 in range(MusicConfig.TOTAL_NOTES):
                for n2 in range(MusicConfig.TOTAL_NOTES):
                    if abs(n2 - n1) > 4:  # Éviter sauts > quinte (5 demi-tons)
                        clauses.append([-MusicConfig.var(t, n1, i), -MusicConfig.var(t + 1, n2, i)])
    
    # 3️⃣ Harmonisation avec des accords (I, IV, V en Do majeur)
    chords = {
        "I": [0, 2, 4],  # C majeur (C-E-G)
        "IV": [3, 5, 0],  # F majeur (F-A-C)
        "V": [4, 6, 1]   # G majeur (G-B-D)
    }

    for t in range(MusicConfig.TOTAL_STEPS):
        chord = chords["I"] if t % 4 == 0 else chords["IV"] if t % 4 == 1 else chords["V"] if t % 4 == 2 else chords["I"]
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            clauses.append([MusicConfig.var(t, n, i) for n in chord])

    # 4️⃣ Éviter 2 notes identiques consécutives (chaque instrument)
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            for n in range(MusicConfig.TOTAL_NOTES):
                clauses.append([-MusicConfig.var(t, n, i), -MusicConfig.var(t + 1, n, i)])

    # Écriture du fichier CNF
    with open("music.cnf", "w") as f:
        f.write(f"p cnf {MusicConfig.num_vars()} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

    print("✅ Fichier CNF généré avec harmonisation en Do majeur !")

generate_cnf()