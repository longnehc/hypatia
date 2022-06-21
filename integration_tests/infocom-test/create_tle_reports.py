from parse_tle import *
import matplotlib.pyplot as plt
import numpy as np


def get_orbit_reports(satellite_groups):
    groups_by_alt = group_sats_by_altitude(satellite_groups)
    write_reports(groups_by_alt)


def group_sats_by_altitude(satellite_groups):
    sorted_alt = list(satellite_groups.keys())
    sorted_alt.sort()
    bin_range = 50
    groups = []
    # Place satellites on their altitude bin range
    for i in range(0, sorted_alt[-1], bin_range):
        sats = []
        for alt in sorted_alt:  # Find the right bin range for the altitude
            if alt >= i and alt < i + bin_range:
                sats += get_sats_on_alt(satellite_groups, alt)
        groups.append(
            {
                'name': '{} - {}'.format(i, i + bin_range),
                'satellites': sats,
            }
        )
    return groups


def get_sats_on_alt(satellite_groups, alt):
    sats = []
    inc_degs = satellite_groups[alt].keys()
    for inc in inc_degs:
        raan_degs = satellite_groups[alt][inc].keys()
        for raan in raan_degs:
            sats += satellite_groups[alt][inc][raan]
    return sats


def write_reports(groups_by_alt):
    with open('tle_reports.txt', 'w') as report:
        report.write('SATELLITES BY ALTITUDES (KM)\n')
        for g in groups_by_alt:
            report.write('> {} KM: {} Satellites\n'.format(g['name'], len(g['satellites'])))


if __name__ == '__main__':
    filepath = 'starlink_tles/starlink_sullplemental_tles.txt'
    satellite_groups = dict()  # Key: [altitude_km][inclination_deg][raan_deg]
    
    with open(filepath, 'r') as f:
        while True:
            name = f.readline()
            tle1 = f.readline()
            tle2 = f.readline()

            if is_end_of_file(name):
                break

            satellite = parse_tle(name, tle1, tle2)
            classify_satellite(satellite_groups, satellite)
    
    get_orbit_reports(satellite_groups)
