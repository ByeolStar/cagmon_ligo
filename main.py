import numpy as np
import nds2
from gwpy.timeseries import TimeSeriesDict as TSD
from gwpy.time import tconvert
import argparse
import Settings
import Read_files
import Retrieve

args = argparse.ArgumentParser(description = "Retrieve LIGO Data from nds")
args.add_argument("--round",  "-r",    type = int,  help = "Round number")
args.add_argument("--date",   "-d",    type = str,  help = "yyyy-mm-dd style date")
args.add_argument("--normal", "-n",    type = bool, help = "additional download to normal state LIGO data")
args.add_argument("--stride", "-s",    type = int,  help = "Data segment from each gps trigger/normal time")
parse = args.parse_args()

round_winner = "round" + str(parse.round)
date = parse.date

site1 = 'nds.ligo.caltech.edu'
site2 = 'nds.ligo-wa.caltech.edu'

Settings.directory(round_winner, date).make_directory()
Settings.directory(round_winner, date).check_list()

Retrieve.retrieve(round_winner, date).trigger(3)

