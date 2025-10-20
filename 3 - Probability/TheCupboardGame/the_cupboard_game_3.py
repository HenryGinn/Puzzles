import itertools as it


A = [0, 1, 2, 3, 4, 5, 6, 7]

for B in it.permutations(A, 8):
    A_count, B_count = [0], [0]
    seen = set([])
    for a, b in zip(A, B):
        A_count.append(A_count[-1] + int(a not in seen))
        B_count.append(B_count[-1] + int(b not in seen))
        seen = seen.union([a, b])

    A_count = A_count[1:]
    B_count = B_count[1:]
    difference = [i - j for i, j in zip(A_count, B_count)]
    
    if difference == [0, 0, 0, 1, 1, 1, 0, 0]:
        print(B)
