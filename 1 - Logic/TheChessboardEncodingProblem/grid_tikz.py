import os

import numpy as np


square = np.array([
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 0],
    [0, 0]])

def draw(rows, cols):
    lines = []
    for row in range(8):
        for col in range(8):
            coords = [row, col] + square
            coords = " -- ".join([f"({i}, {j})" for (i, j) in coords])
            match ((row + col) % 2 == 0, (col in cols or row in rows)):
                case (True, True):   opacity, color = 0.4,  "WildStrawberry"
                case (False, True):  opacity, color = 0.2,  "WildStrawberry"
                case (True, False):  opacity, color = 0.25, "black"
                case (False, False): opacity, color = 0.1,  "black"
            lines.append(f"\\draw[fill={color}, fill opacity={opacity}] {coords};")
    return lines

scale = 0.7

data = [
    [[0, 1, 2, 3], []],
    [[0, 1, 4, 5], []],
    [[0, 2, 4, 6], []],
    [[], [7, 6, 5, 4]],
    [[], [7, 6, 3, 2]],
    [[], [7, 5, 3, 1]]]

for i, (rows, cols) in enumerate(data):
    with open(f"Chessboard_{i + 1}.tikz", "w+") as file:
        lines = draw(rows, cols)
        file.writelines("\n".join(lines))
