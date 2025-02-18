import subprocess

# Étape 1️⃣ : Générer le fichier CNF (synth.py)
print("🔹 Génération du fichier CNF...")
subprocess.run(["python", "synth.py"], check=True)

solver='PB'

if solver == 'SAT':
    
    # Étape 1️⃣ : Générer le fichier CNF (synth.py)
    print("🔹 Génération du fichier CNF...")
    subprocess.run(["python", "synth.py"], check=True)

    # Étape 2️⃣ : Exécuter Gophersat pour résoudre le CNF
    print("🔹 Résolution SAT avec Gophersat...")
    gophersat_cmd = ["./gophersat_win64", "music.cnf"]
    with open("solution.txt", "w", encoding="utf-8") as solution_file:
        subprocess.run(gophersat_cmd, stdout=solution_file, check=True)

if solver == 'PB':

    # Étape 1️⃣ : Générer le fichier CNF (synth.py)
    print("🔹 Génération du fichier CNF...")
    subprocess.run(["python", "synthPB.py"], check=True)

    # Étape 2️⃣ : Exécuter Gophersat pour résoudre le CNF
    print("🔹 Résolution PB avec Gophersat...")
    gophersat_cmd = ["./gophersat_win64", "music.opb"]
    with open("solution.txt", "w", encoding="utf-8") as solution_file:
        subprocess.run(gophersat_cmd, stdout=solution_file, check=True)


# Vérifier si aucune solution n'a été trouvée
with open("solution.txt", "r", encoding="utf-8") as f:
    if "UNSATISFIABLE" in f.read():
        print("❌ Aucune solution trouvée par le SAT solver !")

    else:
        # Étape 3️⃣ : Générer le fichier MIDI (gen.py)
        print("🔹 Génération du fichier MIDI...")
        subprocess.run(["python", "gen.py"], check=True)

        # Étape 4️⃣ : Jouer le fichier MIDI (play.py)
        print("🔹 Lecture du fichier MIDI...")
        subprocess.run(["python", "play.py"], check=True)

        print("✅ Processus terminé avec succès ! 🎶")
