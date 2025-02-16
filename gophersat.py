import subprocess

def execute_command(command):
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(process.stdout)  # Affiche la sortie standard (si besoin)
        return process.returncode
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {e}")
        print(e.stderr)  # Affiche les erreurs (si besoin)
        return e.returncode