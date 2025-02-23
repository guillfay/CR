# config.py

class MusicConfig:
    TOTAL_NOTES = 7  # Do majeur : C, D, E, F, G, A, B
    TOTAL_STEPS = 30  # Nombre de temps

    # Notes MIDI : deux pianos en Do majeur (octave 4)
    NOTE_MAPPING = [
        [60, 62, 64, 65, 67, 69, 71],  # Piano 1 (C4 → B4)
        [48, 50, 52, 53, 55, 57, 59]   # Piano 2 (C3 → B3, une octave plus bas)
    ]

    TOTAL_INSTRUMENTS = len(NOTE_MAPPING)  # Deux pianos

    @classmethod
    def num_vars(cls):
        return cls.TOTAL_NOTES * cls.TOTAL_STEPS * cls.TOTAL_INSTRUMENTS

    @staticmethod
    def var(t, n, i):
        """Retourne l'index SAT pour la note n, instrument i au temps t"""
        return t * (MusicConfig.TOTAL_NOTES * MusicConfig.TOTAL_INSTRUMENTS) + n * MusicConfig.TOTAL_INSTRUMENTS + i + 1