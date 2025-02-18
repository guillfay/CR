import subprocess
import os

# Étape 1️⃣ : Générer le fichier CNF (synth.py)
print("🔹 Génération du fichier CNF...")
subprocess.run(["python", "synth.py"], check=True)

# Limite de tentatives
max_attempts = 50
attempt = 0
solution_found = False

solver_type = 'PB'

if solver_type=='SAT':
    while not solution_found and attempt < max_attempts:
        attempt += 1
        print(f"🔹 Tentative #{attempt} de résolution SAT avec Gophersat...")

        # Supprimer le fichier solution.txt précédent pour une nouvelle tentative propre
        if os.path.exists("solution.txt"):
            os.remove("solution.txt")

        # Exécuter Gophersat pour résoudre le CNF
        gophersat_cmd = ["./gophersat_win64", "music.cnf"]
        with open("solution.txt", "w", encoding="utf-8") as solution_file:
            subprocess.run(gophersat_cmd, stdout=solution_file, check=True)

        # Vérifier si une solution a été trouvée
        with open("solution.txt", "r", encoding="utf-8") as f:
            if "UNSATISFIABLE" in f.read():
                print(f"❌ Aucune solution trouvée par le SAT solver (tentative #{attempt}) !")
            else:
                solution_found = True
                print("✅ Solution trouvée !")

        # Ré-générer le fichier CNF pour la prochaine tentative
        if not solution_found:
            print("🔄 Réinitialisation du problème CNF pour la prochaine tentative...")
            subprocess.run(["python", "synth.py"], check=True)

    # Si une solution a été trouvée, procéder aux étapes suivantes
    if solution_found:
        # Étape 3️⃣ : Générer le fichier MIDI (gen.py)
        print("🔹 Génération du fichier MIDI...")
        subprocess.run(["python", "gen.py"], check=True)

        # Étape 4️⃣ : Jouer le fichier MIDI (play.py)
        print("🔹 Lecture du fichier MIDI...")
        subprocess.run(["python", "play.py"], check=True)

        print("✅ Processus terminé avec succès ! 🎶")
    else:
        print("❌ Échec de la résolution SAT après 15 tentatives.")

if solver_type=='PB':

    # Étape 1️⃣ : Générer la solution avec Gurobi (synthPB.py)
    print("🔹 Génération de la solution avec Gurobi (synthPB.py)...")
    subprocess.run(["python", "synthPB.py"], check=True)

    # Vérifier que le fichier solution.txt a bien été généré et qu'il contient une solution
    if os.path.exists("solution.txt"):
        with open("solution.txt", "r", encoding="utf-8") as f:
            content = f.read()
        if "v" in content:
            print("✅ Solution trouvée !")
            
            # Étape 2️⃣ : Générer le fichier MIDI (gen.py)
            print("🔹 Génération du fichier MIDI (gen.py)...")
            subprocess.run(["python", "gen.py"], check=True)

            # Étape 3️⃣ : Jouer le fichier MIDI (play.py)
            print("🔹 Lecture du fichier MIDI (play.py)...")
            subprocess.run(["python", "play.py"], check=True)

            print("✅ Processus terminé avec succès ! 🎶")
        else:
            print("❌ Le fichier solution.txt ne contient pas de solution valide.")
    else:
        print("❌ Le fichier solution.txt n'a pas été généré.")