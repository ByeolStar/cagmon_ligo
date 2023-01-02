import gwpy.time
import nds2
from gwpy.timeseries import TimeSeriesDict
import tools
import numpy as np
import warnings
import os
warnings.simplefilter("ignore", UserWarning)

# parameter setting -----
round = 'round1'
date = "2019-07-11"
stride = 1
data_size = 8192
sample_rate = int(data_size / stride)

# -----------------------------
aux_list = tools.aux_channel_list()

with open('/Users/nims/Desktop/data/trigger/{}_{}.rtf'.format(date, round), 'r') as f:
    triggers = list(map(lambda trigger : float(str(trigger).split(' ')[0]), f.readlines()[10:]))

# os.mkdir('/Users/nims/Desktop/data/gwf_data/' + '{}'.format(date))
# os.mkdir('/Users/nims/Desktop/data/gwf_data/' + '{}/{}/'.format(date, round))

server = nds2.connection('nds.ligo-wa.caltech.edu')
for i, trigger in enumerate(triggers):
    if stride == 1 :
        gps_start, gps_end = int(trigger), int(trigger) + 1
    else :
        gps_start, gps_end = int(trigger) - stride/2, int(trigger) + stride/2

    data = TimeSeriesDict()
    print("Retrieving {} data from 'nds.ligo-wa.caltech.edu'".format(trigger))
    data.append(TimeSeriesDict.get(channels = ['H1:GDS-CALIB_STRAIN'], start = gps_start, end = gps_end, verbose = False,
                                   allow_tape = True, frametype = 'H1_HOFT_C00',
                                   host = 'nds.ligo-wa.caltech.edu')).resample(sample_rate)
    print("  - main channel done.")
    aux_index = list(np.arange(11) * 500) + [len(aux_list)]
    for i in range(len(aux_index)-1):
        aux_retrieve = server.fetch(gps_start = gps_start, gps_stop = gps_end, channel_names = aux_list[i:i+1])
        data.append(TimeSeriesDict.from_nds2_buffers(aux_retrieve)).resample(sample_rate)
    print("  - auxiliary channel done.")
    data.write("/Users/nims/Desktop/data/gwf_data/{}/{}/H_R-t{}-d{}-s{}.gwf".format(date, round, trigger, data_size, sample_rate), format = 'gwf')
