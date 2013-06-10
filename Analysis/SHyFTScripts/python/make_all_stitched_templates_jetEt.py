#!/bin/python

import subprocess


options = [
           ['pfShyftAna',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaJES095', 'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaJES105', 'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           
           ['pfShyftAnaMETRES090', 'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaMETRES110', 'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           
           
           ['pfShyftAnaJER000', 'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaJER020', 'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           
           
           #    ['pfShyftAna',       'pfShyftAna', '1087pb_424_v8_jetEt_d0vsiso', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_d0vsiso_metcut_normalized_qcd_templates.root', 'pfShyftAnaMC', None],    
           
           ['pfShyftAnaReweightedBTag080',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaReweightedBTag090',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           #    ['pfShyftAnaReweightedLFTag090',      'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaReweightedBTag110',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaReweightedBTag120',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           
           ['pfShyftAnaReweightedLFTag080',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaReweightedLFTag090',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           #    ['pfShyftAnaReweightedUnity',          'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaReweightedLFTag110',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaReweightedLFTag120',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaPUup',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaPUdown',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           ['pfShyftAnaNoPUReweight',       'pfShyftAna', '1087pb_424_v8_jetEt', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
           
           
           ['pfShyftAna',       'pfShyftAna', '1087pb_424_v8_jetEt_pretag', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_pretag_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --makePretagPlots'],
           #    ['pfShyftAna',       'pfShyftAna', '1087pb_424_v8_jetEt_wjetsQ2Scaleup', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --wjetsQ2Var=scaleup'],
           #    ['pfShyftAna',       'pfShyftAna', '1087pb_424_v8_jetEt_wjetsQ2Scaledown', 'SingleMu_Run2011A_ttbsm_v8_HLT_Mu30.root', 'pf_SingleMu_ttbsm_424_v8_jetEt_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --wjetsQ2Var=scaledown'],
           
           ]

#command = 'python combineBackgroundPlots.py --input=shyftana_414_mupt30_split_v2 --mcDir={0:s} --dataDir={1:s} --outputLabel={2:s}  --useData --dataFile={3:s} --useDataQCD --dataQCDFile={4:s} --templateDir={5:s} {6:s} --lumi=151.2'
command = 'python ../../SHyFTScripts/python/combineBackgroundPlots_jetEt.py --input=ttbsm_424_v8 --mcDir={0:s} --dataDir={1:s} --outputLabel={2:s}  --useData --dataFile={3:s} --useDataQCD --dataQCDFile={4:s} --templateDir={5:s} {6:s} '

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
