# !/bin/python

import subprocess


crabFiles = [
    ['crab_InclusiveMu15_shyftana_38xOn35x_v21_allsys_anashyft.cfg',                  'InclusiveMu15_shyftana_38xOn35x_v21_allsys'],
    ['crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v21_allsys_anashyft.cfg',    'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v21_allsys_anashyft.cfg',    'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v21_allsys_anashyft.cfg',   'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_TTbarJets-madgraph_shyftana_38xOn35x_v21_allsys_anashyft.cfg',             'TTbarJets-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_WJets-madgraph_shyftana_38xOn35x_v21_allsys_anashyft.cfg',                 'WJets-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_ZJets-madgraph_shyftana_38xOn35x_v21_allsys_anashyft.cfg',                 'ZJets-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_VqqJets-madgraph_shyftana_38xOn35x_v21_allsys_anashyft.cfg',               'VqqJets-madgraph_shyftana_38xOn35x_v21_allsys']
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
