import ephem
import math


FILENAME_TLES = "../tles.txt"
topFile = "static_html/top.html"
bottomFile = "static_html/bottom.html"
OUT_HTML_FILE = "tles_visualization.html"
EPOCH = "2022-06-21 01:20:00"


def load_satellites_from_tles(filename_tles):
    with open(filename_tles, 'r') as f:
        # Assuming reading Hypatia's TLE file format
        f.readline()  # Skip number of satellite per orbits and number of orbits
        satellites = []
        for name in f:
            tle_line_1 = f.readline()
            tle_line_2 = f.readline()
            satellite = ephem.readtle(name, tle_line_1, tle_line_2)
            satellite.compute(EPOCH)
            satellites.append(
                {
                    'sat_obj': satellite,
                    'alt_km': satellite.elevation / 1000.0,
                    'orb_id': 0,  # May not needed
                    'orb_sat_id': 0,  # May not needed
                }
            )
    return satellites


def get_viz_string(satellites):
    viz_string = ""
    for j in range(len(satellites)):
        viz_string += "var redSphere = viewer.entities.add({name : '', position: Cesium.Cartesian3.fromDegrees(" \
                      + str(math.degrees(satellites[j]["sat_obj"].sublong)) + ", " \
                      + str(math.degrees(satellites[j]["sat_obj"].sublat)) + ", " + str(
            satellites[j]["alt_km"] * 1000) + "), " \
                      + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                      + "material : Cesium.Color.BLACK.withAlpha(1),}});\n"
    return viz_string


def write_viz_files(viz_string):
    with open(OUT_HTML_FILE, 'w') as f_html:
        # Write top file to the output html first
        with open(topFile, 'r') as f_top:
            f_html.write(f_top.read())
        f_html.write(viz_string)
        # Then, write the bottom file to the output html
        with open(bottomFile, 'r') as f_bottom:
            f_html.write(f_bottom.read())


if __name__ == "__main__":
    _satellites = load_satellites_from_tles(FILENAME_TLES)
    _viz_string = get_viz_string(_satellites)
    write_viz_files(_viz_string)
