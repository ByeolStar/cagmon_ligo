import numpy as np

def aux_channel_list():
    with open('/Users/nims/H1-safe.txt', 'r') as f:
        channels = np.array(list(map(str, f.readlines()[1:])))
    channel_list = list(map(lambda channel: channel.split("DQ")[0] + str("DQ"), channels))
    return channel_list

def trigger_list(date, round):
    with open('/Users/nims/Desktop/data/trigger/{}_{}.rtf'.format(date, round), 'r') as f:
        triggers = list(map(lambda trigger: float(str(trigger).split(' ')[0]), f.readlines()[10:]))
    return triggers