import argparse
import os.path
from tcp import generate_bg_flows_by_user_distribution
from util import util


def main(n_bg_flows, output_path):
    # if cache file already exists, print message and return immediately
    if os.path.exists(output_path):
        print('Cache file already exists at {}. Nothing is generated.'.format(output_path))
        return

    gen_data_path = 'temp/gen_data/starlink_550_isls_none_infocom_test'

    # Get start id
    description = util.read_config_file(gen_data_path + '/description.txt', '=')
    num_orbits = int(description['num_orbits'])
    num_satellites_per_orbit = int(description['num_satellites_per_orbit'])
    start_id = num_orbits * num_satellites_per_orbit

    ep_pairs = generate_bg_flows_by_user_distribution(
        n_bg_flows,
        gs_path=gen_data_path + '/ground_stations.txt',
        start_id=start_id,
    )

    with open(output_path, 'w') as f:
        for ep in ep_pairs:
            f.write('{}, {}\n'.format(ep[0], ep[1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate end-point pairs')
    parser.add_argument('--output_path', action="store", dest="output_path", default='./ep_pairs_cache.txt', type=str)
    parser.add_argument('--n_bg_flows', action="store", dest='n_bg_flows', default=100, type=int)
    args = parser.parse_args()

    main(args.n_bg_flows, args.output_path)
