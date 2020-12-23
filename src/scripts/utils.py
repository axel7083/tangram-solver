import json
import math
from random import uniform
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from src.scripts import PolygonUtils


def margin_error(ref, value):
    """ Compute margin error % """

    if ref == 0:
        return abs(value)
    return (abs(value - ref) / ref) * 100


def divide_coords(coords, value):
    """ Divides by value all coordinates"""

    output = []
    if coords:
        for coord in coords:
            output.append(coord / value)

        return output


def random_float(_type, canvas_side):
    """ Returns a random float depending on the polygon type """

    if _type == "MT":
        return uniform(0, canvas_side - 100 * math.sqrt(2)), uniform(0, canvas_side - 100 * math.sqrt(2))
    elif _type == "ST" or _type == "S":
        return uniform(0, canvas_side - 100), uniform(0, canvas_side - 100)
    elif _type == "BT":
        return uniform(0, canvas_side - 200), uniform(0, canvas_side - 200)
    elif _type == "P":
        return uniform(0, canvas_side - 212.13), uniform(0, canvas_side - 212.13)


def find_nearest(shapes, x_pos, y_pos):
    """ find nearest shapes among the others """
    for shape in shapes:
        for x2, y2 in shape:
            if distance([x_pos, y_pos], [x2, y2]) < 1 / 100:
                return [x2, y2]
    return [x_pos, y_pos]


def distance(point_a, point_b):
    """ Returns the euclidean distance between two points if they exist"""

    if point_a and point_b:
        return math.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)
    else:
        return -1


def is_nearby(moving_figure, drawing_place, magnet_slider):
    """ Returns the closest point to one of moving figure points if in range """

    figures = drawing_place.find_all()  # retrieves all canvas polygons IDs

    coords_figures = []
    for id_ in figures:
        if id_ != moving_figure:
            coords_figures.append(drawing_place.coords(id_))

    moving_coords = drawing_place.coords(moving_figure)  # retrieves moving polygon coordinates
    size = len(moving_coords)
    size2 = len(coords_figures)
    temp = []
    k = 0

    while k <= size:
        temp = get_xy_head(moving_coords[k:])  # takes two first coord of movingCoords list from index k
        k = k + 2
        j = 0
        while j <= size2:
            j = j + 1
            for fig in coords_figures:
                fix = fig
                l = 0
                while l < len(fig):
                    l = l + 2
                    cut = get_xy_head(fix)
                    fix = fix[2:]
                    # checks if current point 'cut' is close enough to the moving figure point
                    if distance(temp, cut) <= magnet_slider.get() and distance(temp, cut) != -1:
                        return temp, cut


def get_xy_head(_list):
    """ Returns the two first element of a list """

    temp = []
    if _list:
        for item in _list:
            temp.append(item)
            if len(temp) == 2:
                return temp


def round_coords(coords):
    """ rounds a list of coords """
    output = []
    for coord in coords:
        output.append(round(coord))

    return output


def draw_node(shapes, state, ref):
    """ Function to show results using matplotlib """
    plt.figure()

    multipolygon = []
    if not isinstance(ref, Polygon):
        multipolygon = list(ref)
    else:
        multipolygon = [ref]

    # Convert check multipolygon and convert it into list of polygon
    for sub_ref in multipolygon:
        x_coords, y_coords = sub_ref.exterior.xy
        plt.plot(x_coords, y_coords)

    for i, shape in enumerate(state):
        polygon = PolygonUtils.get_shape_polygon_by_index(shapes, i, shape[0], shape[1], shape[2], shape[3])
        x_coords, y_coords = polygon.exterior.xy

        plt.plot(x_coords, y_coords)

    plt.gca().set_aspect('equal', 'datalim')
    plt.gca().invert_yaxis()
    plt.show()  # if you need...

    return


def load_prefabs():
    """ We avoid hardcoding data so we load it from storage """
    file = open('../assets/prefabs.json',)
    data = json.load(file)
    return data


def tuple_to_list(_tuple):
    """ Returns the list version of the tuple sent """
    return list(_tuple)


def random_color():
    import random
    return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
