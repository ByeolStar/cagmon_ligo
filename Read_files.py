import numpy as np

class filetype:
    def __init__(self, round_winner, date, path='/Users/nims/Desktop/CAGMon_LIGO/'):
        self.path   = path if path[-1] == '/' else path + '/'
        self.winner = round_winner
        self.date   = date
    def types(self, types):
        self.types = types
        if self.types == 'safe':
            path = self.path + 'H1-raw-safe.txt'
            with open(path, 'r') as f:
                safe_channels = list(map(lambda x : str(x.split('DQ')[0] + "DQ"), f.readlines()[1:]))
            return safe_channels

        elif self.types == 'trigger':
            path = self.path + self.date + '/round_trigger/' + f'{self.winner}_vetoed_primary_triggers.txt'
            with open(path, 'r') as f:
                trigger_times = list(map(lambda x : float(str(x).split(' ')[0]), f.readlines()[1:]))
            return trigger_times



