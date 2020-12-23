import math
import numpy
from src.scripts import PolygonUtils


# Constants
MAX_MED_TRIANGLE = 2
MAX_SM_TRIANGLE = 4
MAX_SQUARE = 3
MAX_BIG_TRIANGLE = 2
MAX_PARALLELOGRAM = 4
CANVAS_SIDE = 700


def enable_validate_button(btn_validate, enable):
    """ Disables validate button to let AI work """

    if enable:
        btn_validate['state'] = "normal"
    else:
        btn_validate['state'] = "disabled"


def reset_canvas(drawing_place, labels):
    """ Resets canvas and labels when user clicks on Reset Button """

    figures = drawing_place.find_all()
    for fig in figures:
        drawing_place.delete(fig)

    for label in labels:
        label["text"] = "0"


def update_count_label(label, action, drawing_place=None, labels=None):
    """ Updates the count of a label """

    str_count = label["text"]
    count = int(str_count)

    if action == "+":
        label["text"] = str(count + 1)
    elif action == "-":
        label["text"] = str(count - 1)
    elif action == "reset":
        reset_canvas(drawing_place, labels)


def replace(original, change):
    """ Calculates new polygon points after a matching point has been found in isNearby() """

    if original and change:
        diff = [change[0][0] - change[1][0], change[0][1] - change[1][1]]
        new = []
        placed = 0
        for i, p in enumerate(original):
            if p == change[0][0]:
                if original[i + 1]:  # prevents a list index out of range error from happening
                    if original[i + 1] == change[0][1]:
                        new.append(change[1][0])
                        new.append(change[1][1])
                        placed = i + 2
                    else:
                        new.append(p - diff[0]) if i % 2 == 0 else new.append(p - diff[1])
            else:
                new.append(p - diff[0]) if i % 2 == 0 else new.append(p - diff[1])

        new.pop(placed)
        return new


def get_settings_by_type(_type, x_pos, y_pos):
    unit = 100
    side = round(math.sqrt(2) * 100)

    if _type == "bt":
        return MAX_BIG_TRIANGLE, numpy.array(
            PolygonUtils.get_triangle_points(x_pos, y_pos, 0, unit * 2)).flatten().tolist()
    elif _type == "p":
        return MAX_PARALLELOGRAM, numpy.array(
            PolygonUtils.get_parallelogram_points(x_pos, y_pos, 0, side / 2)).flatten().tolist()
    elif _type == "mt":
        return MAX_MED_TRIANGLE, numpy.array(PolygonUtils.get_triangle_points(x_pos, y_pos, 0, side)).flatten().tolist()
    elif _type == "s":
        return MAX_SQUARE, numpy.array(PolygonUtils.get_square_points(x_pos, y_pos, 0, unit)).flatten().tolist()
    elif _type == "st":
        return MAX_SM_TRIANGLE, numpy.array(PolygonUtils.get_triangle_points(x_pos, y_pos, 0, unit)).flatten().tolist()


def label_value(label):
    """ Converts label text to int """
    return int(label["text"])
