import itertools as it

import numpy as np


winner_lookup = ["Alice", "Draw", "Bob"]


def get_winners(A, B):
    winners = [
            get_winner(A, B, stars)
            for stars in it.combinations(range(8), 2)]
    return winners

def get_winner(A, B, stars):
    A_cupboard = min([A.index(star) for star in stars])
    B_cupboard = min([B.index(star) for star in stars])
    winner = compare_A_and_B(A_cupboard, B_cupboard)
    return winner

def compare_A_and_B(A_cupboard, B_cupboard):
    if A_cupboard < B_cupboard:
        return 0
    elif A_cupboard == B_cupboard:
        return 1
    else:
        return 2

def get_distribution(winners):
    A_wins = winners.count(0)
    draws = winners.count(1)
    B_wins = winners.count(2)
    distribution = (A_wins, draws, B_wins)
    return distribution

def display(A, B, winners):
    distribution = get_distribution(winners)
    A_wins, draws, B_wins = distribution
    print(f"{A_wins:02}, {draws:02}, {B_wins:02}")


A = [0, 1, 2, 3, 4, 5, 6, 7]
B = [0, 4, 1, 5, 2, 6, 3, 7]

#results = {
#    B: get_distribution(get_winners(A, B))
#    for B in it.permutations(A, 8)}
    
#keys = list(set(results.values()))
#data = {key: [] for key in keys}
#for key, value in results.items():
#    data[value].append(key)
winners = get_winners(A, B)
display(A, B, winners)
