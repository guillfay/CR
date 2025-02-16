# config.py
# config.py

# config.py

class MusicConfig:
    TOTAL_NOTES = 24  # 2 octaves
    TOTAL_STEPS = 20  # Nombre de temps
    TOTAL_INSTRUMENTS = 2  # Piano, Violon

    # Notes MIDI : piano / violon (octave 4), cor (octave 3)
    NOTE_MAPPING = [
        # Piano 🎹 (octave 4 et 5)
        [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100],
        
        # Violon 🎻 (octave 2 et 3, plus grave et moins haut)
        [24, 26, 28, 29, 31, 33, 35, 36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64]
    ]
    @classmethod
    def num_vars(cls):
        return cls.TOTAL_NOTES * cls.TOTAL_STEPS * cls.TOTAL_INSTRUMENTS

    @staticmethod
    def var(t, n, i):
        """Retourne l'index SAT pour la note n, instrument i au temps t"""
        return t * (MusicConfig.TOTAL_NOTES * MusicConfig.TOTAL_INSTRUMENTS) + n * MusicConfig.TOTAL_INSTRUMENTS + i + 1
