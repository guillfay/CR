# config file

class MusicConfig:
    TOTAL_NOTES = 7  # Notes possibles : Do, Ré, Mi, Fa, Sol, La, Si
    TOTAL_STEPS = 8  # Nombre de temps
    NOTE_MAPPING = [60, 62, 64, 65, 67, 69, 71]  # MIDI notes (C4 to B4)
    
    @classmethod
    def num_vars(cls):
        return cls.TOTAL_NOTES * cls.TOTAL_STEPS

    @staticmethod
    def var(t, n):
        """Retourne l'index SAT pour la note n au temps t"""
        return t * MusicConfig.TOTAL_NOTES + n + 1