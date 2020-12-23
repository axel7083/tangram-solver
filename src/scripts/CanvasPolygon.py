from math import radians, cos, sin
from src.scripts import utils


class CanvasPolygon:
    """ This class is used to define a polygon on the screen """

    # Constructor
    def __init__(self, coords, color, tag, canvas, magnet_slider, movable=True):
        self.coords = coords
        self.color = color
        self.move = False
        self.tag = tag
        self.canvas = canvas
        self.magnet_slider = magnet_slider
        self.movable = movable
        self.init_x = 0
        self.init_y = 0

        self.id_ = canvas.create_polygon(list(self.coords), fill=self.color, tags=self.tag)

        canvas.tag_bind(self.id_, '<Button-1>', self.start_movement)
        canvas.tag_bind(self.id_, '<Motion>', self.movement)
        canvas.tag_bind(self.id_, '<ButtonRelease-1>', self.stop_movement)
        canvas.tag_bind(self.id_, '<Button-3>', self.rotate)

    def get_coords(self):
        """ Returns polygon's coordinates """

        return self.coords

    def set_coords(self, coords):
        """ Sets polygon's coordinates """

        self.coords = coords

    def delete(self):
        """ Deletes specified polygon """

        self.canvas.delete(self.id_)

    def start_movement(self, event):
        """ Modify move attribute and converts mouse coord to canvas coord """

        if not self.movable:
            return

        self.move = True

        # Translate mouse coordinates to canvas coordinate
        self.init_x = self.canvas.canvasx(event.x)
        self.init_y = self.canvas.canvasy(event.y)

    def movement(self, event):
        """ Moves polygon on the canvas """

        if self.move:
            end_x = self.canvas.canvasx(event.x)  # Translate mouse x screen coordinate to canvas coordinate
            end_y = self.canvas.canvasy(event.y)  # Translate mouse y screen coordinate to canvas coordinate

            deltax = end_x - self.init_x  # Find the difference
            deltay = end_y - self.init_y  # Find the difference

            self.new_position(deltax, deltay)

            self.init_x = end_x  # Update previous current with new location
            self.init_y = end_y

            self.canvas.move(self.id_, deltax, deltay)  # Move object

    def stop_movement(self, event):
        """ Updates move attribute and sticks the moving polygon to nearby polygon """

        nearby = utils.is_nearby(self.id_, self.canvas, self.magnet_slider)
        if nearby:
            self.delete()
            CanvasPolygon(utils.replace(utils.tuple_to_list(self.coords), utils.tuple_to_list(nearby)),
                          self.color, self.tag, self.canvas, self.magnet_slider)

        self.move = False

    def new_position(self, deltax, deltay):
        """ Updates the coords of a polygon given the coordinates of the translation """

        coord = utils.tuple_to_list(self.coords)  # Retrieve object points coordinates
        # old_coord = list(coord)  # Tuple to List
        coords = []  # New coords
        i = 0  # Cursor on old_coord
        for coordinates in coord:

            # check if index of coordinates in range of i and len(old_coord) in old_coord is pair (x coord)
            if (coord.index(coordinates, i, len(coord)) % 2) == 0:
                coords.append(coordinates + deltax)
            else:  # index's impair => y-coord
                coords.append(coordinates + deltay)
            i += 1

        self.set_coords(tuple(coords))

    def rotate(self, event):
        """ Rotate polygon the given angle about its center. """

        theta = radians(45)  # Convert angle to radians
        cos_ang, sin_ang = cos(theta), sin(theta)
        new_points, alpha, beta = [], [], []
        i = 0
        points = self.get_coords()

        for point in points:
            if (points.index(point, i, len(points)) % 2) == 0:
                alpha.append(point)
            else:
                beta.append(point)
            i += 1

        # find new x_y for each point
        for x_pos, y_pos in zip(alpha, beta):
            tx_pos, ty_pos = x_pos - points[0], y_pos - points[1]
            new_points.append(
                (tx_pos * cos_ang + ty_pos * sin_ang) + points[0]
            )
            new_points.append(
                (-tx_pos * sin_ang + ty_pos * cos_ang) + points[1]
            )

        self.delete()
        CanvasPolygon(new_points, self.color, self.tag, self.canvas, self.magnet_slider)
