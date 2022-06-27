# This script tests if the epoch of the observer object will change
# the distance between the satellite.

import sys
sys.path.append("../../../satgenpy")
import ephem
from satgen.tles import *


# Use a Hypatia's artificial generate TLE
TLE = ['Starlink-550',
       '1 00001U 00000ABC 00001.00000000  .00000000  00000-0  00000+0 0    04',
       '2 00001  53.0000   0.0000 0000001   0.0000   0.0000 15.19000000    08']

# Example of epoch_str: '2000-01-01 00:00:00.000'
epochs = [
    '2000-01-01 00:00:00.000',
    '2000-01-02 03:00:00.000',
    '2000-01-04 12:30:10.000',
    '2000-01-01 16:21:00.000',
    '2010-01-05 12:30:12.120',
]

# Example of date_str: '2000-01-01 00:00:00.000'
dates = [
    '2000-01-01 00:00:00.000',
    '2000-01-02 03:00:00.000',
    '2000-01-04 12:30:10.000',
    '2000-01-01 16:21:00.000',
    '2000-01-05 12:30:12.120',
]


gs = {
    'gid': 0,
    'name': 'Tokyo',
    'latitude_degrees_str': '35.689500',
    'longitude_degrees_str': '139.691710',
    'elevation_m_float': 0.0,
    'cartesian_x': -3954843.592378,
    'cartesian_y': 3354935.154958,
    'cartesian_z': 3700263.820217
}


def diff_epoch_same_date():
    distances = []
    for epoch in epochs:
        observer = ephem.Observer()
        observer.epoch = epoch
        observer.date = dates[0]  # Fixed date string
        observer.lat = str(gs["latitude_degrees_str"])  # Very important: string argument is in degrees.
        observer.lon = str(gs["longitude_degrees_str"])  # DO NOT pass a float as it is interpreted as radians
        observer.elevation = gs["elevation_m_float"]

        satellite = ephem.readtle(TLE[0], TLE[1], TLE[2])

        # Compute distance from satellite to observer
        satellite.compute(observer)
        distances.append(satellite.range)

    print('DIFFERENT EPOCH, SAME DATE')
    if are_dist_same(distances):
        print('> Distances are the same.')
    else:
        print('> Distances are **NOT** the same.')
    write_dist_result(distances, filename='observer_diff_epoch_same_date.txt')


def same_epoch_diff_date():
    distances = []
    for date in dates:
        observer = ephem.Observer()
        observer.epoch = epochs[0]  # Fixed epoch string
        observer.date = date
        observer.lat = str(gs["latitude_degrees_str"])  # Very important: string argument is in degrees.
        observer.lon = str(gs["longitude_degrees_str"])  # DO NOT pass a float as it is interpreted as radians
        observer.elevation = gs["elevation_m_float"]

        satellite = ephem.readtle(TLE[0], TLE[1], TLE[2])

        # Compute distance from satellite to observer
        satellite.compute(observer)
        distances.append(satellite.range)

    print('SAME EPOCH, DIFFERENT DATE')
    if are_dist_same(distances):
        print('> Distances are the same.')
    else:
        print('> Distances are **NOT** the same.')
    write_dist_result(distances, filename='observer_same_epoch_diff_date.txt')


def are_dist_same(distances):
    first_dist = distances[0]
    for dist in distances:
        if dist != first_dist:
            return False
    return True


def write_dist_result(distances, filename='observer_epoch.txt'):
    with open(filename, 'w') as f:
        for dist in distances:
            f.write('{}\n'.format(dist))


if __name__ == '__main__':
    diff_epoch_same_date()
    same_epoch_diff_date()
