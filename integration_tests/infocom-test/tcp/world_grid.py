import numpy as np
import random


"""
This SATELLITE_USERS_GRID grid adapts the same setting from
@ARTICLE{7572177,
author={Yang, Yuan and Xu, Mingwei and Wang, Dan and Wang, Yu},
journal={IEEE Journal on Selected Areas in Communications},
title={Towards Energy-Efficient Routing in Satellite Networks},
year={2016},  volume={34},  number={12},  pages={3869-3886},
doi={10.1109/JSAC.2016.2611860}}
"""
SATELLITE_USERS_GRID = [
    [0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [5, 17, 19, 2, 2, 2, 2, 2, 1, 1, 1, 1, 4, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [1, 17, 0, 19, 19, 19, 19, 19, 2, 0, 0, 46, 178, 76, 16, 6, 6, 6, 5, 6, 72, 5, 5, 1],
    [1, 0, 0, 17, 32, 17, 17, 17, 0, 0, 1, 51, 52, 75, 71, 27, 41, 70, 67, 134, 151, 38, 0, 0],
    [0, 17, 0, 0, 15, 33, 38, 24, 0, 0, 1, 13, 3, 15, 22, 37, 115, 116, 118, 156, 149, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 26, 24, 15, 0, 0, 13, 99, 5, 27, 1, 1, 94, 40, 39, 34, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 10, 31, 14, 14, 0, 1, 2, 5, 31, 1, 0, 0, 10, 10, 13, 13, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 18, 21,14, 0, 1, 1, 15, 14, 1, 0, 0, 0, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 10, 22, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 2, 2, 2, 2, 4],
    [0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class WorldGrid:
    def __init__(self, users_grid):
        self.users_grid = users_grid
        self.__build_grid()

    def __build_grid(self):
        """
        Build a grid of world, each grid position contains latitude, longitude
        and satellite user information.
        """
        self.grid_1d = []
        self.grid_2d = []
        self.grid_1d_weights = []
        self.total_satellite_users = self.__get_total_satellite_users()
        for row in range(len(self.users_grid)):
            self.grid_2d.append([])
            for col in range(len(self.users_grid[row])):
                lat_range, lon_range = self.__get_lat_lon_range(row, col)
                grid_position = {
                    'num_satellite_users': self.users_grid[row][col],
                    'lat_range': lat_range,
                    'lon_range': lon_range,
                    'latitude': (lat_range[1] + lat_range[0]) / 2,
                    'longitude': (lon_range[1] + lon_range[0]) / 2,
                    'weights': self.users_grid[row][col] / self.total_satellite_users,
                }
                self.grid_2d[row].append(grid_position)
                self.grid_1d.append(grid_position)
                self.grid_1d_weights.append(grid_position['weights'])

    @staticmethod
    def __get_lat_lon_range(row, col):
        """
        @param row: the row of the grid.
        @param col: the col of the grid.
        @return: the range of latitude and longitude for the given row and col.
                 (latitude_start, latitude_end), (longitude_start, longitude_end)
        """
        # These start values are based on our grid
        lat_on_first_row = 90
        lon_on_first_col = -180
        lat_increment = -15
        lon_increment = 15

        lat_start = lat_on_first_row + row * lat_increment
        lat_end = lat_start + lat_increment
        lon_start = lon_on_first_col + col * lon_increment
        lon_end = lon_start + lon_increment

        # Sort the range to have the smaller value on the left for convenience
        lat_range = sorted((lat_start, lat_end))
        lon_range = sorted((lon_start, lon_end))

        return lat_range, lon_range

    def __get_total_satellite_users(self):
        return np.array(self.users_grid).sum()

    def random_select_grid_position(self, n):
        return random.choices(self.grid_1d, weights=self.grid_1d_weights, k=n)


def get_world_grid():
    """
    Initialize a world grid class and return it.
    @return: a WorldGrid object
    """
    return WorldGrid(SATELLITE_USERS_GRID)
