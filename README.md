# Connaissances et raisonnement

*Erwan DAVID - Guillaume FAYNOT*

# Installer les packages

Pour installer les bibliothèques python utiles, exécuter la commande suivante

`pip install -r requirements.txt`

# Gophersat

Sous Windows, la version utilisée est `gophersat_win64`. Ce solveur permet de lire des fichiers `.cnf` et de faire la résolution de problèmes SAT.

# Gurobi

Pour la résolution de problèmes pseudo-booléens et de problèmes de programmation linéaire, nous utilisons gurobi (conformément aux pré-requis du cours de Systèmes de Décisions et Préférences)

# Structure du code

Le code est composé des scripts suivants : 

- `main.py` : exécute tous les fichiers nécessaires à la génération de musique

    Renseigner en en-tête le type solveur souhaité : SAT, PB ou MILP

- Plusieurs scripts qui font office de synthétiseur :
    - `synth.py` : génère un fichier cnf nommé `music.cnf`

        Avec quelques paramètres, ce script génère au format cnf des variables et des contraintes SAT pour générer une musique

    - `synthPB.py` : génère un fichier txt contenant la partition solution aux contraintes pseudobooléennes

    - `synthMILP.py` : génère un fichier txt contenant la partition solution aux contraintes MILP

- `gen.py` : utilise un fichier texte `solution.txt` renvoyé par le solveur gophersat ou gurobi et génère un fichier midi nommé `output.mid`

    Ce script se charge de convertir la solution satisfiable en un fichier midi

- `play.py` : utilise un fichier midi  `output.mid` pour en jouer la musique dans le terminal

# Exécution

Pour générer votre propre musique à l'aide d'un solveur SAT, il faut :

- renseigner dans `main.py` le type de solveur que vous souhaitez utiliser : SAT, PB ou MILP
- exécuter `main.py`

# Rapport

- Le rapport précisant le problème traité et la démarche suivie peut être consulté [ici](docs/report.pdf)
- Un essai sur l'IA hybride comme vu en TD peut-être consulté [ici](docs/IA_hybride_musique.md)