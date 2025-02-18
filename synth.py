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
   
    # 2️⃣ Harmonisation avec des accords filtrés et semi-aléatoires
    chords = {
        "I": [0, 2, 4],  # C majeur (C-E-G)
        "IV": [3, 5, 0],  # F majeur (F-A-C)
        "V": [4, 6, 1],   # G majeur (G-B-D)
        "vi": [5, 0, 2],  # A mineur (A-C-E)
    }

    # Générer une progression d'accords aléatoire avec les accords sélectionnés
    chord_progression = random.choices(list(chords.values()), k=MusicConfig.TOTAL_STEPS)

    # Générer x intervalles aléatoires où les instruments jouent ensemble
    x = random.randint(0, MusicConfig.TOTAL_STEPS // 10)  # Nombre d'intervalles
    together_intervals = []
    for _ in range(x):
        start = random.randint(0, MusicConfig.TOTAL_STEPS // 2)
        end = start + random.randint(3, MusicConfig.TOTAL_STEPS // 3)
        together_intervals.append((start, end))

    for t in range(0, MusicConfig.TOTAL_STEPS - 1, 2):  # Tous les 2 temps
        chord = chord_progression[t]
        
        if any(start <= t <= end for start, end in together_intervals):
            # Pendant ces intervalles, ils jouent ensemble
            clauses.append([MusicConfig.var(t, n, 0) for n in chord])  # Piano aigu
            clauses.append([MusicConfig.var(t, n, 1) for n in chord])  # Piano grave simultanément
        else:
            # En dehors de ces intervalles, le piano grave joue en décalé
            clauses.append([MusicConfig.var(t, n, 0) for n in chord])  # Piano aigu
            clauses.append([MusicConfig.var(t+1, n, 1) for n in chord])  # Piano grave en retard

    # 4️⃣ Éviter les répétitions trop proches (chaque instrument)
    X = 2  # Nombre minimal de pas avant répétition
    for t in range(MusicConfig.TOTAL_STEPS - X):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            for n in range(MusicConfig.TOTAL_NOTES):
                clauses.append([-MusicConfig.var(t, n, i), -MusicConfig.var(t + X, n, i)])

    # Écriture du fichier CNF
    with open("music.cnf", "w") as f:
        f.write(f"p cnf {MusicConfig.num_vars()} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

    print("✅ Fichier CNF généré avec tempo progressif et final structuré !")

generate_cnf()