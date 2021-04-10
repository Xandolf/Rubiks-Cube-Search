import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as c
import cube as cbe


# TODO {
#   create goal state test
#   Test Rotations
#   ... X-axis
#   ... Y-axis
#   ... Z-axis
#   Searches
#   ... Breadth First
#   ... Depth First
#   ... A*
#   Heuristics
#   ... Entropy
#   ... Gini
#   ... (3-D?) Manhattan Distance
#   ... incorrect tiles
#   Analysis
#   ... Record nodes expanded for each search as N grows larger
#   ... display results in graphs
#   ... Final Documentations
# }



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cube = cbe.init_cube(3)
    actions = cbe.getAllActions(cube)


    for i in range(10):
        cube = cbe.z_rotation(cube, 1, 1)
        cube = cbe.z_rotation(cube, 2, 1)
        cube = cbe.y_rotation(cube, 1, 1)
        cube = cbe.x_rotation(np.copy(cube), 0, -1)

    for i in range (10):
        cube = cbe.x_rotation(np.copy(cube), 0, 1)
        cube = cbe.y_rotation(cube, 1, -1)
        cube = cbe.z_rotation(cube, 2, -1)
        cube = cbe.z_rotation(cube, 1, -1)


    # cbe.print_cube (cube, annotate=True)
    print(cbe.is_goal_state(cube))

    print("\n---------\n")
    # print(cube)

