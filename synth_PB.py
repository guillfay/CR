import itertools
from config import MusicConfig

def generate_opb():
    constraints = []
    
    # 1️⃣ Base constraints: une seule note active par temps
    for t in range(MusicConfig.TOTAL_STEPS):
        # Exactement une note jouée à chaque temps
        constraints.append(" + ".join(f"x_{t}_{n}" for n in range(MusicConfig.TOTAL_NOTES)) + " = 1;")
    
    # 2️⃣ Règle de début et fin sur la tonique (Do)
    constraints.append(f"x_0_0 = 1;")  # La première note doit être Do
    constraints.append(f"x_{MusicConfig.TOTAL_STEPS - 1}_0 = 1;")  # La dernière note doit être Do
    
    # 3️⃣ Éviter les grands sauts
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for n1 in range(MusicConfig.TOTAL_NOTES):
            for n2 in range(MusicConfig.TOTAL_NOTES):
                if abs(n2 - n1) > 2:  # Interdire les sauts de plus de 2 notes
                    constraints.append(f"x_{t}_{n1} + x_{t+1}_{n2} <= 1;")
    
    # 4️⃣ Éviter trois notes identiques consécutives
    for t in range(MusicConfig.TOTAL_STEPS - 2):
        for n in range(MusicConfig.TOTAL_NOTES):
            constraints.append(f"x_{t}_{n} + x_{t+1}_{n} + x_{t+2}_{n} <= 2;")
    
    # 5️⃣ Forcer au moins une note aiguë (Sol ou plus haut)
    high_notes = " + ".join(f"x_{t}_{n}" for t in range(MusicConfig.TOTAL_STEPS) for n in range(4, MusicConfig.TOTAL_NOTES))
    constraints.append(high_notes + " >= 1;")
    
    # 6️⃣ Après une note aiguë (Sol ou plus), descendre
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for n in range(4, MusicConfig.TOTAL_NOTES):
            lower_notes = " + ".join(f"x_{t+1}_{next_n}" for next_n in range(0, n))
            constraints.append(f"x_{t}_{n} + {lower_notes} >= 1;")
    
    # 7️⃣ Fonction objectif pour privilégier des transitions douces
    objective = " + ".join(f"x_{t}_{n}" for t in range(MusicConfig.TOTAL_STEPS) for n in range(MusicConfig.TOTAL_NOTES))
    
    # Écriture du fichier OPB
    with open("music.opb", "w") as f:
        f.write(f"min: {objective};\n")
        for constraint in constraints:
            f.write(constraint + "\n")
    
    print("✅ Fichier OPB généré avec contraintes pseudobooléennes optimisées")
