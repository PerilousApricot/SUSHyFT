#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_selectors import event_flow_selectors

tokens = ['Inclusive',
          '>= 1 Lepton',
          '== 1 Lepton',
          'Dilepton Veto',
          'MET Cut Min',
          'MET Cut Max'        
          ]

dirs = [
'TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_v8_003_shyftDump_v9_submit2/'
]

labels = [
    'pfShyftProducerMu',
    'pfShyftProducerEle'
    ]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_selectors( files, tokens, labels )
