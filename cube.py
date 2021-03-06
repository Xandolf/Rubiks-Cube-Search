import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as c
import random

global size


def test_print():
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
    size = np.size(cube[0][0], 0)
    figs = []
    axs = []
    blk = c.hex2color("000000")
    cMap = c.ListedColormap(['y', 'r', 'b', 'g', 'orange', 'w'])

    for face in cube:
        fig, ax = plt.subplots()
        ax.axes.set_axis_off()
        for i in range(size):
            for j in range(size):
                if annotate:
                    ax.annotate(face[i][j], xy=(j, i), xytext=(j + 0.5, i + 0.5))
        ax.pcolormesh(face, cmap=cMap, vmin=0, vmax=6, edgecolor=blk)
        axs = axs + [ax]
        figs = figs + [fig]
    plt.show()


# initializes the cube with each face being monochromatic with a unique color
def init_cube(size):
    cube = []
    faces = 6
    for f in range(faces):
        face = [f] * size
        face = [face] * size
        cube += [face]
    return np.array(cube)


# initializes the cube with each face being monochromatic with a unique color
def init_num_cube(size):
    cube = []
    faces = 6
    for f in range(faces):
        face = []
        for i in range(size):
            row = []
            for j in range(size):
                value = f + 6 * (j + i * size)
                row += [value]
            face += [row]
        cube += [face]
    print(cube)
    return np.array(cube)


# Rotates a face of the cube. Used when the section of the cube is one of the outer faces.
def rotate_face(cube, faceNumber, direction):
    cube[faceNumber] = np.rot90(cube[faceNumber], direction)
    return cube


# Rotates section of the cube (based on location) either clockwise or counter clockwise around specified axis
# The Direction of the rotation is based on the given direction
# returns the rotated cube
def x_rotation(cube, location, direction):
    # Rotate Faces on the end (either 0 or size-1)
    size = np.size(cube[0][0], 0)
    if location == 0:
        cube = rotate_face(cube, 2, direction)
    elif location == size - 1:
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
def get_all_actions(cube):
    size = np.size(cube[0][0], 0)
    actions = []
    # adds a rotation of each axis for the size of our cube
    # A rotation can be clockwise = 1, or counter-clockwise = -1
    for i in range(size):
        actions += [(i, 'X', 1)]
        actions += [(i, 'X', -1)]
        actions += [(i, 'Y', 1)]
        actions += [(i, 'Y', -1)]
        actions += [(i, 'Z', 1)]
        actions += [(i, 'Z', -1)]
    return actions


# returns a transformed copy of the cube (does not change the cube given to it)
def get_action_result(cube, action):
    if action[1] == 'X':
        cube_copy = x_rotation(np.copy(cube), action[0], action[2])
    elif action[1] == 'Y':
        cube_copy = y_rotation(np.copy(cube), action[0], action[2])
    elif action[1] == 'Z':
        cube_copy = z_rotation(np.copy(cube), action[0], action[2])
    else:
        cube_copy = np.copy(cube)
        print("Error: Rotation axis must be X,Y or Z. Not " + action[1] + "\n No rotation made.")
    return cube_copy


# checks if the cube is solved (all faces are monochromatic)
def is_goal_state(cube):
    size = np.size(cube[0][0], 0)
    for f in range(6):
        for i in range(size):
            for j in range(size):
                if cube[f][i][j] % 6 != f:
                    return False
    return True


def get_entropy(cube):
    size = np.size(cube[0][0], 0)
    result = 0
    # count the occurrences of each color on each face
    for face in cube:
        colorCounts = [0, 0, 0, 0, 0, 0]
        for i in range(size):
            for j in range(size):
                colorCounts[face[i][j]] = colorCounts[face[i][j]] + 1
        for i in range(6):
            probability = colorCounts[i] / (size * size)
            result += probability * safe_log2(probability)
    return -1 * result


def get_misplaced_tiles(cube):
    size = np.size(cube[0][0], 0)
    result = 0
    # count the occurrences of each color on each face
    for i in range(6):
        perfect_face = True
        for j in range(size):
            for k in range(size):
                if cube[i][j][k] % 6 != i:
                    result = result + 0.1
                    perfect_face = False
        if perfect_face:
            result = result - 1

    return result


def get_perfect_rows(cube):
    size = np.size(cube[0][0], 0)
    result = 100
    # count the occurrences of each color on each face
    for i in range(6):
        for j in range(size):
            perfect_collum = True
            perfect_row = True
            for k in range(size):
                if cube[i][j][k] % 6 == cube[i][0][k] % 6:
                    result = result - 1
                    perfect_row = False

                if cube[i][k][j] % 6 == cube[i][k][0] % 6:
                    result = result - 1
                    perfect_collum = False

            if not ( perfect_row and perfect_collum) and result > 5:
                if ( perfect_row or perfect_collum):
                    result = result - 1
            # if perfect_row and result > 3:
            #     result = result - 1
            #
            # if perfect_collum and result > 3:
            #     result = result - 1

            if perfect_row and perfect_collum and result > 6:
                result = result - 1

    return result


def get_gini(cube):
    result = 0
    size = np.size(cube[0][0], 0)

    # count the occurrences of each color on each face
    for face in cube:
        colorCounts = [0, 0, 0, 0, 0, 0]
        for i in range(size):
            for j in range(size):
                colorCounts[face[i][j]] = colorCounts[face[i][j]] + 1
        for i in range(6):
            probability = colorCounts[i] / (size * size)
            result += probability * (1 - probability)
    return -1 * result


def get_chaos(cube):
    size = np.size(cube[0][0], 0)
    result = 1
    # count the occurrences of each color on each face
    for face in cube:
        colorCounts = [1, 1, 1, 1, 1, 1]
        for i in range(size):
            for j in range(size):
                colorCounts[face[i][j]] = colorCounts[face[i][j]] + 1
        for i in range(6):
            probability = colorCounts[i] / (size * size)
            if probability > 0:
                result *= probability
    return result * -1


def safe_log2(x):
    if x == 0:
        return 0
    else:
        return np.log2(x)


# Testing Functions
def generate_random_moves(cube, moves_count):
    actions = get_all_actions(cube)
    ret_moves = []
    for i in range(moves_count):
        action_count = len(actions) - 1
        mi = random.randint(1, action_count)
        ret_moves = ret_moves + [actions[mi]]
    return ret_moves


# Inverts a given action sequence (Undo)
def invert_moves(moves):
    inv_moves = []
    for move in moves:
        inv_moves = [(move[0], move[1], -move[2])] + inv_moves
    return inv_moves


# A* search
def astar_search(cube, heuristic):
    size = np.size(cube[0][0], 0)
    nodes_expanded = 0
    # Create lists for fringe and expanded states
    e = {}
    fringe = []
    # expanded = []
    # Get all the possible rotations
    actions = get_all_actions(cube)

    # Create a start node to push onto fringe
    action_sequence = []
    cost = heuristic(cube)
    start_node = (cube, cost, action_sequence)
    fringe.append(start_node)

    # Loop while we still have elements on the fringe
    while len(fringe) > 0 and nodes_expanded < 100000:
        # Sort the fringe to get the node with the lowest cost first
        fringe = sorted(fringe, key=lambda x: x[1])
        # Get the node with the lowest cost
        current_node = fringe.pop(0)
        nodes_expanded += 1
        # Add the current node to the closed list
        print("Expanded Node", nodes_expanded, "\t ID#", str(hash(str(current_node[0]))),
              "\n Heuristic Value: ", heuristic(current_node[0]), "Cost: ", len(current_node[2]))
        # expanded.append(current_node)
        e[str(hash(str(current_node[0])))] = True

        # Check if we have reached the goal, return the path
        if is_goal_state(current_node[0]):
            return (current_node[2], nodes_expanded)

        # Else not the goal state:
        # Unzip the current node position
        currentCube, currentPath = current_node[0], current_node[2]
        # Get neighbors
        for action in actions:
            neighborCube = get_action_result(currentCube, action)
            if not_in_expanded(neighborCube, e):
                # if not_in_expanded(expanded, neighborCube):
                neighborPath = currentPath + [action]
                neighborCost = len(neighborPath) + heuristic(neighborCube)
                neighbor = (neighborCube, neighborCost, neighborPath)
                if add_to_fringe(fringe, neighbor):
                    fringe.append(neighbor)
    # Return None, no path is found
    return None


# Check if a neighbor should be added to open list
def add_to_fringe(fringe, neighbor):
    for node in fringe:
        if (neighbor[0] == node[0]).all() and neighbor[2] >= node[2]:
            return False
    return True


# Check if a neighbor should be added to open list
def not_in_expanded(neighborCube, e):
    if str(hash(str(neighborCube))) in e:
        return False
    else:
        return True
