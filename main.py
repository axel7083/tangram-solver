import math
from TangramSolver import TangramSolver
from shapely.geometry import Polygon


# Main function
def main():
    print("[Main]")

    global_size = 1
    big_square = 2 * global_size * math.sqrt(2)
    original = Polygon([[0, 0], [0, big_square], [big_square, big_square], [big_square, 0], [0, 0]])

    tangram_solver = TangramSolver(original, ["bt", "bt", "p", "mt", "s", "st", "st"])
    tangram_solver.execute()


    """
    head = Polygon([
        [2 - math.sqrt(2), 2 + math.sqrt(2)],  # D
        [2 - math.sqrt(2) + math.sqrt(2) / 2, 2 + math.sqrt(2) + math.sqrt(2) / 2],  # H
        [2 - math.sqrt(2) + math.sqrt(2) / 2, 2 + 2 * math.sqrt(2) + math.sqrt(2) / 2],  # L
        [2 - math.sqrt(2), 2 + 2 * math.sqrt(2)],  # J
        [2 - math.sqrt(2) - math.sqrt(2) / 2, 2 + 2 * math.sqrt(2) + math.sqrt(2) / 2],  # K
        [2 - math.sqrt(2) - math.sqrt(2) / 2, 2 + math.sqrt(2) + math.sqrt(2) / 2],  # I
        [2 - math.sqrt(2), 2 + math.sqrt(2)],  # D
    ])

    body = Polygon([
        [0, 0], # A
        [2, 0], # B
        [2, 2], # C
        [2 - math.sqrt(2), 2 + math.sqrt(2)], # D
        [2 - math.sqrt(2) - 1, 2 + math.sqrt(2) - 1], # F
        [2 - math.sqrt(2), 2 + math.sqrt(2) - 2], # G
        [2 - math.sqrt(2), 2 - math.sqrt(2)], # E
        [0, 0], # A
    ])

    tail = Polygon([
        [2, 0],  # B
        [3, 0],  # M
        [4, 1],  # N
        [3, 1],  # N1
        [2, 0],  # B
    ])
    original = cascaded_union([body, tail, head])
    """


    """
    draw_node([
        [0, 0, 5, 1],  # bt
        [big_square/2, big_square/2, 7, 0],  # bt
        [0, 0, 0, 0],  # p
        [0, big_square, 6, 0],  # mt
        [math.sqrt(2)/2, math.sqrt(2) + math.sqrt(2)/2, 1, 3],  # s
    ], original)
    plt.gca().set_aspect('equal', 'datalim')
    plt.show()  # if you need...
    return


    is_success, final_shapes = corner_explore(original, 0, [])

    if is_success:
        print("Success")
        draw_node(final_shapes, original)
        plt.gca().set_aspect('equal', 'datalim')
        plt.show()  # if you need...
    else:
        print("Error")
            """


# Launch main function
if __name__ == "__main__":
    main()
