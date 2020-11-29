import numpy as np
import matplotlib.pyplot as plt
import math
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import cascaded_union
import random
import copy

# Global variables
global_size = 1
width = 20
height = 20
shapes = ["bt", "bt", "p", "mt", "s", "st", "st"]  # Final order
# shapes = [""]  # Final order


def margin_error(ref, value):
    if ref == 0:
        return abs(value)
    # print(str(ref) + " vs " + str(value))
    return (abs(value - ref) / ref) * 100


def center_index(shape, index):
    if index == 0:
        return shape

    xs, ys = shape.exterior.xy
    move = [xs[0] - xs[index], ys[0] - ys[index]]
    coordinates = []

    xs, ys = shape.exterior.xy
    for i in range(len(xs)):
        coordinates.append([xs[i] + move[0], ys[i] + move[1]])

    return Polygon(coordinates)


# Rotate a point (x,y) around (cx, cy)
def rotate_by(cx, cy, x, y, angle):
    angle = (math.pi * angle) / 4
    return [math.cos(angle) * (x - cx) - math.sin(angle) * (y - cy) + cx,
            math.sin(angle) * (x - cx) + math.cos(angle) * (y - cy) + cy]


# From one origin point get 3 coordinates of triangles
def get_triangle_points(x, y, rotation, size):
    return [[x, y], rotate_by(x, y, x + size, y, rotation), rotate_by(x, y, x, y + size, rotation)]


# From one origin point get the 4 coordinates of the square
def get_square_points(x, y, rotation, size):
    rotation %= 2
    return [[x, y],
            rotate_by(x, y, x + size, y, rotation),
            rotate_by(x, y, x + size, y + size, rotation),
            rotate_by(x, y, x, y + size, rotation)]


def get_parallelogram_points(x, y, rotation, size):
    return [[x, y],
            rotate_by(x, y, x + size, y + size, rotation),
            rotate_by(x, y, x + size, y + 3 * size, rotation),
            rotate_by(x, y, x, y + 2 * size, rotation)]


# Function which evaluate how good the shapes overlap the reference
def fit_function(state, ref):
    polygons = Polygon()
    for i, shape in enumerate(state):
        # polygons = cascaded_union([polygons, Polygon(get_triangle_points(shape[0], shape[1], shape[2]))])
        polygons = cascaded_union([polygons, get_shape_polygon_by_index(i, shape[0], shape[1], shape[2])])

    return ref.difference(polygons)


# "Debug" function to represent a state
def draw_node(state, ref):
    plt.figure()

    multipolygon = []
    if not isinstance(ref, Polygon):
        multipolygon = list(ref)
    else:
        multipolygon = [ref]

    # Convert check multipolygon and convert it into list of polygon
    for sub_ref in multipolygon:
        xs, ys = sub_ref.exterior.xy
        plt.plot(xs, ys)

    for i, shape in enumerate(state):
        polygon = get_shape_polygon_by_index(i, shape[0], shape[1], shape[2], shape[3])

        xs, ys = polygon.exterior.xy
        plt.plot(xs, ys)


def get_corner_count_by_index(index):
    if shapes[index] == "bt":
        return 3
    elif shapes[index] == "p":
        return 3
    elif shapes[index] == "mt":
        return 3
    elif shapes[index] == "s":
        return 4
    elif shapes[index] == "st":
        return 3


def get_rot_by_index(index):
    if shapes[index] == "s":
        return 2
    else:
        return 8


def get_shape_polygon_by_index(index, x, y, r, point_index):

    offset = 0.001
    unit = 1
    side = math.sqrt(unit*2)

    if shapes[index] == "bt":
        return center_index(
            Polygon(get_triangle_points(x, y, r, unit*2-offset)),
            point_index
        )
    elif shapes[index] == "p":
        return center_index(
            Polygon(get_parallelogram_points(x, y, r, side/2-offset)),
            point_index
        )
    elif shapes[index] == "mt":
        return center_index(
            Polygon(get_triangle_points(x, y, r, side-offset)),
            point_index
        )
    elif shapes[index] == "s":
        return center_index(
            Polygon(get_square_points(x, y, r, unit-offset)),
            point_index
        )
    elif shapes[index] == "st":
        return center_index(
            Polygon(get_triangle_points(x, y, r, unit-offset)),
            point_index
        )


def corner_explore(ref, shape_index, state):
    multipolygon = []
    if not isinstance(ref, Polygon):
        multipolygon = list(ref)
    else:
        multipolygon = [ref]

    # Convert check multipolygon and convert it into list of polygon

    for sub_ref in multipolygon:
        for i in range(len(sub_ref.exterior.xy[0])):

            x = sub_ref.exterior.xy[0][i]
            y = sub_ref.exterior.xy[1][i]

            for r in range(get_rot_by_index(shape_index)):

                for point_index in range(get_corner_count_by_index(shape_index)):

                    new_state = copy.deepcopy(state)
                    new_state.append([x, y, r, point_index])
                    poly = get_shape_polygon_by_index(shape_index, x, y, r, point_index)

                    # new_ref = fit_function(state, ref)
                    diff = ref.difference(poly)

                    if margin_error(diff.area, ref.area - poly.area) < 0.5:
                        # if int(ref.area - poly.area) == int(diff.area):
                        # print("We found a shape which fit ")
                        if shape_index == len(shapes) - 1:
                            print("Finish")
                            return True, new_state
                        else:

                            is_success, new_state = corner_explore(diff, shape_index + 1, new_state)
                            if is_success:
                                return True, new_state

    return False, None


# Main function
def main():
    print("[Main]")

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
    big_square = 2*global_size * math.sqrt(2)
    # original = Polygon([[0, 0], [big_square/2, big_square/2], [0, big_square], [big_square, big_square], [big_square, 0], [0, 0]])

    original = Polygon([[0, 0], [0, big_square], [big_square, big_square], [big_square, 0], [0, 0]])

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
    """

    is_success, final_shapes = corner_explore(original, 0, [])

    if is_success:
        print("Success")
        draw_node(final_shapes, original)
        plt.gca().set_aspect('equal', 'datalim')
        plt.show()  # if you need...
    else:
        print("Error")


# Launch main function
if __name__ == "__main__":
    main()
