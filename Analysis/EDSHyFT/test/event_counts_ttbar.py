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
'TTJets_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1',
'TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola_shyft_387_v1',
'TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola_shyft_387_v1',
'TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola_shyft_387_v1',
'TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1',
'TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1',
'TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola_shyft_387_v1',
'TTJets_TuneZ2_7TeV-madgraph-tauola_shyft_387_v1',

]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_crab( files, tokens )
