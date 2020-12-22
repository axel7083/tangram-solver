from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from shapely.geometry import Polygon

import SolvingThread
import utils
from CanvasPolygon import CanvasPolygon
from VerticalScrolledFrame import VerticalScrolledFrame


class TangramCanvas:

    def polygon_action(self, _type, label, action, coord):
        """ Add or Delete polygons of the canvas depending on what button the user clicked on """
        if action == "add":
            self.create_polygon(_type, label, coord)
        elif action == "del":
            self.delete_polygon(_type, label)

    def create_polygon(self, _type, label, coord):
        x = utils.CANVAS_SIDE / 2
        y = utils.CANVAS_SIDE / 2
        _max, coords = utils.get_settings_by_type(_type, x, y)
        color = utils.random_color()
        if coord == 0:
            _max, coords = self.get_settings_by_type(_type, x, y)

            if self.label_value(label) + 1 <= _max and self.label_value(label) >= 0:
                # Creating a new Polygon
                CanvasPolygon(coords, color, _type, self.drawing_place, self.magnetSlider)
                utils.update_count_label(label, "+")
            else:
                messagebox.showerror("Maximum reach", "You've reached the maximum amount of this item.")
        else:
            CanvasPolygon(coord, color, _type, self.drawing_place, self.magnetSlider)
            utils.update_count_label(label, "+")

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
            messagebox.showerror("Minimum reached", "You've reached the minimum amount of this item.")

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

    def get_label_by_type(self, _type):
        for label in self.labels:
            if label.tag == _type:
                return label

    def get_polygons_by_model(self, model):
        if model == "cat":
            return ['bt', 'bt', 'p', 'mt', 's', 'st', 'st'],\
                   [[292.0, 199.0, 221.28932188134524, 269.71067811865476, 221.28932188134524, 128.28932188134524],
                    [292.0, 199.0, 362.71067811865476, 128.28932188134524, 362.71067811865476, 269.71067811865476],
                    [221.28932188134524, 269.71067811865476, 292.0, 199.0, 362.71067811865476, 269.71067811865476,
                     292.0, 340.4213562373095],
                    [433.4213562373095, 481.842712474619, 291.99999999999994, 623.2640687119285, 292.0,
                     340.4213562373095],
                    [192.2979438526968, 440.1234123846127, 292.0, 340.4213562373095, 292.0, 539.8254685319159],
                    [433.4213562373095, 681.842712474619, 233.4213562373095, 681.842712474619, 433.4213562373095,
                     481.842712474619],
                    [433.4213562373095, 681.842712474619, 433.4213562373095, 582.1406563273158, 533.1234123846127,
                     482.4386001800126, 533.1234123846127, 582.1406563273158]],

        elif model == "swan":
            return ['bt', 'bt', 'p', 'mt', 's', 'st', 'st'], \
                   [[262.0, 509.0, 262.0, 309.0, 462.0, 509.0],
                    [403.4213562373095, 450.4213562373095, 262.0, 309.0, 544.842712474619, 309.0],
                    [162.2979438526968, 408.7020561473032, 262.0, 309.0, 262.0, 508.4041122946064],
                    [233.00862197135154, 337.99137802864846, 162.2979438526968, 408.7020561473032, 162.2979438526968,
                     267.2806999099937],
                    [162.2979438526968, 267.2806999099937, 233.00862197135154, 196.57002179133895, 303.7193000900063,
                     267.2806999099937, 233.00862197135154, 337.99137802864846],
                    [233.2193000900063, 55.7806999099937, 303.7193000900063, 126.2806999099937, 303.7193000900063,
                     267.2806999099937, 233.2193000900063, 196.7806999099937],
                    [233.2193000900063, 155.78069990999379, 133.21930009000621, 155.78069990999379, 233.2193000900063,
                     55.7806999099937]]

        elif model == "hen":
            return ['bt', 'bt', 'p', 'mt', 's', 'st', 'st'], \
                   [[364.0, 325.0, 364.0, 525.0, 163.99999999999997, 325.0], [364.0, 325.0, 564.0, 325.0, 364.0, 525.0],
                    [64.29794385269676, 225.2979438526968, 163.99999999999997, 225.2979438526968, 263.7020561473032,
                     325.0, 163.99999999999997, 325.0],
                    [64.29794385269676, 225.2979438526968, 64.29794385269676, 125.29794385269673, 164.2979438526968,
                     225.2979438526968], [464.0, 225.0, 564.0, 225.0, 564.0, 325.0, 464.0, 325.0],
                    [563.7020561473032, 125.29794385269673, 663.4041122946064, 225.0, 464.0, 225.0],
                    [364.0, 525.0, 434.71067811865476, 595.7106781186548, 293.28932188134524, 595.7106781186548]]

        elif model == "square":
            return ['bt', 'bt', 'p', 'mt', 's', 'st', 'st'], \
                   [[182.0, 521.0, 40.57864376269043, 662.4213562373095, 40.57864376269046, 379.5786437626905],
                    [182.0, 521.0, 40.57864376269046, 379.5786437626905, 323.4213562373095, 379.5786437626905],
                    [182.0, 521.0, 252.71067811865476, 450.28932188134524, 323.4213562373095, 521.0,
                     252.71067811865476, 591.7106781186548], [252.71067811865476, 450.28932188134524, 323.4213562373095,
                    379.5786437626905, 323.4213562373095, 521.0],
                    [40.57864376269043, 662.4213562373095, 111.07864376269043, 591.9213562373095, 252.07864376269043,
                     591.9213562373095, 181.57864376269043, 662.4213562373095], [323.4213562373095, 662.0,
                    182.4213562373095, 662.0, 323.4213562373095, 521.0], [182.0, 521.0, 252.71067811865476,
                    591.7106781186548, 111.28932188134524, 591.7106781186548]]

        elif model == "boat":
            return ['bt', 'bt', 'p', 'mt', 's', 'st', 'st'], \
                   [[663.0, 370.0, 592.5, 440.5, 451.49999999999994, 440.50000000000006, 522.0, 370.0],
                    [522.2106781186548, 511.21067811865476, 451.49999999999994, 440.50000000000006, 592.9213562373094,
                     440.50000000000006],
                    [451.49999999999994, 440.50000000000006, 380.7893218813452, 369.7893218813453, 522.2106781186548,
                     369.7893218813453],
                    [380.7893218813452, 369.7893218813453, 522.2106781186549, 511.2106781186549, 239.36796564403562,
                     511.21067811865487],
                    [239.36796564403562, 511.21067811865487, 97.94660940672611, 369.78932188134536, 380.78932188134513,
                     369.78932188134536], [327.0, 270.0, 427.0, 270.0, 427.0, 370.0, 327.0, 370.0],
                    [372.0, 170.0, 471.70205614730327, 269.70205614730327, 272.29794385269673, 269.70205614730327]]

    def models(self, model):
        """ Puts a puzzle model on the canvas """

        utils.reset_canvas(self.drawing_place, self.labels)
        _type, coords = self.get_polygons_by_model(model)
        for i, coord in enumerate(coords):
            print(_type[i])
            self.polygon_action(_type[i], self.get_label_by_type(_type[i]), "add", coord)

    def __init__(self):
        """ Tkinter objets definitions """

        # -- Window definition
        self.window = Tk()
        self.window.title("Tangram")
        self.window.iconbitmap("img/tangram_logo.ico")
        self.window.geometry("1260x800")
        self.window.resizable(0, 0)
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

        # Scrollbar frame
        self.scframe = VerticalScrolledFrame(self.window)
        self.scframe.place(x=1000, y=20)

        self.squareModel = PhotoImage(file='img/square.PNG')
        self.button = Button(self.scframe.interior, image=self.squareModel, relief=FLAT,
                             command=lambda: [self.models("square")])
        self.button.pack()
        self.catModel = PhotoImage(file="img/cat.PNG")
        self.button = Button(self.scframe.interior, image=self.catModel, relief=FLAT,
                             command=lambda: [self.models("cat")])
        self.button.pack()
        self.boatModel = PhotoImage(file="img/boat.PNG")
        self.button = Button(self.scframe.interior, image=self.boatModel, relief=FLAT,
                             command=lambda: [self.models("boat")])
        self.button.pack()
        self.swanModel = PhotoImage(file="img/swan.PNG")
        self.button = Button(self.scframe.interior, image=self.swanModel, relief=FLAT,
                             command=lambda: [self.models("swan")])
        self.button.pack()
        self.henModel = PhotoImage(file='img/hen.PNG')
        self.button = Button(self.scframe.interior, image=self.henModel, relief=FLAT,
                             command=lambda: [self.models("hen")])
        self.button.pack()

        # Polygons images next to + _ - buttons
        self.imgMT = PhotoImage(file='img/mt.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgMT, state="disabled")
        self.button.grid(row=1, column=4)

        self.imgST = PhotoImage(file='img/st.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgST, state="disabled")
        self.button.grid(row=2, column=4)

        self.imgSQ = PhotoImage(file='img/sq.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgSQ, state="disabled")
        self.button.grid(row=3, column=4)

        self.imgBT = PhotoImage(file='img/bt.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgBT, state="disabled")
        self.button.grid(row=4, column=4)

        self.imgP = PhotoImage(file='img/p.png')
        self.button = Button(self.numPolygonsFrame, image=self.imgP, state="disabled")
        self.button.grid(row=5, column=4)

        # Polygons images + maximum limits
        self.max1 = Button(self.polygonsLimitsFrame, image=self.imgMT, state="disabled")
        self.labelMax1 = Label(self.polygonsLimitsFrame, text=0)
        self.max2 = Button(self.polygonsLimitsFrame, image=self.imgST, state="disabled")
        self.labelMax2 = Label(self.polygonsLimitsFrame, text=0)
        self.max3 = Button(self.polygonsLimitsFrame, image=self.imgSQ, state="disabled")
        self.labelMax3 = Label(self.polygonsLimitsFrame, text=0)
        self.max4 = Button(self.polygonsLimitsFrame, image=self.imgBT, state="disabled")
        self.labelMax4 = Label(self.polygonsLimitsFrame, text=0)
        self.max5 = Button(self.polygonsLimitsFrame, image=self.imgP, state="disabled")
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
                                  command=lambda: [self.polygon_action("bt", self.bigTriangleLabel, "add", 0)])
        self.bigTriangleLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.bigTriangleLabel.tag = 'bt'
        self.labels.append(self.bigTriangleLabel)
        self.minusButton4 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("bt", self.bigTriangleLabel, "del", 0)])

        self.plusButton5 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("p", self.parallelogramLabel, "add", 0)])
        self.parallelogramLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.parallelogramLabel.tag = 'p'
        self.labels.append(self.parallelogramLabel)
        self.minusButton5 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("p", self.parallelogramLabel, "del", 0)])

        self.plusButton1 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("mt", self.medTriangleLabel, "add", 0)])
        self.medTriangleLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.medTriangleLabel.tag = 'mt'
        self.labels.append(self.medTriangleLabel)
        self.minusButton1 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("mt", self.medTriangleLabel, "del", 0)])

        self.plusButton3 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("s", self.squareLabel, "add", 0)])
        self.squareLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.squareLabel.tag = 's'
        self.labels.append(self.squareLabel)
        self.minusButton3 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("s", self.squareLabel, "del", 0)])

        self.plusButton2 = Button(self.numPolygonsFrame, text="+", fg="green", width=3, justify=CENTER,
                                  command=lambda: [self.polygon_action("st", self.smallTriangleLabel, "add", 0)])
        self.smallTriangleLabel = Label(self.numPolygonsFrame, text=0, fg="dark green")
        self.smallTriangleLabel.tag = 'st'
        self.labels.append(self.smallTriangleLabel)
        self.minusButton2 = Button(self.numPolygonsFrame, text="-", fg="red", width=3, justify=CENTER,
                                   command=lambda: [self.polygon_action("st", self.smallTriangleLabel, "del", 0)])

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
        self.magnetSlider = Scale(self.magnetFrame, from_=10, to=100, length=150, resolution=5, orient=HORIZONTAL,
                                  width=20)
        self.magnetSlider.grid(row=0, column=0)

        self.btn_validate = Button(self.commandFrame, text="Validate", command=lambda: [self.transformCoord()])
        self.btn_validate.grid(row=1, column=1)

        self.btn_reset = Button(self.commandFrame, text="  Reset  ",
                                command=lambda: [utils.reset_canvas(self.drawing_place, self.labels)])
        self.btn_reset.grid(row=1, column=2)

        # Updates polygons limits with program constants
        self.getPolygonsLimits()

    def start(self):
        # Run the main loop:
        self.window.mainloop()
