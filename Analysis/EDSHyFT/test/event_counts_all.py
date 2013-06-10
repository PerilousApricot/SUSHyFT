#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_crab import event_flow_crab

tokens = ['step1',
#          'isolatedPatMuons',
#          'isolatedPatMuonsPFlow'
          'scrapingVeto',
          'primaryVertexFilter',
          'HBHENoiseFilter',
#          'shyftMuCalo',          
#          'shyftMuPF',
#          'shyftMuJPT'
          ]

dirs = [
#'DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_shyft_387_v1',
#'Mu_Run2010A-Nov4ReReco_shyft_387_v1',
#'Mu_Run2010B-Nov4ReReco_shyft_387_v1',
#'TTJets_TuneD6T_7TeV-madgraph-tauola_PUBX156_shyft_387_v1',
#'TTJets_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1',
#'TTJets_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1_btagsys',
#'TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola_shyft_387_v1',
#'TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola_shyft_387_v1',
#'TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola_shyft_387_v1',
#'TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1_take2',
#'TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1',
#'TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola_shyft_387_v1',
#'TTJets_TuneZ2_7TeV-madgraph-tauola_shyft_387_v1',
#'TToBLNu_TuneZ2_s-channel_7TeV-madgraph_shyft_387_v1',
#'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_shyft_387_v1',
#'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_shyft_387_v1',
#'VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1',
'VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1',
'VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1',
#'WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1',
'WJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1',
'WJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1'
]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_crab( files, tokens )
