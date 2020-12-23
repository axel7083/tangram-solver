import copy
from src.scripts import utils, PolygonUtils
from shapely.geometry import Polygon, LineString


class TangramSolver:
    # Variables
    coordinates = []
    shapes = ["bt", "bt", "p", "mt", "s", "st", "st"]  # Example
    global_size = 1
    output = []

    # Constructor
    def __init__(self, coordinates, shapes, global_size=1):
        self.coordinates = coordinates
        self.shapes = shapes
        self.global_size = global_size

    # Exploring the corners
    def corner_explore(self, ref, shape_index, state):
        multipolygon = []
        if not isinstance(ref, Polygon):
            multipolygon = list(ref)
        else:
            multipolygon = [ref]

        # Convert check multipolygon and convert it into list of polygon
        for sub_ref in multipolygon:

            # Avoiding error
            if isinstance(sub_ref, LineString):
                continue

            for i in range(len(sub_ref.exterior.xy[0])):

                x = sub_ref.exterior.xy[0][i]
                y = sub_ref.exterior.xy[1][i]

                for r in range(PolygonUtils.get_rot_by_index(self.shapes, shape_index)):

                    for point_index in range(PolygonUtils.get_corner_count_by_index(self.shapes, shape_index)):

                        new_state = copy.deepcopy(state)
                        new_state.append([x, y, r, point_index])
                        poly = PolygonUtils.get_shape_polygon_by_index(self.shapes, shape_index, x, y, r, point_index)

                        # new_ref = fit_function(state, ref)
                        diff = ref.difference(poly)

                        if utils.margin_error(diff.area, ref.area - poly.area) < 0.35:
                            # if int(ref.area - poly.area) == int(diff.area):
                            # print("We found a shape which fit ")
                            if shape_index == len(self.shapes) - 1:
                                print("Finish")
                                return True, new_state
                            else:

                                is_success, new_state = self.corner_explore(diff, shape_index + 1, new_state)
                                if is_success:
                                    return True, new_state

        return False, None

    # Solving function
    def execute(self):

        print("Solving...")
        is_success, final_shapes = self.corner_explore(self.coordinates, 0, [])

        if is_success:
            print("Success")
            return self.shapes, final_shapes, self.coordinates
        else:
            print("Error")

        return True
