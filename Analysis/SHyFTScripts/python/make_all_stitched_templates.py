#!/bin/python

import subprocess


options = [
    ['pfShyftAna',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaJES095', 'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaJES105', 'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],

    ['pfShyftAnaMETRES090', 'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaMETRES110', 'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],


    ['pfShyftAnaJER000', 'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaJER020', 'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],


#    ['pfShyftAna',       'pfShyftAna', '36pb_387v2data_387v9mc_d0vsiso', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_d0vsiso_metcut_normalized_qcd_templates.root', 'pfShyftAnaMC', None],    

    ['pfShyftAnaReweightedBTag080',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedBTag090',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag090',      'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedBTag110',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedBTag120',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],

    ['pfShyftAnaReweightedLFTag080',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag090',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedUnity',          'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag110',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag120',       'pfShyftAna', '36pb_387v2data_387v9mc', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', None],


    ['pfShyftAna',       'pfShyftAna', '36pb_387v2data_387v9mc_pretag', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_metvsiso_pretag_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --makePretagPlots'],
#    ['pfShyftAna',       'pfShyftAna', '36pb_387v2data_387v9mc_wjetsQ2Scaleup', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --wjetsQ2Var=scaleup'],
#    ['pfShyftAna',       'pfShyftAna', '36pb_387v2data_387v9mc_wjetsQ2Scaledown', 'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', 'pf_Mu_shyft_387_v2_shyftana_v9_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --wjetsQ2Var=scaledown'],

    ]

command = 'python combineBackgroundPlots.py --input=shyftana_387_v9 --mcDir={0:s} --dataDir={1:s} --outputLabel={2:s}  --useData --dataFile={3:s} --useDataQCD --dataQCDFile={4:s} --templateDir={5:s} {6:s}'

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
