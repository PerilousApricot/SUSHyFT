#!/bin/python

import subprocess
import commands
import sys
import tokenize

#crabPath='/uscms_data/d2/skhalil/BPrimeEDM/MC_Ele_May1'
#crabPath='/uscms_data/d2/skhalil/BPrimeEDM/Data'
#crabPath='/uscms_data/d2/skhalil/ShyftTemplates12c'
crabPath='/uscms_data/d2/skhalil/ntuplesShyft/crab_MC'
#crabPath='/uscms_data/d2/skhalil/ntuplesShyft/crab_Data2'
from event_flow_selectors import event_flow_selectors

tokens = [
    #'Inclusive',
    #'Trigger',
    #'PV',
    #'== 1 Tight Lepton',
   # '== 1 Tight Lepton, Mu Veto',
    '== 1 Lepton',
    'Conversion Veto',
    'Dilepton Veto',
    'MET Cut Min',
    #'MET Cut Max',
    #'Z Veto',
    #'>=1 Jets',
    #'>=2 Jets',
    #'>=3 Jets',
    #'>=4 Jets',
    #'>=5 Jets',
    ]

dirs = {
##          "ZZ" : ['ZZ_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9'],
##         "WW" :                     ['WW_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9'],
       "TTbarJets":               ['TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_v9'],
##       "WJetsToLNu":              ['WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_ttbsm_v9'],
##       "DYJetsToLL":              ['DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_ttbsm_v9'],
##       "SingleTopT":              ['T_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_v9'],
##       "SingleTopbarT":           ['Tbar_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_v9'],
##       "SingleTopS":              ['T_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_v9'],
##       "SingleTopbarS":           ['Tbar_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_v9'],
##       "SingleToptW":             ['T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_v9'],
##       "SingleTopbartW":          ['Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_v9'],
    
##     "QCD\_EMEn\_Pt20to30":     ['QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_v9'],
##     "QCD\_EMEn\_Pt30to80":     ['QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia_ttbsm_v9'],
##     "QCD\_EMEn\_Pt80to170":    ['QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_v9'],
##     "QCD\_BCtoE\_Pt20to30":    ['QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_v9'],
##     "QCD\_BCtoE\_Pt30to80":    ['QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_v9'],
##     "QCD\_BCtoE\_Pt80to170":   ['QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia_ttbsm_v9'],
##     "PhotonJets\_Pt40to100":   ['GJets_TuneZ2_40_HT_100_7TeV-madgraph_ttbsm_v9'],
##     "PhotonJets\_Pt100to200":  ['GJets_TuneZ2_100_HT_200_7TeV-madgraph_ttbsm_v9'],
##     "PhotonJets\_Pt200toInf":  ['GJets_TuneZ2_200_HT_inf_7TeV-madgraph_ttbsm_v9'],
    
##    "HLT\_Ele32\_CaloIdVT\_CaloIsoT\_TrkIdT_TrkIsoT":   ['SingleElectron_ttbsm_v9_DataP4',
##                                                         'SingleElectron_ttbsm_v9_DataP5',  
##                                                        ],
    
##    "HLT\_Ele27\_CaloIdVT\_CaloIsoT\_TrkIdT\_TrkIsoT":   ['SingleElectron_ttbsm_v9_DataP1',
##                                                          'SingleElectron_ttbsm_v9_DataP2',
##                                                          'SingleElectron_ttbsm_v9_DataP3',]

#   "HLT\_Ele25\_CaloIdVT\_CaloIsoT\_TrkIdT\_TrkIsoT\_TriCentralJet30":   ['ElectronHad_ttbsm_v9_DataP6',
#                                                                          'ElectronHad_ttbsm_v9_DataP7a',
#                                                                          'ElectronHad_ttbsm_v9_DataP7b',
#                                                                          'ElectronHad_ttbsm_v9_DataP8a',
#                                                                          ]
#    
    #"TTJets": ['TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_424_v8'],
    # "DYJetsToLL": ['DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_ttbsm_424_v8']
    
    # "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1": ['SingleElectron_ttbsm_424_v8_P1'],
    # "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v2": ['SingleElectron_ttbsm_424_v8_P2'],
    # "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v3": ['SingleElectron_ttbsm_424_v8_P3'],
    # "HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v3": ['SingleElectron_ttbsm_424_v8_P4'],
    # "HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v4a": ['SingleElectron_ttbsm_424_v8_P5a'],
    # "HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v4b": ['SingleElectron_ttbsm_424_v8_P5b']


    }

labels = [
   'PF muon',
   'PF electron',
   ]
   
## "TToBLNu, s-channel":      ['TToBLNu_TuneZ2_s-channel_7TeV-madgraph_ttbsm_415_v7'],
##     "TToBLNu, t-channel":      ['TToBLNu_TuneZ2_t-channel_7TeV-madgraph_ttbsm_415_v7'],
##     "TToBLNu, tW-channel":     ['TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_ttbsm_415_v7'],

    
outstrings=[]
for sample in dirs:
    total_sum={}
    outstring = sample
    for idir in dirs[sample] :
        print "-------------------------------" + idir + "---------------------------------"
        files = commands.getoutput("ls -1 " + crabPath + "/" + idir + "/res/*.stdout").split()
        #print 'before call', files, tokens, labels
        dict1 = event_flow_selectors( files, tokens, labels )
        #print dict1
        for f in dict1:
            if f not in total_sum: total_sum[f]={}
            for l in dict1[f]:
                if l not in total_sum[f]: total_sum[f][l]=0
                total_sum[f][l] += dict1[f][l]


    for t in tokens:
        #outstring +='& {0:<12.1f}'.format(total_sum[t][labels[0]])
        outstring += " & %i"%total_sum[t][labels[1]]
    outstring+="\\\\"
    outstrings.append(outstring)


print "-------------------sum table-----------------"
for i in outstrings:
    print i

