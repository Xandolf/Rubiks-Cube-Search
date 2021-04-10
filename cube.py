import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as c


def testPrint():
    np.random.seed(19680801)
    Z = [[1, 5, 1], [2, 3, 6], [4, 1, 2]]
    Z = [[1, 5, 1], [2, 3, 6], [4, 1, 2]]
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    cMap = c.ListedColormap(['y', 'b', 'r', 'g', 'w', 'k'])
    ax.axes.set_axis_off()
    ax2.axes.set_axis_off()
    blk = c.hex2color("000000")
    ax.pcolormesh(Z, cmap=cMap)
    Z = np.rot90(Z, 1)
    print(Z)
    ax2.pcolormesh(Z, cmap=cMap, edgecolor=blk)
    plt.show()


# Displays the given cube using matplotlib
def print_cube(cube, annotate=False):
    figs = []
    axs = []
    blk = c.hex2color("000000")
    cMap = c.ListedColormap(['y', 'r', 'b', 'g', 'orange', 'w'])

    for face in cube:
        fig, ax = plt.subplots()
        ax.axes.set_axis_off()
        size = np.size(cube[0][0], 0)

        for i in range(size):
            for j in range(size):
                if annotate:
                    ax.annotate(face[i][j], xy=(j, i), xytext=(j + 0.5, i + 0.5))
        ax.pcolormesh(face, cmap=cMap, vmin=0, vmax=6, edgecolor=blk)
        axs = axs + [ax]
        figs = figs + [fig]
    plt.show()


# printCube


def init_cube(size):
    cube = []
    faces = 6
    for f in range(faces):
        face = [f] * size
        face = [face] * size
        cube += [face]
    return np.array(cube)


# init_cube


def rotate_face(cube, faceNumber, direction):
    cube[faceNumber] = np.rot90(cube[faceNumber], direction)
    return cube


def x_rotation(cube, location, direction):
    # Rotate Faces on the end (either 0 or size-1)
    size = np.size(cube[0][0], 0)

    if (location == 0):
        cube = rotate_face(cube, 2, direction)
    elif (location == size - 1):
        cube = rotate_face(cube, 3, -direction)
    # Always rotate the columns

    # Clockwise
    if direction > 0:
        for i in range(size):
            temp = np.copy(cube[1][i][location])
            cube[1][i][location] = cube[0][i][location]
            cube[0][i][location] = cube[4][size - 1 - i][size - 1 - location]
            cube[4][size - 1 - i][size - 1 - location] = cube[5][i][location]
            cube[5][i][location] = temp

    # Counter Clockwise
    elif direction < 0:
        for i in range(size):
            temp = np.copy(cube[1][i][location])
            cube[1][i][location] = np.copy(cube[5][i][location])
            cube[5][i][location] = np.copy(cube[4][size - 1 - i][size - 1 - location])
            cube[4][size - 1 - i][size - 1 - location] = np.copy(cube[0][i][location])
            cube[0][i][location] = temp

    return cube


# Rotates section of the cube (based on location) either clockwise or counter clockwise around y axis
# The Direction of the rotation is based on the given direction
# returns the rotated cube
def y_rotation(cube, location, direction):
    size = np.size(cube[0][0], 0)
    # rotate appropriate face the location is on either end
    if location == 0:
        cube = rotate_face(cube, 0, -direction)
    elif location == size - 1:
        cube = rotate_face(cube, 5, direction)

    # Clockwise
    if direction > 0:
        temp = np.copy(cube[1][location])
        cube[1][location] = np.copy(cube[2][location])
        cube[2][location] = np.copy(cube[4][location])
        cube[4][location] = np.copy(cube[3][location])
        cube[3][location] = temp

    # Counter Clockwise
    elif direction < 0:
        temp = np.copy(cube[1][location])
        cube[1][location] = np.copy(cube[3][location])
        cube[3][location] = np.copy(cube[4][location])
        cube[4][location] = np.copy(cube[2][location])
        cube[2][location] = np.copy(temp)

    return cube


# Seems to be working

def z_rotation(cube, location, direction):
    size = np.size(cube[0][0], 0)
    # rotate appropriate face the location is on either end
    if location == 0:
        cube = rotate_face(cube, 1, -direction)
    elif location == size - 1:
        cube = rotate_face(cube, 4, direction)

    # clockwise
    if direction > 0:
        for j in range(size):
            cube[5][location][j], cube[2][size - 1 - j][location], cube[0][size - 1 - location][size - 1 - j], \
            cube[0][size - 1 - location][size - 1 - j], cube[3][j][size - 1 - location] = \
                cube[2][size - 1 - j][location], cube[0][size - 1 - location][size - 1 - j], \
                cube[0][size - 1 - location][size - 1 - j], cube[3][j][size - 1 - location], cube[5][location][j]


    # Counter Clockwise
    elif direction < 0:
        for i in range(size):
            temp = cube[5][location][i]
            cube[5][location][i] = cube[3][i][size - 1 - location]
            cube[3][i][size - 1 - location] = cube[0][size - 1 - location][size - 1 - i]
            cube[0][size - 1 - location][size - 1 - i] = cube[2][size - 1 - i][location]
            cube[2][size - 1 - i][location] = temp
    return cube


# returns all potential actions for a given cube
def getAllActions(cube):
    size = np.size(cube[0][0], 0)
    transitions = []
    # adds a rotation of each axis for the size of our cube
    # A rotation can be clockwise = 1, or counter-clockwise = -1
    for i in range(size):
        transitions += [(i, 'X', 1)]
        transitions += [(i, 'X', -1)]
        transitions += [(i, 'Y', 1)]
        transitions += [(i, 'Y', -1)]
        transitions += [(i, 'Z', 1)]
        transitions += [(i, 'Z', -1)]
    return transitions


def getActionResult(cube, action):
    if action[2] == 'X':
        x_rotation(cube, action[0], action[2])
    elif action[2] == 'Y':
        y_rotation(cube, action[0], action[2])
    elif action[2] == 'Z':
        z_rotation(cube, action[0], action[2])

    return cube



def is_goal_state(cube):
    size = np.size(cube[0][0], 0)
    for face in cube:
        for i  in range(size):
            for j in range (size):
                if face[i][j] != face[0][0]:
                    return False
    return True
