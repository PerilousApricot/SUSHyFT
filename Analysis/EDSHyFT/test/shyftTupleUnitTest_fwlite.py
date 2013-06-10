#! /usr/bin/env python
import os
import glob

import ROOT
ROOT.gROOT.Macro("rootlogon.C")


import sys
from DataFormats.FWLite import Events, Handle

files = ["shyft_ultraslim.root"]
print files


events = Events (files)

jetPtHandle     = Handle( "std::vector<float>" )
jetPtLabel  = ( "pfShyftTupleJets", "pt" )



# loop over events
count = 0
print "Start looping"
for event in events:
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)


    event.getByLabel (jetPtLabel, jetPtHandle)
    jetPts = jetPtHandle.product()

    for pt in jetPts :
        print 'Jet pt = ' + str(pt)
