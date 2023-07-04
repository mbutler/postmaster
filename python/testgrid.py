# import the Grid class
from grid import Grid
import time
import unittest

# create a grid with 10 columns and 10 rows
grid = Grid(10, 10)

# test set_properties
print('set_properties')
grid.set_properties({'x': 0, 'y': 0, 'z': 0}, {'obstacle': True})

print("""

-----

""")

# test get_properties
print('get_properties')
print(grid.get_properties({'x': 0, 'y': 0, 'z': 0}, ['obstacle']))

print("""

-----

""")

# test get_relative_coordinates
print('get_relative_coordinates')
print(grid.get_relative_coordinates({'x': 0, 'y': 0, 'z': 0}, 0, 1))
print(grid.get_relative_coordinates({'x': 0, 'y': 0, 'z': 0}, 0, 2))
print(grid.get_relative_coordinates({'x': 2, 'y': -2, 'z': 0}, 1, 1))

print("""

-----

""")
      
# test hexes_in_range
print('hexes_in_range')
print(grid.hexes_in_range({'x': 0, 'y': 0, 'z': 0}, 1))

print("""

-----

""")
      

# test draw_line
print('draw_line')
print(grid.draw_line({'x': 0, 'y': 0, 'z': 0}, {'x': 0, 'y': -3, 'z': 3}))

print("""

-----

""")

# test cube_distance
print('cube_distance')
print(grid.cube_distance({'x': 0, 'y': 0, 'z': 0}, {'x': 0, 'y': -3, 'z': 3}))

print("""

-----

""")

# test cube_round
print('cube_round')
print(grid.cube_round({'x': 0.1, 'y': -0.1, 'z': 0}))
print(grid.cube_round({'x': 0.1, 'y': -0.1, 'z': 0.1}))

print("""

-----

""")

# test hex range intersection
print('hex_range_intersection')
print(grid.hex_range_intersection({'x': 2, 'y': 1, 'z': -3}, 1, {'x': 0, 'y': 1, 'z': -1}, 1))

print("""

-----

""")

# test get_hexagon
print('get_hexagon')
print(grid.get_hexagon({'x': 0, 'y': 0, 'z': 0}))

print("""

-----

""")

# test flood_fill
print('flood_fill')
print(grid.flood_fill({'x': 0, 'y': 0, 'z': 0}, 1))

print("""

-----

""")

# test get_neighbors
print('neighbors')
print(grid.neighbors({'x': 0, 'y': 0, 'z': 0}))

print("""

-----

""")

# use set_properties to set 'obstacle' to True for a hexagon
grid.set_properties({'x': 0, 'y': 0, 'z': 0}, {'obstacle': True})

import unittest

def dict_lists_equal(list1, list2):
    """Helper function to test if two lists of dictionaries are equal"""
    return set(tuple(sorted(d.items())) for d in list1) == set(tuple(sorted(d.items())) for d in list2)

class TestHexesInRange(unittest.TestCase):
    def setUp(self):
        self.center_coords = {'x': 0, 'y': 0, 'z': 0}

    def test_hexes_in_range_N0(self):
        result = grid.hexes_in_range(self.center_coords, 0)
        expected = [self.center_coords]
        self.assertTrue(dict_lists_equal(result, expected))

    def test_hexes_in_range_N0_exclude_center(self):
        result = grid.hexes_in_range(self.center_coords, 0, exclude_center=True)
        expected = []
        self.assertTrue(dict_lists_equal(result, expected))

    def test_hexes_in_range_N1(self):
        result = grid.hexes_in_range(self.center_coords, 1)
        expected = [self.center_coords]
        for dx, dy, dz in [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]:
            expected.append({'x': dx, 'y': dy, 'z': dz})
        self.assertTrue(dict_lists_equal(result, expected))

    def test_hexes_in_range_N1_exclude_center(self):
        result = grid.hexes_in_range(self.center_coords, 1, exclude_center=True)
        expected = []
        for dx, dy, dz in [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]:
            expected.append({'x': dx, 'y': dy, 'z': dz})
        self.assertTrue(dict_lists_equal(result, expected))


class TestCubeDistance(unittest.TestCase):

    def test_cube_distance_same_coords(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(grid.cube_distance(start_coords, end_coords), 0)

    def test_cube_distance_different_coords(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 1, 'y': -1, 'z': 0}
        self.assertEqual(grid.cube_distance(start_coords, end_coords), 1)

    def test_cube_distance_negative_coords(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 0, 'y': -3, 'z': 3}
        self.assertEqual(grid.cube_distance(start_coords, end_coords), 3)

class TestCubeRound(unittest.TestCase):

    def test_cube_round_zero(self):
        coords = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(grid.cube_round(coords), {'x': 0, 'y': 0, 'z': 0})

    def test_cube_round_negative(self):
        coords = {'x': 0, 'y': -3, 'z': 3}
        self.assertEqual(grid.cube_round(coords), {'x': 0, 'y': -3, 'z': 3})

    def test_cube_round_positive(self):
        coords = {'x': 1, 'y': 2, 'z': -3}
        self.assertEqual(grid.cube_round(coords), {'x': 1, 'y': 2, 'z': -3})

    def test_cube_round(self):
        coords = {'x': 0.1, 'y': -0.1, 'z': 0.1}
        self.assertEqual(grid.cube_round(coords), {'x': 0, 'y': 0, 'z': 0})

class TestHexRangeIntersection(unittest.TestCase):

    def test_hex_range_intersection(self):
        radius = 1
        start_coords = {'x': 0, 'y': 2, 'z': -2}
        end_coords = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(grid.hex_range_intersection(start_coords, radius, end_coords, radius), [{'x': 0, 'y': 1, 'z': -1}])

    def test_hex_range_intersection_no_intersection(self):
        radius = 1
        start_coords = {'x': 2, 'y': -1, 'z': 1}
        end_coords = {'x': -2, 'y': 1, 'z': 1}
        self.assertEqual(grid.hex_range_intersection(start_coords, radius, end_coords, radius), [])

    def test_hex_range_multiple_intersections(self):
        radius = 1
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 1, 'y': -2, 'z': 1}
        self.assertEqual(grid.hex_range_intersection(start_coords, radius, end_coords, radius), [{'x': 0, 'y': -1, 'z': 1}, {'x': 1, 'y': -1, 'z': 0}])

if __name__ == "__main__":
    unittest.main()





