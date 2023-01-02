
from gwpy.timeseries import TimeSeriesDict
import time
import argparse
import tools

# -----
parse = argparse.ArgumentParser(description="CAGMon_LIGO")
parse.add_argument('--stride', '-s', type = int,   help = 'Stride')
parse.add_argument('--data_size',   '-d', type = int,   help = 'Data size')
parse.add_argument('--trigger',     '-t', type = float, help = 'Vetoed primary trigger')
args = parse.parse_args()

data_size = args.data_size
stride = args.stride
trigger = args.trigger
# -----
if args.stride == 1:
    gps_start = int(trigger)
    gps_end = int(trigger) + 1
else :
    gps_start = int(trigger) - stride/2
    gps_end = int(trigger) + stride/2
sample_rate = data_size / stride

main_channel = "H1:GDS-CALIB_STRAIN"
aux_list = tools.aux_channel_list()

print("Retrieving data...")
data = TimeSeriesDict()
main_time = time.time()
data.append(TimeSeriesDict.get(channels = [main_channel], start = gps_start, end = gps_end,
                               verbose = False, frametype = "H1_HOFT_C00",
                               host = 'nds.ligo-wa.caltech.edu').resample(sample_rate))
print("  - Main channel : ", time.time() - main_time)

for i in range(len(aux_list)//500):
    aux_time = time.time()
    data.append(TimeSeriesDict.get(channels = aux_list[i * 500 : (i+1) * 500],
                                   start = gps_start, end = gps_end,
                                   verbose = False, frametype = "H1_R",
                                   host = 'nds.ligo-wa.caltech.edu').resample(sample_rate))
    print("  - Aux channel({}/{}) : ".format((i+1) * 500 , len(aux_list)), time.time() - aux_time)
aux_time = time.time()
data.append(TimeSeriesDict.get(channels = aux_list[5000:len(aux_list)],
                               start = gps_start, end = gps_end,
                               verbose = False, frametype = 'H1_R',
                               host = 'nds.ligo-wa.caltech.edu').resample(sample_rate))
print("  - Aux channels ({}/{}) : ".format(len(aux_list), len(aux_list)), time.time() - aux_time)
data.write("/Users/nims/cagmon_ligo/gwf_data/H_R-t{}-d{}-s{}.gwf".format(trigger, data_size, sample_rate),
           format = 'gwf')