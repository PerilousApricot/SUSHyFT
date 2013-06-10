#!/bin/python

import subprocess
import os

from sys import argv
if len(argv)<2:
    print "usage: python my_crab_status_ele.py COMMAND"
    print "where COMMAND can be status, getoutput, etc"
    exit()

argument=""
for i in argv[1:]:
    argument += i+" "

crabPath='/uscms_data/d2/skhalil/'


crabFiles = [
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2', 
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
           'BPrimeEDM_8TeV/Nov16/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2', #submitted
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
           
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
           
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph_tlbsm_53x_v2',           
##            'BPrimeEDM_8TeV/Nov16/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_tlbsm_53x_v2',
    
##            'BPrimeEDM_8TeV/Nov16/T_t-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/T_s-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v2',
##            'BPrimeEDM_8TeV/Nov16/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v2',
    
    
        ##    'BPrimeEDM_8TeV/Nov16/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v2', #submitted

##            'BPrimeEDM_8TeV/Nov16/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_tlbsm_53x_v2_p1',   #done 
        ##   'BPrimeEDM_8TeV/Nov16/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_tlbsm_53x_v2', # new submitted 
##           'BPrimeEDM_8TeV/Nov16/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_tlbsm_53x_v2', #99% done
    
##          'BPrimeEDM_8TeV/Nov16/WW_TuneZ2star_8TeV_pythia6_tauola_tlbsm_53x_v2', #done
##          'BPrimeEDM_8TeV/Nov16/ZZ_TuneZ2star_8TeV_pythia6_tauola_tlbsm_53x_v2', #done   
##          'BPrimeEDM_8TeV/Nov16/TTZJets_8TeV-madgraph_v2_tlbsm_53x_v2', # For Dinko
#    
##           'BPrimeEDM_8TeV/Nov16/TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola_tlbsm_53x_v2', #95% done
##           'BPrimeEDM_8TeV/Nov16/TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola_tlbsm_53x_v2',# new submission
##            'BPrimeEDM_8TeV/Nov16/TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola_tlbsm_53x_v2', # 99% done
##          'BPrimeEDM_8TeV/Nov16/TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola_tlbsm_53x_v2', #almost done


#            'BPrimeEDM_8TeV/Nov16/SingleElectron_DataA_tlbsm_53x_v2', #done
#            'BPrimeEDM_8TeV/Nov16/SingleElectron_DataB_tlbsm_53x_v2', #done
##            'BPrimeEDM_8TeV/Nov16/SingleElectron_Data-Run2012C-PromptReco-v1_tlbsm_53x_v2',
#            'BPrimeEDM_8TeV/Nov16/SingleElectron_Data-Run2012C-24Aug2012-v1_tlbsm_53x_v2',
]

for crabFile in crabFiles :
    s = 'crab -' + argument +' -c ' + crabPath + "/" + crabFile
    print s
    subprocess.call( [s], shell=True )

