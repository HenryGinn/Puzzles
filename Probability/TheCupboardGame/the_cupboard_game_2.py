"""
This aims to explore a more abstract version of the problem. The goal is
to encode only the information that matters about what cupboards are
visited yet still arrive at the same answer as the_cupboard_game_1.
"""


import itertools as it


# The indices of the cupboards that are visited.
A = [0, 1, 2, 3, 4, 5, 6, 7]
B = [0, 4, 1, 5, 2, 6, 3, 7]

# The number of cupboards visited unseen by anyone.
a = [1, 2, 3, 4, 4, 4, 4, 4]
b = [1, 2, 2, 3, 3, 4, 4, 4]

# The difference in the number of unseen cupboards visited.
d = [0, 0, 1, 1, 1, 0, 0, 0]

count = 0
for stars in it.combinations(range(8), 2):
    for star in star:
        if A[star] != B[star]:
            
print(count)
