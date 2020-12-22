from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from shapely.geometry import Polygon

import SolvingThread
import utils
from CanvasPolygon import CanvasPolygon


class TangramCanvas:

    def polygon_action(self, _type, label, action):
        """ Add or Delete polygons of the canvas depending on what button the user clicked on """
        if action == "add":
            self.create_polygon(_type, label)
        elif action == "del":
            self.delete_polygon(_type, label)

    def create_polygon(self, _type, label):
        x = utils.CANVAS_SIDE / 2
        y = utils.CANVAS_SIDE / 2
        _max, coords = utils.get_settings_by_type(_type, x, y)
        color = utils.random_color()

        if utils.label_value(label) + 1 <= _max and utils.label_value(label) >= 0:
            # Creating a new Polygon
            CanvasPolygon(coords, color, _type, self.drawing_place, self.magnetSlider)
            utils.update_count_label(label, "+")
        else:
            messagebox.showerror("Maximum reach", "You've reached the maximum amount of this item.")

    def delete_polygon(self, _type, label):
        """ Deletes polygon that has for tag : 'type' """

        if utils.label_value(label) > 0:

            figures = self.drawing_place.find_withtag(_type)
            _len = len(figures)
            if _len == 1:
                self.drawing_place.delete(_type)

            elif _len > 1:
                result = utils.tuple_to_list(figures)
                self.drawing_place.delete(result[_len - 1])

            utils.update_count_label(label, "-")
        else:
            messagebox.showerror("Minimum reach", "You've reached the minimum amount of this item.")

    def transformCoord(self):
        """ Sends polygon's coordinates to AI """

        figures = self.drawing_place.find_all()
        coords = []
        co = []
        tags = []
        if len(figures) >= 1:
            for fig in figures:
                tags.append(self.drawing_place.gettags(fig))
                co.append(utils.tuple_to_list(self.drawing_place.coords(fig)))
                coords.append(utils.divide_coords(utils.tuple_to_list(self.drawing_place.coords(fig)), 100))

            types = self.getTypeofPolygons()

            print(co)
            print(types)

            coordinates = []
            for shape in coords:
                poly = []
                for i in range(int(len(shape) / 2)):
                    # poly.append(utils.find_nearest(coordinates, round(shape[i * 2], 2), round(shape[i * 2 + 1], 2)))
                    poly.append([round(shape[i * 2], 2), round(shape[i * 2 + 1], 2)])

                coordinates.append(poly)

            print(coordinates)

            polygons = []
            for shape in coordinates:
                polygons.append(Polygon(shape))

            # Output can be polygon OR multipolygon
            output = utils.merge(polygons)
            print("Output:")
            print(output)

            multipolygon = []
            if not isinstance(output, Polygon):
                print("Multipolygon")
                multipolygon = list(output)
            else:
                multipolygon = [output]
                print("Polygon")

            utils.reset_canvas(self.drawing_place, self.labels)

            # Convert check multipolygon and convert it into list of polygon
            for sub_ref in multipolygon:

                print(len(sub_ref.exterior.xy[0]))
                xy = []
                for i in range(len(sub_ref.exterior.xy[0])):
                    xy.append(sub_ref.exterior.xy[0][i] * 100)
                    xy.append(sub_ref.exterior.xy[1][i] * 100)

                CanvasPolygon(xy, 'black', "origin", self.drawing_place, self.magnetSlider, False)
                print(xy)

            print(types)

            should_reset = SolvingThread.solve(output, types, self.window, self.progress)
            if should_reset:
                utils.reset_canvas(self.drawing_place, self.labels)
                self.window.protocol("WM_DELETE_WINDOW", self.close_event)

            # utils.draw_node(shapes, state, ref)

        else:
            messagebox.showerror("No polygons on canvas", "Please add at least one polygon before testing our AI")

    def close_event(self):
        self.window.destroy()

    def getTypeofPolygons(self):
        """ Gets canvas polygons types """

        types = []
        for label in self.labels:
            for i in range(0, int(label['text'])):
                types.append(label.tag)

        return types

    def getPolygonsLimits(self):
        """ Updates at initialization, labels for polygons limits """

        self.labelMax1["text"] = str(utils.MAX_MED_TRIANGLE)
        self.labelMax2["text"] = str(utils.MAX_SM_TRIANGLE)
        self.labelMax3["text"] = str(utils.MAX_SQUARE)
        self.labelMax4["text"] = str(utils.MAX_BIG_TRIANGLE)
        self.labelMax5["text"] = str(utils.MAX_PARALLELOGRAM)

    def __init__(self):
        """ Tkinter objets definitions """

        # -- Window definition
        self.window = Tk()
        self.window.title("Tangram")
        self.window.iconbitmap("img/tangram_logo.ico")
        self.window.geometry("1260x800")
        self.window.scale = 1

        self.labels = []  # Keep track of all polygon's number labels

        # -- Canvas & Frame definition
        self.drawing_place = Canvas(self.window, width=700, height=700, bg="grey")
        self.drawing_place.pack(pady=20, padx=0)

        self.numPolygonsFrame = LabelFrame(self.window, text="Number of Polygons", padx=20, pady=10, labelanchor="nw")
        self.numPolygonsFrame.place(x=70, y=50)

        self.magnetFrame = LabelFrame(self.window, text="Magnetization distance", padx=10, pady=5, labelanchor="nw")
        self.magnetFrame.place(x=40, y=250)

        self.commandFrame = LabelFrame(self.window, text="Actions", padx=5, pady=5, labelanchor="nw")
        self.commandFrame.place(x=70, y=350)

        self.polygonsLimitsFrame = LabelFrame(self.window, text="Polygon's limits", padx=5, pady=5, labelanchor="nw")
        self.polygonsLimitsFrame.place(x=70, y=500)

        # Polygons images next to + _ - buttons
        self.imgMT = PhotoImage(file='img/mt.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgMT)
        self.button.grid(row=1, column=4)

        self.imgST = PhotoImage(file='img/st.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgST)
        self.button.grid(row=2, column=4)

        self.imgSQ = PhotoImage(file='img/sq.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgSQ)
        self.button.grid(row=3, column=4)

        self.imgBT = PhotoImage(file='img/bt.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgBT)
        self.button.grid(row=4, column=4)

        self.imgP = PhotoImage(file='img/p.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgP)
        self.button.grid(row=5, column=4)

        # Polygons images + maximum limits
        self.max1 = Button(self.polygonsLimitsFrame, image=self.imgMT)
        self.labelMax1 = Label(self.polygonsLimitsFrame, text=0)
        self.max2 = Button(self.polygonsLimitsFrame, image=self.imgST)
        self.labelMax2 = Label(self.polygonsLimitsFrame, text=0)
        self.max3 = Button(self.polygonsLimitsFrame, image=self.imgSQ)
        self.labelMax3 = Label(self.polygonsLimitsFrame, text=0)
        self.max4 = Button(self.polygonsLimitsFrame, image=self.imgBT)
        self.labelMax4 = Label(self.polygonsLimitsFrame, text=0)
        self.max5 = Button(self.polygonsLimitsFrame, image=self.imgP)
        self.labelMax5 = Label(self.polygonsLimitsFrame, text=0)

        self.progress = ttk.Progressbar(self.window, orient=HORIZONTAL, length=120)
        self.progress.pack()
        # to step progress bar up
        self.progress.config(mode="determinate", maximum=100, value=0)
        self.progress.step(0)
        self.progress.stop()

        self.max1.grid(row=1, column=1)
        self.max2.grid(row=2, column=1)
        self.max3.grid(row=3, column=1)
        self.max4.grid(row=4, column=1)
        self.max5.grid(row=5, column=1)
        self.labelMax1.grid(row=1, column=2)
        self.labelMax2.grid(row=2, column=2)
        self.labelMax3.grid(row=3, column=2)
        self.labelMax4.grid(row=4, column=2)
        self.labelMax5.grid(row=5, column=2)

        # + or - buttons
        self.plusButton4 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("bt", self.bigTriangleLabel, "add")])
        self.bigTriangleLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.bigTriangleLabel.tag = 'bt'
        self.labels.append(self.bigTriangleLabel)
        self.minusButton4 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("bt", self.bigTriangleLabel, "del")])

        self.plusButton5 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("p", self.parallelogramLabel, "add")])
        self.parallelogramLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.parallelogramLabel.tag = 'p'
        self.labels.append(self.parallelogramLabel)
        self.minusButton5 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("p", self.parallelogramLabel, "del")])

        self.plusButton1 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("mt", self.medTriangleLabel, "add")])
        self.medTriangleLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.medTriangleLabel.tag = 'mt'
        self.labels.append(self.medTriangleLabel)
        self.minusButton1 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("mt", self.medTriangleLabel, "del")])

        self.plusButton3 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("s", self.squareLabel, "add")])
        self.squareLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.squareLabel.tag = 's'
        self.labels.append(self.squareLabel)
        self.minusButton3 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("s", self.squareLabel, "del")])

        self.plusButton2 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("st", self.smallTriangleLabel, "add")])
        self.smallTriangleLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.smallTriangleLabel.tag = 'st'
        self.labels.append(self.smallTriangleLabel)
        self.minusButton2 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("st", self.smallTriangleLabel, "del")])

        # + or - buttons placement

        self.plusButton1.grid(row=1, column=1)
        self.medTriangleLabel.grid(row=1, column=2)
        self.minusButton1.grid(row=1, column=3)

        self.plusButton2.grid(row=2, column=1)
        self.smallTriangleLabel.grid(row=2, column=2)
        self.minusButton2.grid(row=2, column=3)

        self.plusButton3.grid(row=3, column=1)
        self.squareLabel.grid(row=3, column=2)
        self.minusButton3.grid(row=3, column=3)

        self.plusButton4.grid(row=4, column=1)
        self.bigTriangleLabel.grid(row=4, column=2)
        self.minusButton4.grid(row=4, column=3)

        self.plusButton5.grid(row=5, column=1)
        self.parallelogramLabel.grid(row=5, column=2)
        self.minusButton5.grid(row=5, column=3)

        # Buttons and Slider placement
        self.magnetSlider = Scale(self.magnetFrame, from_=10, to=100, length=150, resolution=5, orient=HORIZONTAL, width=20)
        self.magnetSlider.grid(row=0, column=0)

        self.btn_validate = Button(self.commandFrame, text="Validate", command=lambda: [self.transformCoord()])
        self.btn_validate.grid(row=1, column=1)

        self.btn_reset = Button(self.commandFrame, text="  Reset  ", command=lambda: [utils.reset_canvas(self.drawing_place, self.labels)])
        self.btn_reset.grid(row=1, column=2)

        # Updates polygons limits with program constants
        self.getPolygonsLimits()

    def start(self):
        # Run the main loop:
        self.window.mainloop()
