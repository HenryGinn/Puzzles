"""
This program is a tool to help solve the twelve islanders problem where
there are two odd islanders. All possible weighings are applied to a set
of states and the split between left, balanced, and right is found.
"""


from itertools import permutations, product

import numpy as np
import pandas as pd

def generate_states():

    # Different ways two balls can be different
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

    # Generating states
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
    df = df.iloc[:, :12]
    return df

def split_states(states, weighing):
    left_sum = states.multiply(weighing == -1, axis=1).sum(axis=1)
    right_sum = states.multiply(weighing == 1, axis=1).sum(axis=1)
    difference = left_sum - right_sum
    left = states.loc[(difference < 0), :]
    balanced = states.loc[(difference == 0), :]
    right = states.loc[(difference > 0), :]
    return left, balanced, right

def count_splits(states, df):
    # Each row is a weighing
    # Each column is a state
    differences = np.multiply(
        states.values.reshape(1, -1, 12),
        df.values.reshape(-1, 1, 12)
        ).sum(axis=2)
    count = df.copy()
    count.loc[:, "Left"] = (differences > 0).sum(axis=1)
    count.loc[:, "Balanced"] = (differences == 0).sum(axis=1)
    count.loc[:, "Right"] = (differences < 0).sum(axis=1)
    add_deviation_column(states, count)
    count = count.sort_values("Deviation")
    return count

def add_deviation_column(states, count):
    count["Deviation"] = np.max(
        [(count[column] - states.shape[0]/3)
         .round().abs().astype("int16").values
        for column in outcomes], axis=0)
    return count

def solve(states, outcome_history, weighing_history):
    if len(weighing_history) < weighing_count:
        count = count_splits(states, df)
        weighing_index = count.index[0]
        splits = split_states(states, df.iloc[weighing_index, :])
        for split, outcome in zip(splits, outcomes):
            solve(split, outcome_history + [outcome], weighing_history + [weighing_index])
    else:
        all_outcomes.append(outcome_history)
        all_weighings.append(weighing_history)

def postprocess_solution():
    global all_weighings, all_outcomes
    all_weighings = pd.DataFrame(all_weighings)
    all_outcomes = pd.DataFrame(all_outcomes)

    all_outcomes = all_outcomes.iloc[::3, :-1]
    all_weighings = all_weighings.iloc[::3, :]
    outcomes = []
    weighings = []
    for i in range(weighing_count):
        outcomes = [all_outcomes] + outcomes
        weighings = [all_weighings.iloc[:, -1]] + weighings
        all_outcomes = all_outcomes.iloc[::3, :-1]
        all_weighings = all_weighings.iloc[::3, :-1]

    outcomes = pd.concat(outcomes, axis=0)
    weighings = pd.concat(weighings, axis=0)
    solution = pd.concat((outcomes, weighings), axis=1).reset_index(drop=True)
    solution.columns = weighing_columns[:-1] + ["ConfigurationID"]
    configurations = df.iloc[solution["ConfigurationID"], :].reset_index(drop=True)
    solution = pd.concat((solution, configurations), axis=1)
    solution.to_csv("Solution.csv")

def follow_solution(index, state):
    state_solution = solution.copy()
    for weighing_number in range(weighing_count):
        weighing_ID = state_solution.loc[0, "ConfigurationID"]
        result = get_result(state, weighing_ID)
        state_solution = (
            state_solution.loc[
                state_solution.iloc[:, weighing_number] == result]
            .reset_index(drop=True))
        state_history[index, weighing_number] = outcome_lookup[result]

def get_result(state, weighing_ID):
    weighing = df.iloc[weighing_ID]
    difference = weighing.multiply(state).sum()
    result = weighing_result_lookup[(difference == 0, difference > 0)]
    return result
    

outcomes = ["Left", "Balanced", "Right"]
outcome_lookup = {outcome: i - 1 for i, outcome in enumerate(outcomes)}
outcome_inverse_lookup = {value: key for key, value in outcome_lookup.items()}
all_states = generate_states()

weighing_result_lookup = {
    (True, False): "Balanced",
    (False, False): "Left",
    (False, True): "Right"}

df = pd.DataFrame([
    i for i in product([-1, 0, 1], repeat=12)
    if i.count(-1) == i.count(1)])

all_outcomes = []
all_weighings = []

weighing_count = 6
weighing_columns = [f"Weighing{i+1}" for i in range(weighing_count)]
solve(all_states, [], [])
postprocess_solution()
solution = pd.read_csv("Solution.csv", index_col=0)
state_history = np.empty((all_states.shape[0], weighing_count), dtype="int8")

for index, state in all_states.iterrows():
    follow_solution(index, state)

state_history = pd.DataFrame(state_history)
state_history = state_history.sort_values(by=list(state_history.columns))
state_history = pd.concat((state_history.replace(outcome_inverse_lookup), all_states), axis=1)
state_history.columns = weighing_columns + list(range(12))
state_history.reset_index(drop=True, inplace=True)
state_history.loc[:, "Configuration"] = state_history.loc[:, list(range(12))].apply(lambda x: sorted(list(set(x))), axis=1)
state_history.to_csv("StateHistory.csv")

