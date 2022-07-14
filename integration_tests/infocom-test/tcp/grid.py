import numpy as np


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


class Grid:
    def __init__(self):
        self.grid = None
        self.__build_grid()
        self.total_satellite_users = self.__get_total_satellite_users()

    def __build_grid(self):
        """
        Build a grid of world, each grid position contains latitude, longitude
        and satellite user information.
        @return:
        """
        self.grid = []
        for row in range(len(SATELLITE_USERS_GRID)):
            self.grid.append([])
            for col in range(len(SATELLITE_USERS_GRID[row])):
                lat_range, lon_range = self.__get_lat_lon_range(row, col)
                self.grid[row].append({
                    'num_satellite_users': SATELLITE_USERS_GRID[row][col],
                    'lat_range': lat_range,
                    'lon_range': lon_range,
                })

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
        return np.array(self.grid).sum()
