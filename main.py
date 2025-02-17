import config, synth, synth_style, synth_PB, gophersat, gen, play

type = 'PB'

if type=='SAT':
    style=False
    synth.generate_cnf() if not style else synth_style.generate_cnf()
    gophersat.execute_command("gophersat_win64 music.cnf > solution.txt")
    with open("solution.txt", "r") as f:  # Spécifier l'encodage UTF-16
        solution_text = f.read()
    gen.generate_midi(gen.parse_solution(solution_text))
    play.play_midi("output.mid")

if type=='PB':
    style=True
    synth_PB.generate_opb()
    gophersat.execute_command("gophersat_win64 music.opb > solution.txt")
    with open("solution.txt", "r") as f:  # Spécifier l'encodage UTF-16
        solution_text = f.read()
    gen.generate_midi(gen.parse_solution(solution_text))
    play.play_midi("output.mid")