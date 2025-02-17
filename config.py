# config.py

class MusicConfig:
    TOTAL_STEPS = 8  # Nombre de temps

    # Dictionnaire des styles avec les notes correspondantes
    STYLES = {
        "classical": [60, 62, 64, 65, 67, 69, 71],  # Do, Ré, Mi, Fa, Sol, La, Si
        "jazz": [60, 62, 64, 65, 67, 69, 71, 73, 74],  # Extensions (9e, 11e)
        "blues": [60, 62, 63, 64, 65, 67, 68, 69, 71],  # Blue notes (63 = Mib, 68 = Lab)
        "electro": [60, 62, 64, 65, 67, 69, 71]  # Notes classiques (peut être modifié)
    }

    # Choix du style
    STYLE = "jazz"  # Modifier ici pour tester différents styles

    NOTE_MAPPING = STYLES[STYLE]
    TOTAL_NOTES = len(NOTE_MAPPING)

    @classmethod
    def num_vars(cls):
        return cls.TOTAL_NOTES * cls.TOTAL_STEPS

    @staticmethod
    def var(t, n):
        """Retourne l'index SAT pour la note n au temps t"""
        return t * MusicConfig.TOTAL_NOTES + n + 1
