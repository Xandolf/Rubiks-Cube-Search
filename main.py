import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as c
import cube as cbe

# TODO {
#   Searches
#   ... Breadth First
#   ... Depth First
#   ... A*
#   Heuristics
#   ... safe_log2
#   ... (3-D?) Manhattan Distance
#   ... incorrect tiles
#   Analysis
#   ... Record nodes expanded for each search as N grows larger
#   ... display results in graphs
#   ... Final Documentations
#  }


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cube = cbe.init_cube(3)
    print(cbe.get_entropy(cube))
    print(cbe.get_gini(cube))
    print(cbe.get_chaos(cube))

    rand_moves = cbe.generate_random_moves(cube, 300)
    for move in rand_moves:
        cube = cbe.get_action_result(cube, move)

    print(cbe.get_entropy(cube))
    print(cbe.get_gini(cube))
    print(cbe.get_chaos(cube))

    inv_moves = cbe.invert_moves(rand_moves)
    for move in inv_moves:
        cube = cbe.get_action_result(cube, move)

    print(cbe.get_entropy(cube))
    print(cbe.get_gini(cube))
    print(cbe.get_chaos(cube))


    print(cbe.is_goal_state(cube))

    print("\n---------\n")
    # print(cube)
