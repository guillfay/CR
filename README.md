# CR

# Installer les packages

Pour installer les bibliothèques python utiles

`pip install -r requirements.txt`

# Gophersat

Sous Windows, la version utilisée est `gophersat_win64`

# Structure du code

Le code est composé des script suivants : 

- `synth.py` : génère un fichier cnf nommé `music.cnf`
Avec quelques paramètres, ce script génère au format cnf des variables et des contraintes SAT pour générer une musique

- `gen.py` : utilise un fichier texte `solution.txt` renvoyé par le solveur gophersat et génère un fichier midi nommé `output.mid`
Ce script se charge de convertir la solution satisfiable en un fichier midi

- `play.py` : utilise un ffichier midi  `output.mid` pour en jouer la musique dans le terminal

# Exécution

Pour générer votre propre musique à l'aide d'un solveur SAT, il faut :

- exécuter `synth.py`
- dans le terminal ( :warning: exécuter en tant qu'administrateur :warning: ), exécuter la commande : `gophersat_win64 music.cnf > solution.txt`
- exécuter `gen.py`
- exécuter `play.py`
