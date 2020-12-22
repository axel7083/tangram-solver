from math import *
import utils


class CanvasPolygon:

    # Constructor
    def __init__(self, coords, color, tag, canvas, magnetSlider, movable=True):
        self.coords = coords
        self.color = color
        self.move = False
        self.tag = tag
        self.canvas = canvas
        self.magnetSlider = magnetSlider
        self.movable = movable

        self.id = canvas.create_polygon(list(self.coords), fill=self.color, tags=self.tag)

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

        if not self.movable:
            return

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

        yesCase = utils.is_nearby(self.id, self.canvas, self.magnetSlider)
        if yesCase:
            self.delete()
            CanvasPolygon(utils.replace(utils.tuple_to_list(self.coords), utils.tuple_to_list(yesCase)),
                          self.color, self.tag, self.canvas, self.magnetSlider)

        self.move = False

    def new_position(self, deltax, deltay):
        """ Updates the coords of a polygon given the coordinates of the translation """

        coord = utils.tuple_to_list(self.coords)  # Retrieve object points coordinates
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
        CanvasPolygon(new_points, self.color, self.tag, self.canvas, self.magnetSlider)

    def print_figure_coords(self, figure):
        print(figure.coords)
