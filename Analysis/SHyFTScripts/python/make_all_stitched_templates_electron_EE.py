#!/bin/python

import subprocess


options = [
    ['pfRecoShyftAna/eleEE',                 'pfRecoShyftAna/eleEE', 'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],

    ['pfRecoShyftAnaJES095/eleEE',           'pfRecoShyftAna/eleEE', 'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaJES105/eleEE',           'pfRecoShyftAna/eleEE', 'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    
    ['pfRecoShyftAnaReweightedUnity/eleEE',  'pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaReweightedBTag080/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    
## ##     #for cut and count
    ['pfRecoShyftAnaReweightedBTag090/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    
    ['pfRecoShyftAnaReweightedBTag110/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaReweightedBTag120/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    
    ['pfRecoShyftAnaReweightedLFTag070/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaReweightedLFTag080/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaReweightedLFTag090/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaReweightedLFTag110/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],

##     ['pfRecoShyftAnaReweightedLFTag100/eleEE','pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],#Not present
        
##    # systematics
    ['pfRecoShyftAnaJER000/eleEE',            'pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaJER020/eleEE',            'pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaMETRES090/eleEE',         'pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaMETRES110/eleEE',         'pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    
    ['pfRecoShyftAnaEleEEPt125/eleEE',         'pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    ['pfRecoShyftAnaEleEEPt075/eleEE',         'pfRecoShyftAna/eleEE',  'MET_v2', 'data_387_all_v2.root', 'qcd_data_eleEE_MET.root', 'pfRecoShyftAnaMC/eleEE',  None],
    
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
