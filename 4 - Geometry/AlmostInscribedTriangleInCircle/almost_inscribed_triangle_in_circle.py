from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np


# Defining the circle

theta = np.linspace(0, 2*np.pi)
r = 1
circle_x = r * np.cos(theta)
circle_y = r * np.sin(theta)


# Defining the triangle

X = 0.25
Y = -X / np.sqrt(3)
R = np.sqrt(1 - X**2) - Y


# Defining vertices

O = np.array([X, Y])
A = O + R * np.array([0, 1])
B = O + R/2 * np.array([-np.sqrt(3), -1])
C = O + R/2 * np.array([+np.sqrt(3), -1])
D = np.array([R * np.sqrt(3) / 2 - X, Y - R / 2])
E = 0.5 * np.array([
    X + Y * np.sqrt(3) - R * np.sqrt(3),
    X * np.sqrt(3) - Y - R])
F = (A + D)
a = (A + D) / 2
b = (3*A + D) / 4

names = ["A", "B", "C", "D", "E", "F", "a", "b"]
points = np.array([A, B, C, D, E, F, a, b])

# Plotting with matplotlib

fig, ax = plt.subplots(1)
ax.set_aspect(1)

ax.plot(circle_x, circle_y, "k")
triangle_rhs = Polygon([A, D, C], color="tab:red")
triangle_lhs = Polygon([A, E, B], color="tab:red")
ax.add_patch(triangle_rhs)
ax.add_patch(triangle_lhs)
ax.plot(*np.array([B, D]).T, "k")
ax.plot(*np.array([E, D]).T, "k")

#plt.show()


# Plotting with tikz

lines = []

for point, name in zip(points, names):
    coord = f"({point[0]}, {point[1]})"
    lines.append(f"\\coordinate ({name}) at {coord};")

with open("Coordinates.tikz", "w+") as file:
    file.write("\n".join(lines))
