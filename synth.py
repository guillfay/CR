import itertools
from config import MusicConfig

def generate_cnf():
    clauses = []
    
    # 1️⃣ Base constraints: une note exactement par temps
    for t in range(MusicConfig.TOTAL_STEPS):
        # Au moins une note
        clauses.append([MusicConfig.var(t, n) for n in range(MusicConfig.TOTAL_NOTES)])
        # Au plus une note
        for n1, n2 in itertools.combinations(range(MusicConfig.TOTAL_NOTES), 2):
            clauses.append([-MusicConfig.var(t, n1), -MusicConfig.var(t, n2)])
    
    # 2️⃣ Règle de début et fin sur la tonique (Do)
    # Première note doit être Do (note 0)
    clauses.append([MusicConfig.var(0, 0)])
    # Dernière note doit être Do
    clauses.append([MusicConfig.var(MusicConfig.TOTAL_STEPS - 1, 0)])
    
    # 3️⃣ Éviter les grands sauts
    # Pour chaque temps t (sauf le dernier)
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        # Pour chaque note courante
        for n1 in range(MusicConfig.TOTAL_NOTES):
            # Pour chaque note suivante possible
            for n2 in range(MusicConfig.TOTAL_NOTES):
                # Si le saut est plus grand que 2 notes (tierce), on l'interdit
                if abs(n2 - n1) > 2:
                    clauses.append([-MusicConfig.var(t, n1), -MusicConfig.var(t + 1, n2)])
    
    # 4️⃣ Éviter trois notes identiques consécutives
    for t in range(MusicConfig.TOTAL_STEPS - 2):
        for n in range(MusicConfig.TOTAL_NOTES):
            clauses.append([-MusicConfig.var(t, n), -MusicConfig.var(t + 1, n), -MusicConfig.var(t + 2, n)])
    
    # 5️⃣ Forcer au moins une note aiguë (Sol ou plus haut) dans la mélodie
    high_notes = []
    for t in range(MusicConfig.TOTAL_STEPS):
        for n in range(4, MusicConfig.TOTAL_NOTES):  # Sol et au-dessus
            high_notes.append(MusicConfig.var(t, n))
    clauses.append(high_notes)
    
    # 6️⃣ Après une note aiguë (Sol ou plus), descendre
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for n in range(4, MusicConfig.TOTAL_NOTES):  # Pour Sol et au-dessus
            lower_notes = []
            for next_n in range(0, n):  # Toutes les notes plus basses
                lower_notes.append(MusicConfig.var(t + 1, next_n))
            clauses.append([-MusicConfig.var(t, n)] + lower_notes)
    
    # Écriture du fichier CNF
    with open("music.cnf", "w") as f:
        f.write(f"p cnf {MusicConfig.num_vars()} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    print("✅ Fichier CNF généré avec règles musicales avancées")



generate_cnf()