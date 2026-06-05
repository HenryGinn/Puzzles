import itertools
import os

import numpy as np
import pandas as pd


path = os.path.join(os.path.dirname(__file__), "ThreeHatsLookups.csv")
df = pd.read_csv(path, names=list(range(27)))
v = df.values

a = v[:50, ::3]

scenarios = list(itertools.product([0, 1, 2], repeat=3))
scenario_index_lookup = {}
index = 0
for person_a in range(3):
    for person_b in range(3):
        for guess in range(3):
            scenario_index_lookup[index+0, guess] = scenarios.index((guess, person_a, person_b))
            scenario_index_lookup[index+1, guess] = scenarios.index((person_a, guess, person_b))
            scenario_index_lookup[index+2, guess] = scenarios.index((person_a, person_b, guess))
        index += 3

for i in a:
    for j in i:
        print(scenarios[j], end=", ")
    print("")
