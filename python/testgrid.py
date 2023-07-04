# import the Grid class
from grid import Grid
import time

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





