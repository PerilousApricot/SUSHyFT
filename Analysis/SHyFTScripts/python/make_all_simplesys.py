#!/bin/python

import subprocess


options = [
    ['35pb_387v1data_387v1mc_TuneD6T_central', 'TuneD6T', 'central'],
#    ['35pb_387v1data_387v1mc_TuneD6T_pu', 'TuneD6T', 'pu'],
    ['35pb_387v1data_387v1mc_TuneD6T_matchingup', 'TuneD6T', 'matchingup'],
    ['35pb_387v1data_387v1mc_TuneD6T_matchingdown', 'TuneD6T', 'matchingdown'],        
    ['35pb_387v1data_387v1mc_TuneD6T_scaleup', 'TuneD6T', 'scaleup'],
    ['35pb_387v1data_387v1mc_TuneD6T_scaledown', 'TuneD6T', 'scaledown'],
    ['35pb_387v1data_387v1mc_TuneD6T_largerISRFSR', 'TuneD6T', 'largerISRFSR'],
    ['35pb_387v1data_387v1mc_TuneD6T_smallerISRFSR', 'TuneD6T', 'smallerISRFSR'],      
    ['35pb_387v1data_387v1mc_TuneZ2_central', 'TuneZ2', 'central'],

    ]

command = 'python makeSimpleSysTemplates.py --input=shyftana_387_v1 --outputLabel={0:s}  --tune={1:s} --variation={2:s}'

for option in options :
    s = command.format(
        option[0], option[1], option[2]
        )
    print '--------------------------------------------------------------------------'    
    print '--------------------------------------------------------------------------'
    print s
    print '--------------------------------------------------------------------------'
    print '--------------------------------------------------------------------------'
    subprocess.call( [s, ""], shell=True )    
