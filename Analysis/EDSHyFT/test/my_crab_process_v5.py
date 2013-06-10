#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'TTbarJets-madgraph_shyft_38xOn35x_v5',
'WJets-madgraph_shyft_38xOn35x_v5',
'ZJets-madgraph_shyft_38xOn35x_v5',
'SingleTop_tChannel-madgraph_shyft_38xOn35x_v5',
'SingleTop_tWChannel-madgraph_shyft_38xOn35x_v5',
'InclusiveMu15_shyft_38xOn35x_v5',
'SingleTop_sChannel-madgraph_shyft_38xOn35x_v5',
'VqqJets-madgraph_shyft_38xOn35x_v5'
]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
