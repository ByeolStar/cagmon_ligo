import nds2
from gwpy.timeseries import TimeSeriesDict
import tools
import argparse
import numpy as np
import tqdm
# argparse setting ------
parse = argparse.ArgumentParser(description = 'CAGMon_LIGO')
parse.add_argument('--stride', '-s', type = int,   help = 'Stride')
parse.add_argument('--data_size',   '-d', type = int,   help = 'Data size')
parse.add_argument('--trigger',     '-t', type = float, help = 'Vetoed primary trigger')
args = parse.parse_args()
# -----------------------

# basic parameter setting -----
data_size = args.data_size
stride = args.stride
trigger = args.trigger

if args.stride == 1:
    gps_start = int(trigger)
    gps_end = int(trigger) + 1
else :
    gps_start = int(trigger) - stride/2
    gps_end = int(trigger) + stride/2
sample_rate = data_size / stride

main_channel = "H1:GDS-CALIB_STRAIN"
aux_list = tools.aux_channel_list()

# -----------------------------

server = nds2.connection('nds.ligo-wa.caltech.edu')

data = TimeSeriesDict()
print("Retrieving data from 'nds.ligo-wa.caltech.edu'")
data.append(TimeSeriesDict.get(channels = ['H1:GDS-CALIB_STRAIN'], start = gps_start, end = gps_end, verbose = False,
                               allow_tape = True, frametype = 'H1_HOFT_C00',
                               host = 'nds.ligo-wa.caltech.edu')).resample(sample_rate)
print("  - main channel done.")
aux_index = list(np.arange(11) * 500) + [len(aux_list)]
for i in tqdm.tqdm(range(len(aux_index)-1)):
    aux_retrieve = server.fetch(gps_start = gps_start, gps_stop = gps_end, channel_names = aux_list[i:i+1])
    data.append(TimeSeriesDict.from_nds2_buffers(aux_retrieve)).resample(sample_rate)
print("  - auxiliary channel done.")
data.write("/Users/nims/Desktop/data/gwf_data/H_R-t{}-d{}-s{}.gwf".format(trigger, data_size, sample_rate), format = 'gwf')