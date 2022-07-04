from parse_tle import *
import math


def classify_satellite_by_alt_inc_raan(satellite_groups, satellite):
    altitude_km = math.ceil(satellite['altitude_km'])
    inclination_deg =  math.ceil(satellite['inclination_deg'])
    raan_deg =  math.ceil(satellite['raan_deg'])

    if altitude_km not in satellite_groups:
        satellite_groups[altitude_km] = dict()
    if inclination_deg not in satellite_groups[altitude_km]:
        satellite_groups[altitude_km][inclination_deg] = dict()
    if raan_deg not in satellite_groups[altitude_km][inclination_deg]:
        satellite_groups[altitude_km][inclination_deg][raan_deg] = []

    satellite_groups[altitude_km][inclination_deg][raan_deg].append(satellite)


def get_orbit_reports(satellite_groups):
    groups_by_alt = group_sats_by_altitude(satellite_groups)
    write_alt_reports(groups_by_alt)


def group_sats_by_altitude(satellite_groups):
    sorted_alt = list(satellite_groups.keys())
    sorted_alt.sort()
    bin_range = 50
    groups = []
    # Place satellites on their altitude bin range
    for i in range(0, sorted_alt[-1], bin_range):
        sats = []
        alts_in_range = []
        for alt in sorted_alt:  # Find the right bin range for the altitude
            if alt >= i and alt < i + bin_range:
                alts_in_range.append(alt)
                sats += get_sats_on_alt(satellite_groups, alt)
        orbits = group_sats_in_same_bin_by_orbits(satellite_groups, alts_in_range)
        groups.append(
            {
                'name': '{} - {}'.format(i, i + bin_range),
                'satellites': sats,
                'num_orbits': len(orbits),
                'orbits': orbits,
            }
        )
    return groups


def group_sats_in_same_bin_by_orbits(satellite_groups, alts_in_range):
    """
    If satellites have the same altitude (50 km bin range), inclination angle
    and right ascension of the ascending node (RAAN), they are considered as on the same orbit.
    """
    # Satellites in the same altitude bin are considered in the same altitude.
    # Therefore, reallocate satellites based on inclination degree and RAAN degree.
    new_groups = dict()
    for alt in alts_in_range:
        for inc in satellite_groups[alt].keys():
            # Round inclination degree
            round_inc = round(inc/2.0) * 2
            if round_inc not in new_groups:
                new_groups[round_inc] = dict()
            for raan in satellite_groups[alt][inc].keys():
                # Round raan
                round_raan = round(raan/20.0) * 20
                if round_raan not in new_groups[round_inc]:
                    new_groups[round_inc][round_raan] = []
                new_groups[round_inc][round_raan].append(satellite_groups[alt][inc][raan])

    # Group them into orbit dictionary
    orbits = []
    for inc in sort_dict_keys(new_groups.keys()):
        for raan in sort_dict_keys(new_groups[inc].keys()):
            orbits.append(
                {
                    'inclination_deg': inc,
                    'raan_deg': raan,
                    'satellites': new_groups[inc][raan],
                }
            )
    return orbits


def get_sats_on_alt(satellite_groups, alt):
    sats = []
    inc_degs = satellite_groups[alt].keys()
    for inc in inc_degs:
        raan_degs = satellite_groups[alt][inc].keys()
        for raan in raan_degs:
            sats += satellite_groups[alt][inc][raan]
    return sats


def find_max_min_epoch(satellites):
    min_epoch = {
        'year': float('inf'),
        'days': float('inf'),
    }
    max_epoch = {
        'year': -float('inf'),
        'days': -float('inf'),
    }
    for satellite in satellites:
        satellite_epoch = {
            'year': satellite['epoch_year'],
            'days': satellite['epoch_days'],
        }
        if is_epoch_larger(satellite_epoch, max_epoch):
            max_epoch = satellite_epoch
        if is_epoch_smaller(satellite_epoch, min_epoch):
            min_epoch = satellite_epoch
    return max_epoch, min_epoch


def is_epoch_larger(ep1, ep2):
    if ep1['year'] >= ep2['year'] and ep1['days'] > ep2['days']:
        return True
    else:
        return False


def is_epoch_smaller(ep1, ep2):
    if ep1['year'] <= ep2['year'] and ep1['days'] < ep2['days']:
        return True
    else:
        return False


def write_alt_reports(groups_by_alt):
    with open('tle_reports.txt', 'w') as report:
        report.write('SATELLITES BY ALTITUDES (KM)\n')
        for g in groups_by_alt:
            report.write('> {} KM: {} Satellites\n'.format(g['name'], len(g['satellites'])))

        report.write('\n\n')

        # Wrtie orbit reports for each altitude
        report.write('ORBITS BY ALTITUDE (KM)\n')
        for g in groups_by_alt:
            report.write('> {} KM: {} Orbits\n'.format(g['name'], g['num_orbits']))
            orbit_index = 0
            for orbit in g['orbits']:
                report.write('  >> Orbit {}, Inclination Degree {}, RAAN Degree {}, {} Satellites \n'
                             .format(orbit_index, orbit['inclination_deg'], orbit['raan_deg'], len(orbit['satellites'])))
                orbit_index += 1


def write_satellite_epoch(satellites, max_epoch, min_epoch):
    """
    Write satellite names and epoch to a file.
    """
    max_day_frac, _ = math.modf(max_epoch['days'])
    min_day_frac, _ = math.modf(min_epoch['days'])
    with open('satellite_epoch.txt', 'w') as f:
        f.write('The maximum epoch is year {}, {} days.\n'.format(max_epoch['year'], max_epoch['days']))
        f.write('The minimum epoch is year {}, {} days.\n'.format(min_epoch['year'], min_epoch['days']))
        f.write('The epoch difference is {} years, {} days, {} hours\n\n'.format(
            max_epoch['year'] - min_epoch['year'],
            int(max_epoch['days']) - int(min_epoch['days']),
            (max_day_frac - min_day_frac) * 24.0,
        ))
        for sat in satellites:
            f.write(sat['name'] + '\n')
            f.write('Year: {}\n'.format(sat['epoch_year']))
            f.write('Days: {}\n'.format(sat['epoch_days']))
            f.write('\n')


def sort_dict_keys(keys):
    l = list(keys)
    l.sort()
    return l


def is_end_of_file(name):
    """
    If the file ends properly, the last read of name should be empty.
    """
    return len(name) == 0


if __name__ == '__main__':
    filepath = 'starlink_sullplemental_tles.txt'
    satellite_groups = dict()  # Key: [altitude_km][inclination_deg][raan_deg]
    satellites = []
    with open(filepath, 'r') as f:
        while True:
            name = f.readline()
            tle1 = f.readline()
            tle2 = f.readline()
            if is_end_of_file(name):
                break
            satellite = parse_tle(name, tle1, tle2)
            satellites.append(satellite)
            classify_satellite_by_alt_inc_raan(satellite_groups, satellite)
    max_epoch, min_epoch = find_max_min_epoch(satellites)
    write_satellite_epoch(satellites, max_epoch, min_epoch)
    get_orbit_reports(satellite_groups)
