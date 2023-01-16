import nds2
from gwpy.timeseries import TimeSeriesDict
import Read_files
import numpy as np
import tqdm
import os

class retrieve:
    def __init__(self, round_winner, date, path = '/Users/nims/Desktop/CAGMon_LIGO/'):
        self.winner = round_winner
        self.date   = date
        self.path   = path

    def trigger(self, stride, site='nds.ligo-wa.caltech.edu'):
        self.site   = site
        self.stride = stride

        trigger_times  = Read_files.filetype(self.winner, self.date).types("trigger")
        safe_channels  = Read_files.filetype(self.winner, self.date).types("safe")

        path = self.path + self.date + '/data/trigger/'
        for tri_index, trigger in enumerate(trigger_times):
            if os.path.isfile(path + f"trigger_{trigger}.gwf") == True : print(f"  - {trigger} passed")
            else :
                if self.stride == 1:
                    start, end = int(trigger), int(trigger) + 1
                else :
                    start, end = int(int(trigger) - stride/2), int(int(trigger) + stride/2)

                print(f"({tri_index+1}/{len(trigger_times)}) Retrieve trigger data...")
                data = TimeSeriesDict()
                main_data = TimeSeriesDict.get(channels=["H1:GDS-CALIB_STRAIN"], start=start, end=end,
                                               frametype="H1_HOFT_C00", allow_tape=True).resample(8192*self.stride)
                data.append(main_data)

                slicing = list(np.arange(11) * 500) + [len(safe_channels)]
                for i in tqdm.trange(len(slicing)-1):
                    aux_data = TimeSeriesDict.get(channels=safe_channels[slicing[i]:slicing[i+1]], start=start, end=end,
                                                  frametype='H1_R', allow_tape=True).resample(8192*self.stride)
                    data.append(aux_data)
                    data.write(path + f"trigger_{trigger}.gwf", format = 'gwf')
                print(f"  - {trigger} Done.")

    def normal(self, stride, site='nds.ligo-wa.caltech.edu'):
        self.site   = site
        self.stride = stride

        trigger_times  = Read_files.filetype(self.winner, self.date).types("trigger")
        safe_channels  = Read_files.filetype(self.winner, self.date).types("safe")

        path = self.path + self.date + '/data/normal/'
        for tri_index, trigger in enumerate(trigger_times):
            if os.path.isfile(path + f"trigger_{trigger}.gwf") == True : print(f"  - {trigger} passed")
            else :
                if self.stride == 1:
                    start, end = int(trigger), int(trigger) + 1
                else :
                    start, end = int(int(trigger) - stride/2), int(int(trigger) + stride/2)

                print(f"({tri_index+1}/{len(trigger_times)}) Retrieve trigger data...")
                data = TimeSeriesDict()
                main_data = TimeSeriesDict.get(channels=["H1:GDS-CALIB_STRAIN"], start=start, end=end,
                                               frametype="H1_HOFT_C00", allow_tape=True).resample(8192*self.stride)
                data.append(main_data)

                slicing = list(np.arange(11) * 500) + [len(safe_channels)]
                for i in tqdm.trange(len(slicing)-1):
                    aux_data = TimeSeriesDict.get(channels=safe_channels[slicing[i]:slicing[i+1]], start=start, end=end,
                                                  frametype='H1_R', allow_tape=True).resample(8192*self.stride)
                    data.append(aux_data)
                    data.write(path + f"trigger_{trigger}.gwf", format = 'gwf')
                print(f"  - {trigger} Done.")



