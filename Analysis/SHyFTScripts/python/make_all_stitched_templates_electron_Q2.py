#!/bin/python

import subprocess


options = [
  

    #Q^2
    ['pfRecoShyftAna/eleEB',  'pfRecoShyftAna/eleEB', 'Q2_up_MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  'scaleup'],
    ['pfRecoShyftAna/eleEB',  'pfRecoShyftAna/eleEB', 'Q2_dn_MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  'scaledown'],
    
    ['pfRecoShyftAna/eleEE',  'pfRecoShyftAna/eleEE', 'Q2_up_MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  'scaleup'],
    ['pfRecoShyftAna/eleEE',  'pfRecoShyftAna/eleEE', 'Q2_dn_MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  'scaledown'],

    ]

command = 'python combineBackgroundPlots_met.py --input=387_v1 --mcDir={0:s} --dataDir={1:s}  --outputLabel={2:s} --useData --noQCD --lepMET=MET --dataFile={3:s} --useDataQCD --dataQCDFile={4:s} --templateDir={5:s} --wjetsQ2Var={6:s}'

for option in options :
    if option[6] is None :
        s = command.format(
            option[0], option[1], option[2], option[3], option[4], option[5], ''
            )
    else :
        s = command.format(
            option[0], option[1], option[2], option[3], option[4], option[5], option[6]
            )
    print '--------------------------------------------------------------------------'    
    print '--------------------------------------------------------------------------'
    print s
    print '--------------------------------------------------------------------------'
    print '--------------------------------------------------------------------------'
    subprocess.call( [s, ""], shell=True )    
