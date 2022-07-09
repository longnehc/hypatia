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
