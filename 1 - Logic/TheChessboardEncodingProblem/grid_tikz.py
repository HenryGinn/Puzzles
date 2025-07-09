import os
import random

import numpy as np


random.seed(36)

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
            coords = get_coords(row, col)
            match ((row + col) % 2 == 0, (col in cols or row in rows)):
                case (True, True):   opacity, color = 0.4,  "WildStrawberry"
                case (False, True):  opacity, color = 0.2,  "WildStrawberry"
                case (True, False):  opacity, color = 0.25, "black"
                case (False, False): opacity, color = 0.1,  "black"
            lines.append(f"\\draw[fill={color}, fill opacity={opacity}] {coords};")
    return lines

def get_coords(row, col):
    coords = [col, row] + square
    coords = " -- ".join([f"({i}, {j})" for (i, j) in coords])
    return coords

scale = 0.7


# Drawing the six regions

region_rows_and_cols = [
    [[], [4, 5, 6, 7]],
    [[], [2, 3, 6, 7]],
    [[], [1, 3, 5, 7]],
    [[0, 1, 2, 3], []],
    [[0, 1, 4, 5], []],
    [[0, 2, 4, 6], []]]

for i, (rows, cols) in enumerate(region_rows_and_cols):
    lines = draw(rows, cols)
    with open(f"Chessboard_{i + 1}.tikz", "w+") as file:
        file.writelines("\n".join(lines))


# Drawing an example board

lines = draw([], [])
lines.append("")

state_lookup = {
    (row, col): random.randint(0, 1)
    for row in range(8)
    for col in range(8)}

letter_lookup = {
    0: "T",
    1: "H"}

encoded_row = random.randint(0, 7)
encoded_col = random.randint(0, 7)
coords = get_coords(encoded_row, encoded_col)
lines.append(f"\\draw[fill=WildStrawberry, fill opacity=0.4] {coords};\n")

for row in range(8):
    for col in range(8):
        cell_state = state_lookup[(row, col)]
        letter = letter_lookup[cell_state]
        lines.append(f"\\draw[fill=white, fill opacity=1]({col + 0.5}, {row + 0.5}) circle (0.35);")
        lines.append(f"\\node at ({col + 0.5}, {row + 0.5}) {{{letter}}};")

with open(f"ChessboardExample.tikz", "w+") as file:
    file.writelines("\n".join(lines))


# Creating a table that describes the results

region_to_flip_lookup = {
    0: "Yes",
    1: "No"}

lines = []
encoded_parities = [(encoded_row not in rows) and (encoded_col not in cols)
                    for rows, cols in region_rows_and_cols]

for region_index, (rows, cols) in enumerate(region_rows_and_cols):
    head_total = sum([
        state_lookup[(row, col)]
        for row in range(8)
        for col in range(8)
        if (row in rows or col in cols)])
    head_parity = head_total % 2
    encoded_parity = encoded_parities[region_index]
    parity_change = head_parity ^ encoded_parity
    region_to_flip = region_to_flip_lookup[parity_change]
    lines.append(f"{region_index + 1} & {head_total} & {head_parity} & {encoded_parity} & {parity_change} & {region_to_flip}  \\\\")

with open(f"ChessboardExampleTable.tex", "w+") as file:
    file.writelines("\n".join(lines))





