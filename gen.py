# gen.py
from mido import Message, MidiFile, MidiTrack
from config import MusicConfig

def parse_solution(solution_text):
    melody = [None] * MusicConfig.TOTAL_STEPS
    
    # Parcourir les lignes de la solution
    for line in solution_text.split('\n'):
        if line.startswith('v'):
            # Extraire tous les nombres de la ligne
            numbers = [int(x) for x in line.split()[1:] if x != '0']  # Ignore le dernier 0
            positive_vars = [x for x in numbers if x > 0]
            
            # Pour chaque variable positive, calculer la note correspondante
            for var in positive_vars:
                var = var - 1  # Décalage car les variables SAT commencent à 1
                t = var // MusicConfig.TOTAL_NOTES
                n = var % MusicConfig.TOTAL_NOTES
                
                if 0 <= t < MusicConfig.TOTAL_STEPS and 0 <= n < MusicConfig.TOTAL_NOTES:
                    melody[t] = MusicConfig.NOTE_MAPPING[n]
    
    return melody

def generate_midi(melody):
    print("🎵 Notes générées par le SAT Solver :", melody)
    
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    for note in melody:
        if note is not None:
            track.append(Message('note_on', note=note, velocity=64, time=80))
            track.append(Message('note_off', note=note, velocity=64, time=160))
    
    midi.save('output.mid')
    print("✅ Fichier MIDI généré : output.mid")