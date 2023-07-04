#!/usr/bin/env python
# coding: utf-8

import math
import json
import heapq
from queue import PriorityQueue

def lerp(a, b, t):
    """Linear interpolation."""
    return a + (b - a) * t

def movement_table(orientation='flat'):
    if orientation == 'flat':
        # Clockwise starting from East direction for flat-top hexagon
        directions = [(1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, 1, -1), (1, 0, -1)]
    elif orientation == 'pointy':
        # Clockwise starting from Northeast direction for pointy-top hexagon
        directions = [(1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, 1, -1)]
    else:
        raise ValueError('Invalid orientation. Choose either "flat" or "pointy".')

    movement_table = {}
    for i, direction in enumerate(directions):
        movement_table[i] = direction
    return movement_table


class Grid:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.grid = self.create_hex_grid()

    def create_hex_grid(self):
        """Create a hexagon grid."""
        grid = []
        for x in range(-self.x_size, self.x_size + 1):
            for y in range(max(-self.y_size, -x - self.y_size), min(self.y_size, -x + self.y_size) + 1):
                z = -x-y
                grid.append({
                    'coordinates': {
                        'x': x,
                        'y': y,
                        'z': z
                    },
                    'properties': {}
                })
        return grid
    
    def get_hexagon(self, coords):
        """Get the entire hexagon data given its coordinates."""
        for hexagon in self.grid:
            if hexagon['coordinates'] == coords:
                return hexagon
        return None
    
    def hexes_in_range(self, center_coords, N, exclude_center=False):
        """Get a list of hexes within a range of a center hex. Can exclude the center hex."""
        results = []
        for dx in range(-N, N+1):
            for dy in range(max(-N, -dx-N), min(N, -dx+N)+1):
                dz = -dx-dy
                coords = {'x': center_coords['x'] + dx, 'y': center_coords['y'] + dy, 'z': center_coords['z'] + dz}
                # If excluding center, skip the center hex
                if exclude_center and coords == center_coords:
                    continue
                results.append(coords)
        return results
    
    def neighbors(self, coords):
        """Get the neighbors of a hexagon."""
        return self.hexes_in_range(coords, 1, exclude_center=True)

    def get_properties(self, coordinates, prop=None):
        """Get the properties of a hexagon."""
        for hexagon in self.grid:
            if hexagon['coordinates'] == coordinates:
                if prop:
                    return {k: hexagon['properties'].get(k, None) for k in prop}
                else:
                    return hexagon['properties']
        return None

    def set_properties(self, coordinates, prop):
        """Set the properties of a hexagon."""
        for hexagon in self.grid:
            if hexagon['coordinates'] == coordinates:
                hexagon['properties'].update(prop)
                return True
        return False
    
    def get_relative_coordinates(self, start_coords, direction, N):
        """Get the coordinates of a hexagon relative to another hexagon."""
        dq, dr, ds = movement_table()[direction]
        new_coords = {
            'x': start_coords['x'] + dq * N,
            'y': start_coords['y'] + dr * N,
            'z': start_coords['z'] + ds * N
        }
        return new_coords
    
    def cube_distance(self, start_coords, end_coords):
        """Get the distance between two hexes in cube coordinates."""
        return max(abs(start_coords['x'] - end_coords['x']), abs(start_coords['y'] - end_coords['y']), abs(start_coords['z'] - end_coords['z']))
    
    def cube_round(self, cube):
        """Round cube coordinates to the nearest hexagon coordinates."""
        rx = round(cube['x'])
        ry = round(cube['y'])
        rz = round(cube['z'])
        
        x_diff = abs(rx - cube['x'])
        y_diff = abs(ry - cube['y'])
        z_diff = abs(rz - cube['z'])
        
        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry-rz
        elif y_diff > z_diff:
            ry = -rx-rz
        else:
            rz = -rx-ry

        return {'x': rx, 'y': ry, 'z': rz}
    
    def hexes_in_path(self, start_coords, end_coords):
        """Get a list of hexes in a line between two hexes."""
        N = self.cube_distance(start_coords, end_coords)
        results = []
        for i in range(0, N+1):
            t = 1.0/N * i
            cube = {
                'x': lerp(start_coords['x'], end_coords['x'], t),
                'y': lerp(start_coords['y'], end_coords['y'], t),
                'z': lerp(start_coords['z'], end_coords['z'], t)
            }
            results.append(self.cube_round(cube))
        return results
    
    def hex_range_intersection(self, center_a, range_a, center_b, range_b):
        a_list = self.hexes_in_range(center_a, range_a)
        b_list = self.hexes_in_range(center_b, range_b)
        return [hexagon for hexagon in a_list if hexagon in b_list]
  
    def flood_fill(self, center_coords, N):
        """Get a list of hexes within a range of a center hex that are not obstacles."""
        fringes = []
        for k in range(N+1):
            fringes.append([])

        # The start hexagon is at distance 0
        fringes[0].append(center_coords)

        for k in range(1, N+1):
            for hex_coords in fringes[k-1]:
                # Check the neighbors of this hexagon
                for direction in range(6):
                    # Calculate the coordinates of the neighboring hex
                    neighbor_coords = self.get_relative_coordinates(hex_coords, direction, 1)

                    # Check if this hex is already in a fringe
                    if any(neighbor_coords in fringe for fringe in fringes):
                        continue
                    
                    # Check if this hex is an obstacle
                    hex_properties = self.get_properties(neighbor_coords)
                    if hex_properties.get('obstacle', False):
                        continue

                    # This hex is not an obstacle and not yet in a fringe, so we add it to the current fringe
                    fringes[k].append(neighbor_coords)

        return fringes
    
    def update_properties_from_list(self, hex_list):
        """Updates the properties of each hex in the grid from a list of hexagon objects."""
        for hex_obj in hex_list:
            # Ensure the object has the required keys
            if 'coordinates' in hex_obj and 'properties' in hex_obj:
                self.set_properties(hex_obj['coordinates'], hex_obj['properties'])
            else:
                raise ValueError("Hexagon object must contain 'coordinates' and 'properties' keys.")
        return self.grid
    
    def direction_to_index(self, direction_str, orientation='flat'):
        print(direction_str, orientation)
        """Convert a string direction to its corresponding index in the movement table."""
        # Define mapping for flat orientation
        if orientation == 'flat':
            direction_mapping = {
                'NE': 0,
                'SE': 1,
                'S': 2,
                'SW': 3,
                'NW': 4,
                'N': 5
            }
        elif orientation == 'pointy':
            direction_mapping = {
                'NE': 0,
                'E': 1,
                'SE': 2,
                'SW': 3,
                'W': 4,
                'NW': 5
            }
        else:
            raise ValueError('Invalid orientation. Choose either "flat" or "pointy".')
        
        if direction_str not in direction_mapping:
            raise ValueError(f"Invalid direction. Choose from {list(direction_mapping.keys())}.")
        
        return direction_mapping[direction_str]

    def index_to_direction(self, direction_index, orientation='flat'):
        """Convert an index in the movement table to its corresponding string direction."""
        # Define mapping for flat orientation
        if orientation == 'flat':
            index_mapping = {
                0: 'NE',
                1: 'SE',
                2: 'S',
                3: 'SW',
                4: 'NW',
                5: 'N'
            }
        elif orientation == 'pointy':
            index_mapping = {
                0: 'NE',
                1: 'E',
                2: 'SE',
                3: 'SW',
                4: 'W',
                5: 'NW'
            }
        else:
            raise ValueError('Invalid orientation. Choose either "flat" or "pointy".')

        if direction_index not in index_mapping:
            raise ValueError(f"Invalid index. Choose from {list(index_mapping.keys())}.")

        return index_mapping[direction_index]


    def to_json(self):
        return json.dumps(self.grid)