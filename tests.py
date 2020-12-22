# Unit testing
import utils
from TangramSolver import TangramSolver
from math import sqrt
from shapely.geos import TopologicalError
from shapely.geometry import Polygon
import pytest


def test_tangram_full_square():
    original = [[0, 0], [2 * sqrt(2), 0], [2 * sqrt(2), 2 * sqrt(2)], [0, 2 * sqrt(2)], [0, 0]]
    types = ["bt", "bt", "p", "mt", "s", "st", "st"]

    tangram_solver = TangramSolver(Polygon(original), types)

    try:
        shapes, final_shapes, coordinates = tangram_solver.execute()
        # utils.draw_node(shapes, final_shapes, coordinates)
        assert len(shapes) == len(types)

    except (RuntimeError, TypeError, NameError):
        pytest.raises(RuntimeError)
    except TopologicalError:
        assert pytest.raises(TopologicalError)


def test_tangram_fit_function():

    types = ["bt", "bt", "p", "mt", "s", "st", "st"]
    original = [[0, 0], [2 * sqrt(2), 0], [2 * sqrt(2), 2 * sqrt(2)], [0, 2 * sqrt(2)], [0, 0]]
    state = [[0.0, 0.0, 3, 2],
             [0.0, 0.0, 5, 1],
             [0.0, 2.8284271247461903, 2, 2],
             [1.4042135623730951, 2.8284271247461903, 4, 1],
             [2.1063203435596423, 2.1263203435596427, 1, 2],
             [2.1063203435596423, 2.1263203435596427, 1, 1],
             [2.1063203435596423, 0.7191778489984131, 7, 0]]

    area = utils.fit_function(types, state, Polygon(original)).area
    assert area < 0.1

