def convert_to_hypatia_tles(filepath, output_dir='.'):
    """
    Convert the TLE file obtained from https://celestrak.com/ to
    Hypatia's TLE file format.
    """
    output_lines = []
    output_lines.append('num_orbits num_sat_per_orbit')  # Placeholder
    sat_id = 0
    with open(filepath, 'r') as f:
        for line in f:
            name = clean_string(line.strip() + ' ' + str(sat_id))
            name = clean_name(name)
            output_lines.append(name)  # Satellite name and ID
            output_lines.append(clean_string(f.readline()))  # TLE line 1
            output_lines.append(clean_string(f.readline()))  # TLE line 2
            sat_id += 1
    # Since we are using GSL only algorithm, and supplemental TLEs do not always
    # have the same number of satellites across all orbits, we use this trick
    # to match the total number of satellites: num_orbits * num_sat_per_orbit
    output_lines[0] = clean_string('{} {}'.format(1, sat_id))

    with open(output_dir + '/tles.txt', 'w') as f:
        for line in output_lines:
            f.write(line)


def clean_string(s):
    return s.replace('\n', '').strip() + '\n'


def clean_name(name):
    # The name contains a white space
    split_name = name.split()
    if len(split_name) == 3:
        return split_name[0] + split_name[1] + ' ' + split_name[2] + '\n'
    return name


def count_sat_in_tles(filepath):
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            f.readline()
            f.readline()
            count += 1
    return count


if __name__ == '__main__':
    filepath = 'starlink_supplemental_tles.txt'
    convert_to_hypatia_tles(filepath)
