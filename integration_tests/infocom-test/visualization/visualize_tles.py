import argparse
import ephem
import math
import os


topFile = "static_html/top.html"
bottomFile = "static_html/bottom.html"
OUT_HTML_FILE = "tles_visualization.html"


def load_satellites_from_tles(tles_filepath, epoch):
    with open(tles_filepath, 'r') as f:
        # Assuming reading Hypatia's TLE file format
        f.readline()  # Skip number of satellite per orbits and number of orbits
        satellites = []
        for name in f:
            tle_line_1 = f.readline()
            tle_line_2 = f.readline()
            satellite = ephem.readtle(name, tle_line_1, tle_line_2)

            # If epoch is None, use the next day of the first satellite's epoch
            if epoch is None:
                # Change it to the next day 00:00:00
                epoch = ephem.Date(math.floor(satellite.epoch) + 0.5)

            satellite.compute(epoch)
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
    print('Please open {} file to see the visualization.\n'.format(OUT_HTML_FILE))


if __name__ == "__main__":
    if os.path.exists(OUT_HTML_FILE):
        os.remove(OUT_HTML_FILE)
    parser = argparse.ArgumentParser(description='Visualize the given TLEs constellation.')
    parser.add_argument('--tle', action="store",
                        help="The file path for the TLE file.",
                        dest="tle", type=str)
    parser.add_argument('--epoch', action="store",
                        help="Optional. E.g., 2022-06-21 01:20:00, the datetime for the TLEs to visualize. "
                             + "The default value is the next day 00:00:00 of the first satellite's epoch.",
                        default=None, dest="epoch", type=str)
    args = parser.parse_args()

    _satellites = load_satellites_from_tles(args.tle, args.epoch)
    _viz_string = get_viz_string(_satellites)
    write_viz_files(_viz_string)
