from mido import Message, MidiFile, MidiTrack

# 🔹 Paramètres
num_notes = 14  # Do majeur : C, D, E, F, G, A, B
num_steps = 16  # Nombre de temps
note_mapping = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]  # MIDI notes (C4, D4, E4, F4, G4, A4, B4)

# 🔹 Charger la solution SAT
with open("solution.txt", "r") as f:
    lines = f.readlines()

# 🔹 Extraire les variables positives de la solution SAT
solution_vars = []
for line in lines:
    if line.startswith("v "):  # Ligne contenant les variables
        solution_vars.extend(map(int, line.strip().split()[1:]))  # Extraire les valeurs

# Filtrer uniquement les variables positives
active_vars = [var for var in solution_vars if var > 0]

# 🔹 Convertir les variables SAT en notes MIDI
melody = [None] * num_steps  # Initialiser la mélodie vide

for var in active_vars:
    t = (var - 1) // num_notes  # Temps associé à cette variable
    n = (var - 1) % num_notes  # Index de la note dans la gamme

    if 0 <= t < num_steps and 0 <= n < num_notes:
        melody[t] = note_mapping[n]  # Assigner la note correcte

# 🔹 Génération du fichier MIDI
midi = MidiFile()
track = MidiTrack()
midi.tracks.append(track)

for i, note in enumerate(melody):
    if note is not None:
        track.append(Message('note_on', note=note, velocity=64, time=80))
        track.append(Message('note_off', note=note, velocity=64, time=160))

# 🔹 Sauvegarde du fichier MIDI
midi.save('output.mid')
print("✅ Fichier MIDI généré : output.mid")
