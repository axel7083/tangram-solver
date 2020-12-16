from tkinter import *
from math import *
from tkinter import messagebox
from random import uniform
from shapely.geometry import Polygon
from TangramSolver import TangramSolver

# Constants
import utils

MAX_MED_TRIANGLE = 50
MAX_SM_TRIANGLE = 50
MAX_SQUARE = 50
MAX_BIG_TRIANGLE = 50
MAX_PARALLELOGRAM = 50
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

        yesCase = is_nearby(self.id)
        if yesCase:
            self.delete()
            new_polygon = CanvasPolygon(replace(tuple_to_list(self.coords), tuple_to_list(yesCase)), self.color, self.tag, self.canvas)

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


def is_nearby(movingFigure):
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
        temp = twoFirst(movingCoords[k:])  # takes two first coord of movingCoords list from index k
        k = k+2
        j = 0
        while j <= size2:
            j = j + 1
            for fig in coordsFigures:
                fix = fig
                l = 0
                while l < len(fig):
                    l = l+2
                    cut = twoFirst(fix)
                    fix = fix[2:]
                    # checks if current point 'cut' is close enough to the moving figure point
                    if euclideanDistance(temp, cut) <= magnetSlider.get() and euclideanDistance(temp, cut) != -1:
                        return temp, cut




def twoFirst(list):
    """ Returns the two first element of a list """

    temp = []
    if list:
        for item in list:
            temp.append(item)
            if(len(temp) == 2):
                return temp



def euclideanDistance(p1, p2):
    """ Returns the euclidean distance between two points if they exist"""

    if p1 and p2:
        return sqrt((p2[0] - p1[0])**2+(p2[1] - p1[1])**2)
    else:
        return -1


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


def add_delPolygon(type, label, action):
    """ Add or Delete polygons of the canvas depending on what button the user clicked on """

    if type == "MT":
        if action == "add":
            if label_value(label)+1 <= MAX_MED_TRIANGLE and label_value(label) >= 0:
                overlap, iter = True, 0
                while overlap:
                    if iter < 1000:
                        iter += 1
                        x, y = randfloatinRange(type)
                        mt3 = CanvasPolygon((x, y, x + 100 * sqrt(2), y, x, y + 100 * sqrt(2)), 'red', "MT", drawing_place)
                        if isPolygonOverlapping(mt3.id, type):
                            overlap = False
                            update_count_label(label, "+")
                        else:
                            drawing_place.delete(mt3.id)
                    else:
                        overlap = False
                        messagebox.showerror("Upps", "It looks like there is no place left on the canvas...")

            else:
                messagebox.showerror("Capacity limit", "You've reached the maximum amount of Medium Triangles")

        elif action == "del":
            if label_value(label) > 0:
                delPolygon("MT")
                update_count_label(label, "-")
            else:
                messagebox.showinfo("Minimum reached", "You've already reached the minimum amount of Medium Triangles")



    elif type == "ST":
        if action == "add":
            if label_value(label)+1 <= MAX_SM_TRIANGLE and label_value(label) >= 0:
                overlap, iter = True, 0
                while overlap:
                    if iter < 1000:
                        iter += 1
                        x, y = randfloatinRange(type)
                        sm1 = CanvasPolygon((x, y , x + 100, y, x, y + 100), 'orange', "ST", drawing_place)
                        if isPolygonOverlapping(sm1.id, type):
                            overlap = False
                            update_count_label(label, "+")
                        else:
                            drawing_place.delete(sm1.id)
                    else:
                        overlap = False
                        messagebox.showerror("Upps", "It looks like there is no place left on the canvas...")

            else:
                messagebox.showerror("Capacity limit", "You've reached the maximum amount of Small Triangles")

        elif action == "del":
            if label_value(label) > 0:
                delPolygon("ST")
                update_count_label(label, "-")
            else:
                messagebox.showinfo("Minimum reached", "You've already reached the minimum amount of Small Triangles")


    elif type == "S":
        if action == "add":
            if label_value(label)+1 <= MAX_SQUARE and label_value(label) >= 0:
                overlap, iter = True, 0
                while overlap:
                    if iter < 1000:
                        iter += 1
                        x, y = randfloatinRange(type)
                        sq = CanvasPolygon((x, y, x + 100, y, x + 100, y + 100, x, y + 100), 'pink', "S", drawing_place)
                        if isPolygonOverlapping(sq.id, type):
                            overlap = False
                            update_count_label(label, "+")
                        else:
                            drawing_place.delete(sq.id)
                    else:
                        overlap = False
                        messagebox.showerror("Upps", "It looks like there is no place left on the canvas...")
            else:
                messagebox.showerror("Capacity limit", "You've reached the maximum amount of Squares")

        elif action == "del":
            if label_value(label) > 0:
                delPolygon("S")
                update_count_label(label, "-")
            else:
                messagebox.showinfo("Minimum reached", "You've already reached the minimum amount of Squares")


    elif type == "BT":
        if action == "add":
            if label_value(label)+1 <= MAX_BIG_TRIANGLE and label_value(label) >= 0:
                overlap, iter = True, 0
                while overlap:
                    if iter < 1000:
                        iter += 1
                        x, y = randfloatinRange(type)
                        bt = CanvasPolygon((x, y, x + 200, y, x, y + 200), 'green', "BT", drawing_place)
                        if isPolygonOverlapping(bt.id, type):
                            overlap = False
                            update_count_label(label, "+")
                        else:
                            drawing_place.delete(bt.id)
                    else:
                        overlap = False
                        messagebox.showerror("Upps", "It looks like there is no place left on the canvas...")
            else:
                messagebox.showerror("Capacity limit", "You've reached the maximum amount of Big Triangles")

        elif action == "del":
            if label_value(label) > 0:
                delPolygon("BT")
                update_count_label(label, "-")
            else:
                messagebox.showinfo("Minimum reached", "You've already reached the minimum amount of Big Triangles")


    elif type == "P":
        if action == "add":
            if label_value(label)+1 <= MAX_PARALLELOGRAM and label_value(label) >= 0:
                overlap, iter = True, 0
                while overlap:
                    if iter < 1000:
                        iter += 1
                        x, y = randfloatinRange(type)
                        p = CanvasPolygon((x, y, x + 141.08, y, x + 212.13, y + 71.05, x + 70.71, y + 71.05), 'indian red', "P", drawing_place)
                        if isPolygonOverlapping(p.id, type):
                            overlap = False
                            update_count_label(label, "+")
                        else:
                            drawing_place.delete(p.id)
                    else:
                        overlap = False
                        messagebox.showerror("Upps", "It looks like there is no place left on the canvas...")

            else:
                messagebox.showerror("Capacity limit", "You've reached the maximum amount of Parallelograms")

        elif action == "del":
            if label_value(label) > 0:
                delPolygon("P")
                update_count_label(label, "-")
            else:
                messagebox.showinfo("Minimum reached", "You've already reached the minimum amount of Parallelograms")


def randfloatinRange(type):
    """ Returns a random float depending on the polygon type """

    if type == "MT":
        return uniform(0, CANVAS_SIDE - 100 * sqrt(2)), uniform(0, CANVAS_SIDE - 100 * sqrt(2))
    elif type == "ST" or type == "S":
        return uniform(0, CANVAS_SIDE - 100), uniform(0, CANVAS_SIDE - 100)
    elif type == "BT":
        return uniform(0, CANVAS_SIDE - 200), uniform(0, CANVAS_SIDE - 200)
    elif type == "P":
        return uniform(0, CANVAS_SIDE - 212.13), uniform(0, CANVAS_SIDE - 212.13)


def update_count_label(label,action):
    """ Updates the count of a label """

    str_count = label["text"]
    count = int(str_count)

    if action == "+":
        label["text"] = str(count + 1)
    elif action == "-":
        label["text"] = str(count - 1)
    elif action == "reset":
        resetCanvas()



def label_value(label):
    """ Converts label text to int """

    return int(label["text"])

def delPolygon(type):
    """ Deletes polygon that has for tag : 'type' """

    figures = drawing_place.find_withtag(type)

    if len(figures) == 1:
        drawing_place.delete(type)

    elif len(figures) > 1:
        result = tuple_to_list(figures)
        drawing_place.delete(result[0])


def isPolygonOverlapping(id, type):
    """ Checks if the last polygon created is overlapping other polygons """

    figures = drawing_place.find_all()
    if len(figures) > 1:
        overResult = []
        for fig in figures:
            if fig != id:
                coords = tuple_to_list(drawing_place.coords(fig))
                if type == "P":
                    result = tuple_to_list(drawing_place.find_overlapping(coords[0], coords[1], coords[4], coords[5]))

                    if id in result:
                        overResult.append(1)
                    else:
                        overResult.append(0)

                elif type == "S":
                    result = tuple_to_list(drawing_place.find_overlapping(coords[0], coords[1], coords[4], coords[5]))
                    if id in result:
                        overResult.append(1)
                    else:
                        overResult.append(0)

                else:
                    result = tuple_to_list(drawing_place.find_overlapping(coords[2], coords[3], coords[4], coords[5]))
                    if id in result:
                        overResult.append(1)
                    else:
                        overResult.append(0)

        if 1 in overResult:
            return False
        else:
            return True

    else:
        return True


def transformCoord():
    """ Sends polygon's coordinates to AI """

    figures = drawing_place.find_all()
    coords = []
    tags = []
    if len(figures) >= 1:
        for fig in figures:
            tags.append(drawing_place.gettags(fig))
            coords.append(divideBy100(tuple_to_list(drawing_place.coords(fig))))

        types = getTypeofPolygons()

        coordinates = []
        for shape in coords:
            poly = []
            for i in range(int(len(shape) / 2)):
                poly.append(find_nearest(coordinates, round(shape[i * 2], 3), round(shape[i * 2 + 1], 3)))
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



def find_nearest(shapes, x, y):

    for shape in shapes:
        for x2, y2 in shape:
            if euclideanDistance([x, y], [x2, y2]) < 1/100:
                return [x2, y2]

    return [x, y]


def getTypeofPolygons():
    """ Gets canvas polygons types """

    types = []
    for label in labels:
        for i in range(0, int(label['text'])):
            types.append(label.tag)

    return types



def divideBy100(coords):
    """ Divides by 100 all coordinates in order to fit real sizes """

    realCoords = []
    if(coords):
        for coord in coords:
            realCoords.append(coord/100)

        return realCoords


def resetCanvas():
    """ Resets canvas and labels when user clicks on Reset Button """

    figures = drawing_place.find_all()
    for fig in figures:
        drawing_place.delete(fig)

    for label in labels:
        label["text"] = "0"





""" Tkinter objets definitions """

# -- Window definition
window = Tk()
window.title("Tangram")
window.iconbitmap("img/tangram_logo.ico")
window.geometry("1260x800")
window.scale = 1

# -- Canvas & Frame definition
drawing_place = Canvas(window, width=700, height=700, bg="grey")
drawing_place.pack(pady=20, padx=0)

numPolygonsFrame = LabelFrame(window, text="Number of Polygons", padx=20, pady=10, labelanchor="nw")
numPolygonsFrame.place(x=70, y=50)

magnetFrame = LabelFrame(window, text="Magnetization distance", padx=10, pady=5, labelanchor="nw")
magnetFrame.place(x=40, y=250)

commandFrame = LabelFrame(window, text="Actions", padx=5, pady=5, labelanchor="nw")
commandFrame.place(x=70, y=350)


#imgMT = PhotoImage(file='img/MT.PNG')
#button = Button(numPolygonsFrame, image=imgMT)
#button.grid(row=1, column=4)

labels = []  # Keep track of all polygon's number labels

# + or - buttons
plusButton4 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [add_delPolygon("BT", bigTriangleLabel, "add")])
bigTriangleLabel = Label(numPolygonsFrame, text=0, fg="dark green")
bigTriangleLabel.tag = 'bt'
labels.append(bigTriangleLabel)
minusButton4 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [add_delPolygon("BT", bigTriangleLabel, "del")])

plusButton5 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [add_delPolygon("P", parallelogramLabel, "add")])
parallelogramLabel = Label(numPolygonsFrame, text=0, fg="dark green")
parallelogramLabel.tag = 'p'
labels.append(parallelogramLabel)
minusButton5 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [add_delPolygon("P", parallelogramLabel, "del")])

plusButton1 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [add_delPolygon("MT", medTriangleLabel, "add")])
medTriangleLabel = Label(numPolygonsFrame, text=0, fg="dark green")
medTriangleLabel.tag = 'mt'
labels.append(medTriangleLabel)
minusButton1 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [add_delPolygon("MT", medTriangleLabel, "del")])

plusButton3 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [add_delPolygon("S", squareLabel, "add")])
squareLabel = Label(numPolygonsFrame, text=0, fg="dark green")
squareLabel.tag = 's'
labels.append(squareLabel)
minusButton3 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [add_delPolygon("S", squareLabel, "del")])

plusButton2 = Button(numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER, command=lambda: [add_delPolygon("ST", smallTriangleLabel, "add")])
smallTriangleLabel = Label(numPolygonsFrame, text=0, fg="dark green")
smallTriangleLabel.tag = 'st'
labels.append(smallTriangleLabel)
minusButton2 = Button(numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER, command=lambda: [add_delPolygon("ST", smallTriangleLabel, "del")])






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

btn_reset = Button(commandFrame, text="  Reset  ", command=lambda:[resetCanvas()])
btn_reset.grid(row=1, column=2)


# Run the main loop:
window.mainloop()
