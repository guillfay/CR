# Knowledge and Reasoning - Music Generation Using Solvers

*Erwan DAVID - Guillaume FAYNOT*

# Install Packages

To install the required Python libraries, run the following command:

`pip install -r requirements.txt`

# Gophersat

On Windows, the version used is `gophersat_win64`. This solver can read `.cnf` files and solve SAT problems.

# Gurobi

For solving pseudo-Boolean problems and linear programming problems, we use Gurobi (as required by the Decision Systems and Preferences course).

# Code Structure

The code consists of the following scripts:

- `main.py`: runs all the necessary files for music generation

    Specify at the top of the file the desired solver type: SAT, PB, or MILP

- Several scripts act as synthesizers:
    - `synth.py`: generates a cnf file named `music.cnf`

        With some parameters, this script generates SAT variables and constraints in cnf format to create music

    - `synthPB.py`: generates a txt file containing the solution partition for the pseudo-Boolean constraints

    - `synthMILP.py`: generates a txt file containing the solution partition for the MILP constraints

- `gen.py`: uses a text file `solution.txt` returned by the Gophersat or Gurobi solver and generates a midi file named `output.mid`

    This script converts the satisfiable solution into a midi file

- `play.py`: uses a midi file `output.mid` to play the music in the terminal

# Execution

To generate your own music using a SAT solver, you need to:

- specify in `main.py` the type of solver you want to use: SAT, PB, or MILP
- run `main.py`

# Report

- The report detailing the problem addressed and the approach taken can be found [here](docs/report.pdf)
- An essay on hybrid AI as discussed in tutorials can be found [here](docs/IA_hybride_musique.md)
