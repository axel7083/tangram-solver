import math
from shapely.geometry import Polygon
from shapely.ops import cascaded_union


def center_index(shape, index):
    """ Center a polygon to one of its position """

    if index == 0:
        return shape

    x_coords, y_coords = shape.exterior.xy
    move = [x_coords[0] - x_coords[index], y_coords[0] - y_coords[index]]
    coordinates = []

    for i in range(len(x_coords)):
        coordinates.append([x_coords[i] + move[0], y_coords[i] + move[1]])

    return Polygon(coordinates)


def rotate_by(x_pivot, y_pivot, x_pos, y_pos, angle):
    """ Rotate a point (x,y) around (cx, cy) """

    angle = (math.pi * angle) / 4
    return [math.cos(angle) * (x_pos - x_pivot) - math.sin(angle) * (y_pos - y_pivot) + x_pivot,
            math.sin(angle) * (x_pos - x_pivot) + math.cos(angle) * (y_pos - y_pivot) + y_pivot]


def get_triangle_points(x_pos, y_pos, rotation, size):
    """ From one origin point get 3 coordinates of triangles """

    return [[x_pos, y_pos], rotate_by(x_pos, y_pos, x_pos + size, y_pos, rotation), rotate_by(x_pos, y_pos, x_pos,
                                                                                              y_pos + size, rotation)]


def get_square_points(x_pos, y_pos, rotation, size):
    """ From one origin point get the 4 coordinates of the square """

    rotation %= 2
    return [[x_pos, y_pos],
            rotate_by(x_pos, y_pos, x_pos + size, y_pos, rotation),
            rotate_by(x_pos, y_pos, x_pos + size, y_pos + size, rotation),
            rotate_by(x_pos, y_pos, x_pos, y_pos + size, rotation)]


def get_parallelogram_points(x_pos, y_pos, rotation, size):
    """ From one origin point the 4 coordinates of the parallelogram """

    if rotation <= 3:
        return [[x_pos, y_pos],
                rotate_by(x_pos, y_pos, x_pos + size, y_pos + size, rotation),
                rotate_by(x_pos, y_pos, x_pos + size, y_pos + 3 * size, rotation),
                rotate_by(x_pos, y_pos, x_pos, y_pos + 2 * size, rotation)]
    # flip parallelogram
    else:
        return [[x_pos, y_pos],
                rotate_by(x_pos, y_pos, x_pos - size, y_pos + size, rotation),
                rotate_by(x_pos, y_pos, x_pos - size, y_pos + 3 * size, rotation),
                rotate_by(x_pos, y_pos, x_pos, y_pos + 2 * size, rotation)]


def fit_function(types, state, ref):
    """ Function which evaluate how good the shapes overlap the reference """

    polygons = Polygon()
    for i, shape in enumerate(state):
        polygons = cascaded_union([
            polygons,
            get_shape_polygon_by_index(types, i, shape[0], shape[1], shape[2], shape[3])
        ])

    return ref.difference(polygons)


def get_shape_polygon_by_index(shapes, index, x_pos, y_pos, rotation, point_index, offset=0.005):
    """" Get polygon depending on the """
    unit = 1
    side = math.sqrt(unit * 2)

    if shapes[index] == "bt":
        return center_index(
            Polygon(get_triangle_points(x_pos, y_pos, rotation, unit * 2 - offset)),
            point_index
        )
    elif shapes[index] == "p":
        return center_index(
            Polygon(get_parallelogram_points(x_pos, y_pos, rotation, side / 2 - offset)),
            point_index
        )
    elif shapes[index] == "mt":
        return center_index(
            Polygon(get_triangle_points(x_pos, y_pos, rotation, side - offset)),
            point_index
        )
    elif shapes[index] == "s":
        return center_index(
            Polygon(get_square_points(x_pos, y_pos, rotation, unit - offset)),
            point_index
        )
    elif shapes[index] == "st":
        return center_index(
            Polygon(get_triangle_points(x_pos, y_pos, rotation, unit - offset)),
            point_index
        )


def get_corner_count_by_index(shapes, index):
    """ Get the number of corner per index """
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


def get_rot_by_index(shapes, index):
    """ Number of rotation available per shape """
    if shapes[index] == "s":
        return 2
    elif shapes[index] == "p":
        return 4
    else:
        return 8


def merge(polygons):
    """ Merge a list of polygons into one """
    return cascaded_union(polygons)
