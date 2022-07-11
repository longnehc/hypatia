def count_gs_in_file(filepath):
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count


def count_sat_in_tles(filepath):
    count = 0
    with open(filepath, 'r') as f:
        f.readline()  # Skip num_orbits and num_sat_per_orbit
        for line in f:
            f.readline()
            f.readline()
            count += 1
    return count


def get_config_value(filepath, key):
    # For infocom-test, read some values from description.txt
    with open(filepath, 'r') as f:
        for line in f:
            _key, value = parse_properties_line(line)
            if key == _key:
                return value


def parse_properties_line(line):
    """
    Given a properties line: key=value,
    return key and value
    """
    key_value = line.strip().split('=')
    return key_value[0], key_value[1]  # key, value
