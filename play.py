import pygame.midi
import mido

def play_midi(file):
    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)
    
    mid = mido.MidiFile(file)
    
    try:
        for msg in mid.play():
            if msg.type == 'note_on':
                player.note_on(msg.note, msg.velocity)
            elif msg.type == 'note_off':
                player.note_off(msg.note, msg.velocity)
    finally:
        player.close()
        pygame.midi.quit()