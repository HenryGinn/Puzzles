from itertools import permutations

import numpy as np
import pandas as pd

ball_sets = [
    [2, 2],    # Equal light
    [4, 4],    # Equal heavy
    [1, 2],    # Non-equal light
    [4, 5],    # Non-equal heavy
    [2, 4],    # Opposite heavy and light
    [5, 2],    # Heavier heavy
    [4, 1]]    # Lighter heavy

indexes = list(range(12))
base_balls = [3]*12
all_balls = []
sets = []

n = 4
m = 12 - 2*n

for ball_set in ball_sets:
    for indexer in permutations(indexes, 2):
        balls = base_balls.copy()
        balls[indexer[0]] = ball_set[0]
        balls[indexer[1]] = ball_set[1]
        all_balls.append(tuple(balls))
        sets.append(ball_set)

values = np.concatenate((all_balls, sets), axis=1)
df = pd.DataFrame(values)
df = df.drop_duplicates().reset_index(drop=True)
df.columns = list(range(12)) + ["Odd1", "Odd2"]
df["Left"] = df.loc[:, :n-1].sum(axis=1) - n*3
df["Right"] = df.loc[:, n:2*n-1].sum(axis=1) - n*3
df["Off"] = df.loc[:, 2*n:11].sum(axis=1) - m*3
df["State"] = None
df.loc[df["Left"] == df["Right"], "State"] = "Balanced"
df.loc[df["Left"] > df["Right"], "State"] = "Left"
df.loc[df["Left"] < df["Right"], "State"] = "Right"
df_pos = df.iloc[:, :12]
odd1 = df_pos == df["Odd1"].values.reshape(-1, 1)
odd2 = df_pos == df["Odd2"].values.reshape(-1, 1)
df["Odd1Index"] = odd1.idxmax(axis=1)
df["Odd2Index"] = odd2.iloc[:, ::-1].idxmax(axis=1)
df["Count"] = 1
index_to_pos = {index: "Left" for index in range(n)}
index_to_pos.update({index: "Right" for index in range(n, 2*n)})
index_to_pos.update({index: "Off" for index in range(2*n, 12)})
df["Odd1Pos"] = df.loc[:, "Odd1Index"].map(index_to_pos)
df["Odd2Pos"] = df.loc[:, "Odd2Index"].map(index_to_pos)
configurations = df.groupby(["State", "Odd1Pos", "Odd2Pos", "Odd1", "Odd2"]).agg({"Count": "sum"}).reset_index()
print(configurations)
