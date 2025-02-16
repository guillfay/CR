import config, synth, gophersat, gen, play

synth.generate_cnf()
gophersat.execute_command("gophersat_win64 music.cnf > solution.txt")
with open("solution.txt", "r") as f:  # Spécifier l'encodage UTF-16
    solution_text = f.read()
gen.generate_midi(gen.parse_solution(solution_text))
play.play_midi("output.mid")