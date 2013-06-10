#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'data_anashyft_v6tuples_r1-3_15pb_v1',
'data_anashyft_v7tuples_r4_15pb_v1',
'data_anashyft_v7tuples_r5_15pb_v1',
#'InclusiveMu15_shyftana_38xOn35x_v20_allsys',
#'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v20_allsys',
#'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v20_allsys',
#'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v20_allsys',
#'TTbarJets-madgraph_shyftana_38xOn35x_v20_allsys',
#'WJets-madgraph_shyftana_38xOn35x_v20_allsys',
#'ZJets-madgraph_shyftana_38xOn35x_v20_allsys',
#'VqqJets-madgraph_shyftana_38xOn35x_v20_allsys',


]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
