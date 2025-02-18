# synth_pb.py (Correction de la génération OPB)

from config import MusicConfig

def generate_opb():
    clauses = []
    
    # Contraintes pour garantir qu'au moins une note est jouée à chaque instant
    for t in range(MusicConfig.TOTAL_STEPS):
        clause = " + ".join([f"1 x{t}_{n}_{i}" for n in range(MusicConfig.TOTAL_NOTES) for i in range(MusicConfig.TOTAL_INSTRUMENTS)])
        clauses.append(f"{clause} >= 1 ;")
    
    # Éviter les grands sauts
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            for n1 in range(MusicConfig.TOTAL_NOTES):
                for n2 in range(MusicConfig.TOTAL_NOTES):
                    if abs(n2 - n1) > 4:
                        clauses.append(f"1 x{t}_{n1}_{i} + 1 x{t+1}_{n2}_{i} <= 1 ;")
    
    # Harmonisation avec des accords (I, IV, V en Do majeur)
    chords = {
        "I": [0, 2, 4],
        "IV": [3, 5, 0],
        "V": [4, 6, 1]
    }
    
    for t in range(MusicConfig.TOTAL_STEPS):
        chord = chords["I"] if t % 4 == 0 else chords["IV"] if t % 4 == 1 else chords["V"] if t % 4 == 2 else chords["I"]
        clause = " + ".join([f"1 x{t}_{n}_{i}" for i in range(MusicConfig.TOTAL_INSTRUMENTS) for n in chord])
        clauses.append(f"{clause} >= 1 ;")
    
    # Éviter la répétition excessive d'une note
    for t in range(MusicConfig.TOTAL_STEPS - 1):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            for n in range(MusicConfig.TOTAL_NOTES):
                clauses.append(f"1 x{t}_{n}_{i} + 1 x{t+1}_{n}_{i} <= 1 ;")
    
    # Écriture du fichier OPB
    with open("music.opb", "w") as f:
        f.write(f"* #variables = {MusicConfig.num_vars()} #constraints = {len(clauses)}\n")
        for clause in clauses:
            f.write(clause + "\n")
    
    print("✅ Fichier OPB généré avec succès !")

generate_opb()
