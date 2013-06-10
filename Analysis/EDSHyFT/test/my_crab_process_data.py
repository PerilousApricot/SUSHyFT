#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
    'data_anashyft_v5tuples_r1-3_11pb_v1',
    'data_anashyft_v5tuples_r4_11pb_v1',
    'data_anashyft_v5tuples_r5_11pb_v1',
    'data_anashyft_v5tuples_r6_11pb_v1'
]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
