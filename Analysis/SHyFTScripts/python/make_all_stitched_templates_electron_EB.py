#!/bin/python

import subprocess


options = [
    ['pfRecoShyftAna/eleEB',                 'pfRecoShyftAna/eleEB', 'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],

    ['pfRecoShyftAnaJES095/eleEB',           'pfRecoShyftAna/eleEB', 'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaJES105/eleEB',           'pfRecoShyftAna/eleEB', 'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    
    ['pfRecoShyftAnaReweightedUnity/eleEB',  'pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaReweightedBTag080/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    
## ##     #for cut and count
    ['pfRecoShyftAnaReweightedBTag090/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    
    ['pfRecoShyftAnaReweightedBTag110/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaReweightedBTag120/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    
    ['pfRecoShyftAnaReweightedLFTag070/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaReweightedLFTag080/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaReweightedLFTag090/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaReweightedLFTag110/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],

##     ['pfRecoShyftAnaReweightedLFTag100/eleEB','pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],#Not present
        
##    # systematics
    ['pfRecoShyftAnaJER000/eleEB',            'pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaJER020/eleEB',            'pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaMETRES090/eleEB',         'pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    ['pfRecoShyftAnaMETRES110/eleEB',         'pfRecoShyftAna/eleEB',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEB_MET.root', 'pfRecoShyftAnaMC/eleEB',  None],
    
    ]

command = 'python combineBackgroundPlots_met.py --input=387_v2 --mcDir={0:s} --dataDir={1:s}  --outputLabel={2:s} --useData --noQCD --lepMET=MET --dataFile={3:s} --useDataQCD --dataQCDFile={4:s} --templateDir={5:s} {6:s}'

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
