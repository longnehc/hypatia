from glob import glob
import pandas as pd

ground_station_path = './temp/gen_data/starlink_550_isls_plus_grid_infocom_test/ground_stations.txt'
GS_data = pd.read_csv(ground_station_path, usecols=[0,1], names=['index', 'location'], index_col=False)

files = glob('./temp/runs/*')

result = []

for file in files:
  GS_pair = file.replace('./temp/runs/starlink_550_isls_plus_grid_', '').replace('_tcp', '')
  scr_GS = GS_pair.split('_')[0]
  scr_GS = GS_data[GS_data['index'] == int(scr_GS)]['location'].values[0]
  dst_GS = GS_pair.split('_')[1]
  dst_GS = GS_data[GS_data['index'] == int(dst_GS)]['location'].values[0]

  with open(file + "/logs_ns3/pingmesh.txt") as f:
    lines = f.readlines()
  argu_list = [x for x in lines[1].replace('ms', '').replace('\n', '').split(' ') if x != '']
  argu_list = argu_list[2:]
  argu_list[-2] = argu_list[-2] + ' ' + argu_list[-1]
  argu_list = argu_list[:-1]

  # print(argu_list)
  # exit(0)

  argu_list = [scr_GS, dst_GS] + argu_list

  result.append(argu_list)

result = pd.DataFrame(result, columns=['Source', 'Destination', 'Mean latency there', 'Mean latency back', 
                                       'Min. RTT', 'Mean RTT', 'Max. RTT', 'Smp.std. RTT', 'Reply arrival'])

result['Mean RTT'] = [float(x) for x in result['Mean RTT']]

print(result.sort_values(by=['Mean RTT']))
