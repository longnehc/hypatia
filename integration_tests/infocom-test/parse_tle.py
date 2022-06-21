from sgp4.api import Satrec
import math


# The radius of Earth in km
R = 6371.0


def parse_tle(name, tle1, tle2):
    satellite = dict()
    satellite['name'] = name.replace('\n', '').strip()
    satrec = Satrec.twoline2rv(tle1, tle2)

    # Retrieve satellite information
    satellite['altitude_km'] = satrec.altp * R  # Use altitude of the perigee
    satellite['inclination_deg'] = math.degrees(satrec.im)
    satellite['raan_deg'] = math.degrees(satrec.Om)

    return satellite


def is_end_of_file(name):
    """
    If the file ends properly, the last read of name should be empty.
    """
    return len(name) == 0


def classify_satellite(satellite_groups, satellite):
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
