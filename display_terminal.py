# display_terminal.py
from engine import dice_game_main

def run_terminal():
    counts = dice_game_main()
    print("Quantum Dice Measurement Counts:")
    for bitstring, count in counts.items():
        print(f"  |{bitstring}>: {count}")
