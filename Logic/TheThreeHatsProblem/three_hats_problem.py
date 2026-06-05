import time
import itertools

import numpy as np


def recurse(depth, lookup, history):
    if depth < N**N:
        for colour in range(3):
            index = scenario_index_lookup[(depth, colour)]
            if not history[index]:
                new_history = history.copy()
                new_history[index] = True
                recurse(depth + 1, lookup + [colour], new_history)
    else:
        results.append(lookup)

N = 4
results = []

scenarios = list(itertools.product(list(range(N)), repeat=N))
scenario_index_lookup = {}
index = 0

for person_a in range(2):
    for guess in range(2):
        scenario_index_lookup[index + 0, guess] = scenarios.index((guess, person_a))
        scenario_index_lookup[index + 1, guess] = scenarios.index((person_a, guess))
    index += 2

"""
for person_a in range(3):
    for person_b in range(3):
        for guess in range(3):
            scenario_index_lookup[index + 0, guess] = scenarios.index((guess, person_a, person_b))
            scenario_index_lookup[index + 1, guess] = scenarios.index((person_a, guess, person_b))
            scenario_index_lookup[index + 2, guess] = scenarios.index((person_a, person_b, guess))
        index += 3
"""
"""
for person_a in range(4):
    for person_b in range(4):
        for person_c in range(4):
            for guess in range(4):
                scenario_index_lookup[index + 0, guess] = scenarios.index((guess, person_a, person_b, person_c))
                scenario_index_lookup[index + 1, guess] = scenarios.index((person_a, guess, person_b, person_c))
                scenario_index_lookup[index + 2, guess] = scenarios.index((person_a, person_b, guess, person_c))
                scenario_index_lookup[index + 3, guess] = scenarios.index((person_a, person_b, person_c, guess))
            index += 4
"""

recurse(0, [], [False]*N**N)
print(len(results))

# scenario_index_lookup tells you what scenario would be guessed
# correctly. The index corresponds to the position in the lookup as give
# below and the second number is what colour they guess.

#  0: person 0 looking at person 1 wearing 0 and person 2 wearing 0
#  1: person 1 looking at person 0 wearing 0 and person 2 wearing 0
#  2: person 2 looking at person 0 wearing 0 and person 1 wearing 0
#  3: person 0 looking at person 1 wearing 0 and person 2 wearing 1
#  4: person 1 looking at person 0 wearing 0 and person 2 wearing 1
#  5: person 2 looking at person 0 wearing 0 and person 1 wearing 1
#  6: person 0 looking at person 1 wearing 0 and person 2 wearing 2
#  7: person 1 looking at person 0 wearing 0 and person 2 wearing 2
#  8: person 2 looking at person 0 wearing 0 and person 1 wearing 2
#  9: person 0 looking at person 1 wearing 1 and person 2 wearing 0
# 10: person 1 looking at person 0 wearing 1 and person 2 wearing 0
# 11: person 2 looking at person 0 wearing 1 and person 1 wearing 0
# 12: person 0 looking at person 1 wearing 1 and person 2 wearing 1
# 13: person 1 looking at person 0 wearing 1 and person 2 wearing 1
# 14: person 2 looking at person 0 wearing 1 and person 1 wearing 1
# 15: person 0 looking at person 1 wearing 1 and person 2 wearing 2
# 16: person 1 looking at person 0 wearing 1 and person 2 wearing 2
# 17: person 2 looking at person 0 wearing 1 and person 1 wearing 2
# 18: person 0 looking at person 1 wearing 2 and person 2 wearing 0
# 19: person 1 looking at person 0 wearing 2 and person 2 wearing 0
# 20: person 2 looking at person 0 wearing 2 and person 1 wearing 0
# 21: person 0 looking at person 1 wearing 2 and person 2 wearing 1
# 22: person 1 looking at person 0 wearing 2 and person 2 wearing 1
# 23: person 2 looking at person 0 wearing 2 and person 1 wearing 1
# 24: person 0 looking at person 1 wearing 2 and person 2 wearing 2
# 25: person 1 looking at person 0 wearing 2 and person 2 wearing 2
# 26: person 2 looking at person 0 wearing 2 and person 1 wearing 2
