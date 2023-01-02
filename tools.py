import numpy as np

def aux_channel_list():
    with open('/Users/nims/H1-safe.txt', 'r') as f:
        channels = np.array(list(map(str, f.readlines()[1:])))
    channel_list = list(map(lambda channel: channel.split("DQ")[0] + "DQ", channels))
    return channel_list