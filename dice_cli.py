from dice_game_functions import *

qc = createCircuit()
counts = ideal_simulator(qc)[0]
selected = returnSelectedState(counts)

print(selected)