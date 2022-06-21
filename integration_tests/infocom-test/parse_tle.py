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
