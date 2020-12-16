import math
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from random import uniform


# Compute margin error %
def margin_error(ref, value):
    if ref == 0:
        return abs(value)
    return (abs(value - ref) / ref) * 100


# Center a polygon to one of its position
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


# From one origin point the 4 coordinates of the parallelogram
def get_parallelogram_points(x, y, rotation, size):
    if rotation <= 3:
        return [[x, y],
                rotate_by(x, y, x+size, y+size, rotation),
                rotate_by(x, y, x+size, y+3*size , rotation),
                rotate_by(x, y, x, y+2*size , rotation)]
    # flip parallelogram
    else:
        return [[x, y],
                rotate_by(x, y, x-size, y+size, rotation),
                rotate_by(x, y, x-size, y+3*size, rotation),
                rotate_by(x, y, x, y+2*size, rotation)]


# Function which evaluate how good the shapes overlap the reference
def fit_function(state, ref):
    polygons = Polygon()
    for i, shape in enumerate(state):
        # polygons = cascaded_union([polygons, Polygon(get_triangle_points(shape[0], shape[1], shape[2]))])
        polygons = cascaded_union([polygons, get_shape_polygon_by_index(i, shape[0], shape[1], shape[2])])

    return ref.difference(polygons)


# Get polygon depending on the
def get_shape_polygon_by_index(shapes, index, x, y, r, point_index):

    offset = 0.005
    unit = 1
    side = math.sqrt(unit * 2)

    if shapes[index] == "bt":
        return center_index(
            Polygon(get_triangle_points(x, y, r, unit * 2 - offset)),
            point_index
        )
    elif shapes[index] == "p":
        return center_index(
            Polygon(get_parallelogram_points(x, y, r, side / 2 - offset)),
            point_index
        )
    elif shapes[index] == "mt":
        return center_index(
            Polygon(get_triangle_points(x, y, r, side - offset)),
            point_index
        )
    elif shapes[index] == "s":
        return center_index(
            Polygon(get_square_points(x, y, r, unit - offset)),
            point_index
        )
    elif shapes[index] == "st":
        return center_index(
            Polygon(get_triangle_points(x, y, r, unit - offset)),
            point_index
        )


# Get the number of corner per index
def get_corner_count_by_index(shapes, index):
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


# Number of rotation available per shape
def get_rot_by_index(shapes, index):
    if shapes[index] == "s":
        return 2
    else:
        return 8


# Merge a list of polygons into one
def merge(polygons):
    return cascaded_union(polygons)


def divide_coords(coords, value):
    """ Divides by value all coordinates"""

    output = []
    if coords:
        for coord in coords:
            output.append(coord/value)

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


def find_nearest(shapes, x, y):

    for shape in shapes:
        for x2, y2 in shape:
            if distance([x, y], [x2, y2]) < 1/100:
                return [x2, y2]
    return [x, y]


def distance(p1, p2):
    """ Returns the euclidean distance between two points if they exist"""

    if p1 and p2:
        return math.sqrt((p2[0] - p1[0])**2+(p2[1] - p1[1])**2)
    else:
        return -1


def is_nearby(movingFigure, drawing_place, magnetSlider):
    """ Returns the closest point to one of moving figure points if in range """

    figures = drawing_place.find_all()  # retrieves all canvas polygons IDs

    coordsFigures = []
    for id in figures:
        if id != movingFigure:
            coordsFigures.append(drawing_place.coords(id))

    movingCoords = drawing_place.coords(movingFigure)  # retrieves moving polygon coordinates
    size = len(movingCoords)
    size2 = len(coordsFigures)
    temp = []
    k = 0

    while k <= size:
        temp = get_xy_head(movingCoords[k:])  # takes two first coord of movingCoords list from index k
        k = k+2
        j = 0
        while j <= size2:
            j = j + 1
            for fig in coordsFigures:
                fix = fig
                l = 0
                while l < len(fig):
                    l = l+2
                    cut = get_xy_head(fix)
                    fix = fix[2:]
                    # checks if current point 'cut' is close enough to the moving figure point
                    if distance(temp, cut) <= magnetSlider.get() and distance(temp, cut) != -1:
                        return temp, cut


def get_xy_head(_list):
    """ Returns the two first element of a list """

    temp = []
    if _list:
        for item in _list:
            temp.append(item)
            if len(temp) == 2:
                return temp
