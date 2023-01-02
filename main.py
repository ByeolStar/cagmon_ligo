
from gwpy.timeseries import TimeSeriesDict
import time
import argparse
import tools

# -----
parse = argparse.ArgumentParser(description="CAGMon_LIGO")
parse.add_argument('--sample_rate', '-s', type = int,   help = 'Sampling rate')
parse.add_argument('--data_size',   '-d', type = int,   help = 'Data size')
parse.add_argument('--trigger',     '-t', type = float, help = 'Vetoed primary trigger')
args = parse.parse_args()

data_size = args.data_size
sample_rate = args.sample_rate
trigger = args.trigger
# -----
gps_start = int(trigger) - (data_size/sample_rate)/2
gps_end = int(trigger) + (data_size/sample_rate)/2

main_channel = "H1:GDS-CALIB_STRAIN"
aux_list = tools.aux_channel_list()

print("Retrieving data...")
data = TimeSeriesDict()
main_time = time.time()
data.append(TimeSeriesDict.get(channels = [main_channel], start = gps_start, end = gps_end,
                               verbose = False, frametype = "H1_HOFT_C00", port = 31200,
                               host = 'nds.ligo-wa.caltech.edu').resample(sample_rate))
print("  - Main channel : ", time.time() - main_time)

index_list = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, len(aux_list)]
for i in range(len(index_list)-1):
    aux_time = time.time()
    data.append(TimeSeriesDict.get(channels = aux_list[index_list[i]:index_list[i+1]],
                                   start = gps_start, end = gps_end,
                                   verbose = False, frametype = "H1_R", port = 31200,
                                   host = 'nds.ligo-wa.caltech.edu').resample(sample_rate))
    print("  Aux channel({}/{}) : ".format(index_list[i+1], len(aux_list)), time.time() - aux_time)

data.write("/Users/nims/cagmon_ligo/gwf_data/H_R-t{}-d{}-s{}.gwf".format(trigger, data_size, sample_rate),
           format = 'gwf')