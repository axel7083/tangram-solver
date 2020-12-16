import math
from tkinter import *
from math import *
from tkinter import messagebox

import numpy
from shapely.geometry import Polygon
from TangramSolver import TangramSolver


# Constants
import utils

MAX_MED_TRIANGLE = 2
MAX_SM_TRIANGLE = 4
MAX_SQUARE = 3
MAX_BIG_TRIANGLE = 2
MAX_PARALLELOGRAM = 8
CANVAS_SIDE = 700


class CanvasPolygon:

    # Constructor
    def __init__(self, coords, color, tag, canvas):
        self.coords = coords
        self.color = color
        self.move = False
        self.tag = tag
        self.canvas = canvas

        self.id = canvas.create_polygon(self.coords, fill=self.color, tags=self.tag)

        canvas.tag_bind(self.id, '<Button-1>', self.start_movement)
        canvas.tag_bind(self.id, '<Motion>', self.movement)
        canvas.tag_bind(self.id, '<ButtonRelease-1>', self.stop_movement)
        canvas.tag_bind(self.id, '<Button-3>', self.rotate)

    def get_coords(self):
        """ Returns polygon's coordinates """

        return self.coords

    def set_coords(self, coords):
        """ Sets polygon's coordinates """

        self.coords = coords

    def delete(self):
        """ Deletes specified polygon """

        self.canvas.delete(self.id)

    def start_movement(self, event):
        """ Modify move attribute and converts mouse coord to canvas coord """

        self.move = True

        # Translate mouse coordinates to canvas coordinate
        self.initi_x = self.canvas.canvasx(event.x)
        self.initi_y = self.canvas.canvasy(event.y)

    def movement(self, event):
        """ Moves polygon on the canvas """

        if self.move:

            end_x = self.canvas.canvasx(event.x)  # Translate mouse x screen coordinate to canvas coordinate
            end_y = self.canvas.canvasy(event.y)  # Translate mouse y screen coordinate to canvas coordinate

            deltax = end_x - self.initi_x  # Find the difference
            deltay = end_y - self.initi_y  # Find the difference

            self.new_position(deltax, deltay)

            self.initi_x = end_x  # Update previous current with new location
            self.initi_y = end_y

            self.canvas.move(self.id, deltax, deltay)  # Move object

    def stop_movement(self, event):
        """ Updates move attribute and sticks the moving polygon to nearby polygon """

        yesCase = utils.is_nearby(self.id, drawing_place, magnetSlider)
        if yesCase:
            self.delete()
            CanvasPolygon(replace(tuple_to_list(self.coords), tuple_to_list(yesCase)), self.color, self.tag, self.canvas)

        self.move = False

    def new_position(self, deltax, deltay):
        """ Updates the coords of a polygon given the coordinates of the translation """

        coord = tuple_to_list(self.coords)  # Retrieve object points coordinates
        # old_coord = list(coord)  # Tuple to List
        c = []  # New coords
        i = 0  # Cursor on old_coord
        for coordinates in coord:

            # check if index of coordinates in range of i and len(old_coord) in old_coord is pair (x coord)
            if (coord.index(coordinates, i, len(coord)) % 2) == 0:
                c.append(coordinates + deltax)
            else:  # index's impair => y-coord
                c.append(coordinates + deltay)
            i += 1

        coord2 = tuple(c)  # List to Tuple
        self.set_coords(coord2)

    def rotate(self, event):
        """ Rotate polygon the given angle about its center. """

        theta = radians(45)  # Convert angle to radians
        cosang, sinang = cos(theta), sin(theta)
        new_points, a, b = [], [], []
        i, j, cx, cy = 0, 0, 0.0, 0.0
        points = self.get_coords()

        for p in points:
            if (points.index(p, i, len(points)) % 2) == 0:
                a.append(p)
            else:
                b.append(p)
            i += 1

        # Takes center point as the first point of the Polygon to use it as pivot
        cx = points[0]
        cy = points[1]

        # find new x_y for each point
        for x, y in zip(a, b):
            tx, ty = x - cx, y - cy
            new_x = (tx * cosang + ty * sinang) + cx
            new_y = (-tx * sinang + ty * cosang) + cy
            new_points.append(new_x)
            new_points.append(new_y)

        self.delete()
        new_polygon = CanvasPolygon(new_points, self.color, self.tag, self.canvas)

    def print_figure_coords(figure):
        print(figure.coords)


def replace(original, change):
    """ Calculates new polygon points after a matching point has been found in isNearby() """

    if original and change:
        diff = [change[0][0] - change[1][0],change[0][1] - change[1][1]]
        new = []
        placed = 0
        for i,p in enumerate(original):
            if p == change[0][0]:
                if original[i+1] == change[0][1]:
                    new.append(change[1][0])
                    new.append(change[1][1])
                    placed = i+2
                else:
                    new.append(p-diff[0]) if i%2 == 0 else new.append(p-diff[1])
            else:
                new.append(p-diff[0]) if i%2 == 0 else new.append(p-diff[1])

        new.pop(placed)
        return new


def tuple_to_list(tuple):
    """ Returns the list version of the tuple sent """

    return list(tuple)


def get_settings_by_type(_type, x, y):

    unit = 100
    side = math.sqrt(2)*100

    if _type == "bt":
        return MAX_BIG_TRIANGLE, numpy.array(utils.get_triangle_points(x, y, 0, unit * 2)).flatten().tolist(), "green"
    elif _type == "p":
        return MAX_PARALLELOGRAM, numpy.array(utils.get_parallelogram_points(x, y, 0, side / 2)).flatten().tolist(), "indian red"
    elif _type == "mt":
        return MAX_MED_TRIANGLE, numpy.array(utils.get_triangle_points(x, y, 0, side)).flatten().tolist(), "red"
    elif _type == "s":
        return MAX_SQUARE, numpy.array(utils.get_square_points(x, y, 0, unit)).flatten().tolist(), "pink"
    elif _type == "st":
        return MAX_SM_TRIANGLE, numpy.array(utils.get_triangle_points(x, y, 0, unit)).flatten().tolist(), "orange"


def polygon_action(_type, label, action):
    """ Add or Delete polygons of the canvas depending on what button the user clicked on """

    if action == "add":
        create_polygon(_type, label)
    elif action == "del":
        delete_polygon(_type, label)


def update_count_label(label, action):
    """ Updates the count of a label """

    str_count = label["text"]
    count = int(str_count)

    if action == "+":
        label["text"] = str(count + 1)
    elif action == "-":
        label["text"] = str(count - 1)
    elif action == "reset":
        reset_canvas()


def label_value(label):
    """ Converts label text to int """
    return int(label["text"])


def create_polygon(_type, label):
    x = CANVAS_SIDE / 2
    y = CANVAS_SIDE / 2
    _max, coords, color = get_settings_by_type(_type, x, y)

    if label_value(label) + 1 <= _max and label_value(label) >= 0:
        # Creating a new Polygon
        CanvasPolygon(coords, color, _type, drawing_place)
        update_count_label(label, "+")
    else:
        messagebox.showerror("Maximum reach", "You've reached the maximum amount of this item.")


def delete_polygon(_type, label):
    """ Deletes polygon that has for tag : 'type' """

    if label_value(label) > 0:

        figures = drawing_place.find_withtag(_type)
        _len = len(figures)
        if _len == 1:
            drawing_place.delete(_type)

        elif _len > 1:
            result = tuple_to_list(figures)
            drawing_place.delete(result[_len-1])

        update_count_label(label, "-")
    else:
        messagebox.showerror("Minimum reach", "You've reached the minimum amount of this item.")


def transformCoord():
    """ Sends polygon's coordinates to AI """

    figures = drawing_place.find_all()
    coords = []
    tags = []
    if len(figures) >= 1:
        for fig in figures:
            tags.append(drawing_place.gettags(fig))
            coords.append(utils.divide_coords(tuple_to_list(drawing_place.coords(fig)), 100))

        types = getTypeofPolygons()

        coordinates = []
        for shape in coords:
            poly = []
            for i in range(int(len(shape) / 2)):
                poly.append(utils.find_nearest(coordinates, round(shape[i * 2], 3), round(shape[i * 2 + 1], 3)))
                # poly.append([shape[i * 2], shape[i * 2 + 1]])

            coordinates.append(poly)

        print(coordinates)

        polygons = []
        for shape in coordinates:
            polygons.append(Polygon(shape))

        # Output can be polygon OR multipolygon
        output = utils.merge(polygons)

        multipolygon = []
        if not isinstance(output, Polygon):
            print("Polygon")
            multipolygon = list(output)
        else:
            multipolygon = [output]
            print("Multipolygon")

        # Convert check multipolygon and convert it into list of polygon
        for sub_ref in multipolygon:

            print(len(sub_ref.exterior.xy[0]))
            xy = []
            for i in range(len(sub_ref.exterior.xy[0])):
                xy.append(sub_ref.exterior.xy[0][i] * 100)
                xy.append(sub_ref.exterior.xy[1][i] * 100)

            CanvasPolygon(xy, 'black', "origin", drawing_place)
            print(xy)

        print(types)

        solve(output, types)
    else:
        messagebox.showerror("No polygons on canvas", "Please add at least one polygon before testing our AI")


def solve(original, types):

    tangram_solver = TangramSolver(original, types)
    tangram_solver.execute()


def getTypeofPolygons():
    """ Gets canvas polygons types """

    types = []
    for label in labels:
        for i in range(0, int(label['text'])):
            types.append(label.tag)

    return types


def reset_canvas():
    """ Resets canvas and labels when user clicks on Reset Button """

    figures = drawing_place.find_all()
    for fig in figures:
        drawing_place.delete(fig)

    for label in labels:
        label["text"] = "0"

def getPolygonsLimits():
    """ Updates at initialization, labels for polygons limits """

    labelMax1["text"] = str(MAX_MED_TRIANGLE)
    labelMax2["text"] = str(MAX_SM_TRIANGLE)
    labelMax3["text"] = str(MAX_SQUARE)
    labelMax4["text"] = str(MAX_BIG_TRIANGLE)
    labelMax5["text"] = str(MAX_PARALLELOGRAM)

def mode_validate_button(currState):
    """ Disables validate button to let AI work """

    if currState == "disabled":
        btn_validate['state'] = "normal"
    else:
        btn_validate['state'] = "disabled"


""" Tkinter objets definitions """

# -- Window definition
window = Tk()
window.title("Tangram")
window.iconbitmap("img/tangram_logo.ico")
window.geometry("1260x800")
window.scale = 1

labels = []  # Keep track of all polygon's number labels

# -- Canvas & Frame definition
drawing_place = Canvas(window, width=700, height=700, bg="grey")
drawing_place.pack(pady=20, padx=0)

numPolygonsFrame = LabelFrame(window, text="Number of Polygons", padx=20, pady=10, labelanchor="nw")
numPolygonsFrame.place(x=70, y=50)

magnetFrame = LabelFrame(window, text="Magnetization distance", padx=10, pady=5, labelanchor="nw")
magnetFrame.place(x=40, y=250)

commandFrame = LabelFrame(window, text="Actions", padx=5, pady=5, labelanchor="nw")
commandFrame.place(x=70, y=350)

polygonsLimitsFrame = LabelFrame(window, text="Polygon's limits", padx=5, pady=5, labelanchor="nw")
polygonsLimitsFrame.place(x=70, y=500)


# Polygons images next to + _ - buttons
imgMT = PhotoImage(file='img/mt.png')
button = Button(numPolygonsFrame, image=imgMT)
button.grid(row=1, column=4)

imgST = PhotoImage(file='img/st.png')
button = Button(numPolygonsFrame, image=imgST)
button.grid(row=2, column=4)

imgSQ = PhotoImage(file='img/sq.png')
button = Button(numPolygonsFrame, image=imgSQ)
button.grid(row=3, column=4)

imgBT = PhotoImage(file='img/bt.png')
button = Button(numPolygonsFrame, image=imgBT)
button.grid(row=4, column=4)

imgP = PhotoImage(file='img/p.png')
button = Button(numPolygonsFrame, image=imgP)
button.grid(row=5, column=4)

# Polygons images + maximum limits
max1 = Button(polygonsLimitsFrame, image=imgMT)
labelMax1 = Label(polygonsLimitsFrame, text=0)
max2 = Button(polygonsLimitsFrame, image=imgST)
labelMax2 = Label(polygonsLimitsFrame, text=0)
max3 = Button(polygonsLimitsFrame, image=imgSQ)
labelMax3 = Label(polygonsLimitsFrame, text=0)
max4 = Button(polygonsLimitsFrame, image=imgBT)
labelMax4 = Label(polygonsLimitsFrame, text=0)
max5 = Button(polygonsLimitsFrame, image=imgP)
labelMax5 = Label(polygonsLimitsFrame, text=0)

max1.grid(row=1, column=1)
max2.grid(row=2, column=1)
max3.grid(row=3, column=1)
max4.grid(row=4, column=1)
max5.grid(row=5, column=1)
labelMax1.grid(row=1, column=2)
labelMax2.grid(row=2, column=2)
labelMax3.grid(row=3, column=2)
labelMax4.grid(row=4, column=2)
labelMax5.grid(row=5, column=2)

# + or - buttons
plusButton4 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [polygon_action("bt", bigTriangleLabel, "add")])
bigTriangleLabel = Label(numPolygonsFrame, text=0, fg="dark green")
bigTriangleLabel.tag = 'bt'
labels.append(bigTriangleLabel)
minusButton4 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [polygon_action("bt", bigTriangleLabel, "del")])

plusButton5 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [polygon_action("p", parallelogramLabel, "add")])
parallelogramLabel = Label(numPolygonsFrame, text=0, fg="dark green")
parallelogramLabel.tag = 'p'
labels.append(parallelogramLabel)
minusButton5 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [polygon_action("p", parallelogramLabel, "del")])

plusButton1 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [polygon_action("mt", medTriangleLabel, "add")])
medTriangleLabel = Label(numPolygonsFrame, text=0, fg="dark green")
medTriangleLabel.tag = 'mt'
labels.append(medTriangleLabel)
minusButton1 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [polygon_action("mt", medTriangleLabel, "del")])

plusButton3 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [polygon_action("s", squareLabel, "add")])
squareLabel = Label(numPolygonsFrame, text=0, fg="dark green")
squareLabel.tag = 's'
labels.append(squareLabel)
minusButton3 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [polygon_action("s", squareLabel, "del")])

plusButton2 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [polygon_action("st", smallTriangleLabel, "add")])
smallTriangleLabel = Label(numPolygonsFrame, text=0, fg="dark green")
smallTriangleLabel.tag = 'st'
labels.append(smallTriangleLabel)
minusButton2 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [polygon_action("st", smallTriangleLabel, "del")])






# + or - buttons placement

plusButton1.grid(row=1, column=1)
medTriangleLabel.grid(row=1, column=2)
minusButton1.grid(row=1, column=3)

plusButton2.grid(row=2, column=1)
smallTriangleLabel.grid(row=2, column=2)
minusButton2.grid(row=2, column=3)

plusButton3.grid(row=3, column=1)
squareLabel.grid(row=3, column=2)
minusButton3.grid(row=3, column=3)

plusButton4.grid(row=4, column=1)
bigTriangleLabel.grid(row=4, column=2)
minusButton4.grid(row=4, column=3)

plusButton5.grid(row=5, column=1)
parallelogramLabel.grid(row=5, column=2)
minusButton5.grid(row=5, column=3)

# Buttons and Slider placement
magnetSlider = Scale(magnetFrame, from_=5, to=100, length=150, resolution=5, orient=HORIZONTAL, width=20)
magnetSlider.grid(row=0, column=0)

btn_validate = Button(commandFrame, text="Validate", command=lambda:[transformCoord()])
btn_validate.grid(row=1, column=1)

btn_reset = Button(commandFrame, text="  Reset  ", command=lambda:[reset_canvas()])
btn_reset.grid(row=1, column=2)

# Updates polygons limits with program constants
getPolygonsLimits()

# Run the main loop:
window.mainloop()
