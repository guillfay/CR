# gen.py

from mido import Message, MidiFile, MidiTrack
from config import MusicConfig

def parse_solution(solution_text):
    melody = {0: [None] * MusicConfig.TOTAL_STEPS,  # Piano
              1: [None] * MusicConfig.TOTAL_STEPS}  # Violon

    for line in solution_text.split('\n'):
        if line.startswith('v'):
            numbers = [int(x) for x in line.split()[1:] if x != '0']
            positive_vars = [x for x in numbers if x > 0]

            for var in positive_vars:
                var -= 1  # Décalage car les variables SAT commencent à 1
                t = var // (MusicConfig.TOTAL_NOTES * MusicConfig.TOTAL_INSTRUMENTS)
                ni = var % (MusicConfig.TOTAL_NOTES * MusicConfig.TOTAL_INSTRUMENTS)
                n = ni // MusicConfig.TOTAL_INSTRUMENTS
                i = ni % MusicConfig.TOTAL_INSTRUMENTS

                if 0 <= t < MusicConfig.TOTAL_STEPS and 0 <= n < MusicConfig.TOTAL_NOTES:
                    melody[i][t] = MusicConfig.NOTE_MAPPING[i][n]

    return melody

def generate_midi(melody):
    midi = MidiFile(type=1)  # Type 1 : plusieurs pistes indépendantes

    print("🎵 Notes générées :", melody)

    midi = MidiFile()
    instruments = {0: 0, 1: 40}  # Piano, Violon
    tracks = {}

    for i in range(MusicConfig.TOTAL_INSTRUMENTS):
        tracks[i] = MidiTrack()
        midi.tracks.append(tracks[i])
        tracks[i].append(Message('program_change', program=instruments[i], time=0, channel=i))

    for t in range(MusicConfig.TOTAL_STEPS):
        for i in range(MusicConfig.TOTAL_INSTRUMENTS):
            note = melody[i][t]
            if note is not None:
                tracks[i].append(Message('note_on', note=note, velocity=64, time=0, channel=i))
                tracks[i].append(Message('note_off', note=note, velocity=64, time=160, channel=i))
            else:
                # Si la note est None, ajouter un délai pour respecter le rythme
                tracks[i].append(Message('note_off', note=0, velocity=0, time=160, channel=i))  # Silence

    midi.save('output.mid')
    print("✅ Fichier MIDI généré avec plusieurs instruments !")


with open("solution.txt", "r", encoding="utf-8") as f:
    solution_text = f.read()

melody = parse_solution(solution_text)
generate_midi(melody)