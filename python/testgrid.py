# import the Grid class
from grid import Grid
import time
import unittest

"""
We assume we are generating Grid, a 6-mile hex: http://steamtunnel.blogspot.com/2009/12/in-praise-of-6-mile-hex.html
A 6-mile hex has a radius of 3 miles. 3 miles is 15,840 feet. A Grid hex is 31,680 feet across. Grid hex is 20,371.2 acres.
A Grid size of 11 (Grid(11)) is 23 sub-hexes wide with a side length of 12 sub-hexes.
397 total sub-hexes in the larger Grid hex. 31.82 sq miles in the larger Grid hex.
Each sub-hex is 1,377 feet, or 275 squares, wide. 803 feet per sub-hex side. 51.3 acres per sub-hex.
"""

# create a grid with 10 columns and 10 rows
grid = Grid(11)

# test set_properties
print('set_properties')
grid.set_properties({'x': 0, 'y': 0, 'z': 0}, {'obstacle': True})

print("""

-----

""")

# test get_properties
print('get_properties')
print(grid.get_properties(({'x': 0, 'y': 0, 'z': 0}), ['obstacle']))

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
      

# test hexes_in_path
print('hexes_in_path')
print(grid.hexes_in_path({'x': 0, 'y': 0, 'z': 0}, {'x': 0, 'y': -3, 'z': 3}))

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
# set obstacle next to start hex
grid.set_properties({'x': 1, 'y': -1, 'z': 0}, {'obstacle': True})
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
jsongrid = grid.to_json()
with open('grid.json', 'w') as f:
     f.write(jsongrid)
grid.draw_grid(25)

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
        print('test_hexes_in_range_N0 passed')

    def test_hexes_in_range_N0_exclude_center(self):
        result = grid.hexes_in_range(self.center_coords, 0, exclude_center=True)
        expected = []
        self.assertTrue(dict_lists_equal(result, expected))
        print('test_hexes_in_range_N0_exclude_center passed')

    def test_hexes_in_range_N1(self):
        result = grid.hexes_in_range(self.center_coords, 1)
        expected = [self.center_coords]
        for dx, dy, dz in [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]:
            expected.append({'x': dx, 'y': dy, 'z': dz})
        self.assertTrue(dict_lists_equal(result, expected))
        print('test_hexes_in_range_N1 passed')

    def test_hexes_in_range_N1_exclude_center(self):
        result = grid.hexes_in_range(self.center_coords, 1, exclude_center=True)
        expected = []
        for dx, dy, dz in [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]:
            expected.append({'x': dx, 'y': dy, 'z': dz})
        self.assertTrue(dict_lists_equal(result, expected))
        print('test_hexes_in_range_N1_exclude_center passed')


class TestCubeDistance(unittest.TestCase):

    def test_cube_distance_same_coords(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(grid.cube_distance(start_coords, end_coords), 0)
        print('test_cube_distance_same_coords passed')

    def test_cube_distance_different_coords(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 1, 'y': -1, 'z': 0}
        self.assertEqual(grid.cube_distance(start_coords, end_coords), 1)
        print('test_cube_distance_different_coords passed')

    def test_cube_distance_negative_coords(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 0, 'y': -3, 'z': 3}
        self.assertEqual(grid.cube_distance(start_coords, end_coords), 3)
        print('test_cube_distance_negative_coords passed')

class TestCubeRound(unittest.TestCase):

    def test_cube_round_zero(self):
        coords = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(grid.cube_round(coords), {'x': 0, 'y': 0, 'z': 0})
        print('test_cube_round_zero passed')

    def test_cube_round_negative(self):
        coords = {'x': 0, 'y': -3, 'z': 3}
        self.assertEqual(grid.cube_round(coords), {'x': 0, 'y': -3, 'z': 3})
        print('test_cube_round_negative passed')

    def test_cube_round_positive(self):
        coords = {'x': 1, 'y': 2, 'z': -3}
        self.assertEqual(grid.cube_round(coords), {'x': 1, 'y': 2, 'z': -3})
        print('test_cube_round_positive passed')

    def test_cube_round(self):
        coords = {'x': 0.1, 'y': -0.1, 'z': 0.1}
        self.assertEqual(grid.cube_round(coords), {'x': 0, 'y': 0, 'z': 0})
        print('test_cube_round passed')

class TestHexRangeIntersection(unittest.TestCase):

    def test_hex_range_intersection(self):
        radius = 1
        start_coords = {'x': 0, 'y': 2, 'z': -2}
        end_coords = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(grid.hex_range_intersection(start_coords, radius, end_coords, radius), [{'x': 0, 'y': 1, 'z': -1}])
        print('test_hex_range_intersection passed')

    def test_hex_range_intersection_no_intersection(self):
        radius = 1
        start_coords = {'x': 2, 'y': -1, 'z': 1}
        end_coords = {'x': -2, 'y': 1, 'z': 1}
        self.assertEqual(grid.hex_range_intersection(start_coords, radius, end_coords, radius), [])
        print('test_hex_range_intersection_no_intersection passed')

    def test_hex_range_multiple_intersections(self):
        radius = 1
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 1, 'y': -2, 'z': 1}
        self.assertEqual(grid.hex_range_intersection(start_coords, radius, end_coords, radius), [{'x': 0, 'y': -1, 'z': 1}, {'x': 1, 'y': -1, 'z': 0}])
        print('test_hex_range_multiple_intersections passed')

class TestConversion(unittest.TestCase):
    def test_direction_to_index(self):
        self.assertEqual(grid.direction_to_index('N'), 5)
        self.assertEqual(grid.direction_to_index('NE'), 0)
        self.assertEqual(grid.direction_to_index('SE'), 1)
        self.assertEqual(grid.direction_to_index('S'), 2)
        self.assertEqual(grid.direction_to_index('SW'), 3)
        self.assertEqual(grid.direction_to_index('NW'), 4)
        print('test_direction_to_index passed')

    def test_index_to_direction(self):
        self.assertEqual(grid.index_to_direction(5), 'N')
        self.assertEqual(grid.index_to_direction(0), 'NE')
        self.assertEqual(grid.index_to_direction(1), 'SE')
        self.assertEqual(grid.index_to_direction(2), 'S')
        self.assertEqual(grid.index_to_direction(3), 'SW')
        self.assertEqual(grid.index_to_direction(4), 'NW')
        print('test_index_to_direction passed')

class TestCoordinates(unittest.TestCase):
    def test_get_relative_coordinates(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        direction = 0
        N1 = 1
        N2 = 2
        self.assertEqual(grid.get_relative_coordinates(start_coords, direction, N1), {'x': 1, 'y': -1, 'z': 0})
        self.assertEqual(grid.get_relative_coordinates(start_coords, direction, N2), {'x': 2, 'y': -2, 'z': 0})
        print('test_get_relative_coordinates passed')

    def test_neighbors(self):
        coords = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(grid.neighbors(coords), [{'x': -1, 'y': 0, 'z': 1}, {'x': -1, 'y': 1, 'z': 0}, {'x': 0, 'y': -1, 'z': 1}, {'x': 0, 'y': 1, 'z': -1}, {'x': 1, 'y': -1, 'z': 0}, {'x': 1, 'y': 0, 'z': -1}])
        print('test_neighbors passed')

class TestHexesInPath(unittest.TestCase):
    def test_hexes_in_path(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 0, 'y': 2, 'z': -2}
        self.assertEqual(grid.hexes_in_path(start_coords, end_coords), [{'x': 0, 'y': 0, 'z': 0}, {'x': 0, 'y': 1, 'z': -1}, {'x': 0, 'y': 2, 'z': -2}])
        print('test_hexes_in_path passed')

    def test_hexes_in_path_negative_coords(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 0, 'y': -2, 'z': 2}
        self.assertEqual(grid.hexes_in_path(start_coords, end_coords), [{'x': 0, 'y': 0, 'z': 0}, {'x': 0, 'y': -1, 'z': 1}, {'x': 0, 'y': -2, 'z': 2}])
        print('test_hexes_in_path_negative_coords passed')

    def test_hexes_in_path_multiple_intersections(self):
        start_coords = {'x': 0, 'y': 0, 'z': 0}
        end_coords = {'x': 2, 'y': -2, 'z': 0}
        self.assertEqual(grid.hexes_in_path(start_coords, end_coords), [{'x': 0, 'y': 0, 'z': 0}, {'x': 1, 'y': -1, 'z': 0}, {'x': 2, 'y': -2, 'z': 0}])
        print('test_hexes_in_path_multiple_intersections passed')

if __name__ == "__main__":
    unittest.main()





