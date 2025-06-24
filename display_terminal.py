# display_terminal.py

from engine import run_quantum_dice_once

def run_terminal():
    print("\n[INFO] Terminal mode activated.")
    print("Rolling the quantum dice...\n")

    counts = run_quantum_dice_once()

    print("Quantum Dice Measurement Counts:")
    for key, value in counts.items():
        print(f"{key}: {value}")

    print("\n[INFO] Game finished.")