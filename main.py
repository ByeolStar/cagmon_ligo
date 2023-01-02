import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeriesDict, TimeSeries
from gwpy.detector import ChannelList
import tools
# parameter setting -----
round = 'round1'
date = '2019-07-11'
data_size = 8192
sample_rate = 8192
# ----- ----- ----- -----
triggers = tools.trigger_list(date = date, round = round)
channels = ["H1:GDS-CALIB_STRAIN"] + tools.aux_channel_list()
path = '/Users/nims/Desktop/data/gwf_data/{}/{}/'.format(date, round)
for trigger in triggers:
    file_name = 'H_R-t{}-d{}-s{}.gwf'.format(trigger, data_size, sample_rate)
    data = TimeSeriesDict.read(path+file_name, channels = channels, format = 'gwf')
    print(data)