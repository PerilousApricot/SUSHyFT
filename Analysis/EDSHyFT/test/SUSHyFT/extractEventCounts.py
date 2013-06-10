#! /usr/bin/env python

from __future__ import print_function

# Import everything from ROOT
# screw you, root for always wanting x11
import sys
oldargs = sys.argv[:]
sys.argv = [oldargs[0], '-b']
from ROOT import *
#gROOT.Macro("~/rootlogon.C")
gROOT.SetBatch(True)
sys.argv = oldargs[:]

import sys
import glob
import math
import json

def deltaR( eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = phi1 - phi2
    if dphi >= math.pi: dphi -= 2*math.pi
    elif dphi < -math.pi: dphi += 2*math.pi
    return math.sqrt(deta*deta + dphi*dphi)

from array import array
from optparse import OptionParser

# Create a command line option parser
parser = OptionParser()
parser.add_option('--output', type='string', action='store',
                  default="",
                  dest='outputFile',
                  help='Output file for exported JSON')

parser.add_option('--files', metavar='F', type='string', action='store',
                  default = "",
                  dest='files',
                  help='Input files')

parser.add_option('--txtfiles', metavar='F', type='string', action='store',
                  default = "",
                  dest='txtfiles',
                  help='Input txt files')

parser.add_option("--onDcache", action='store_true',
                  default=False,
                  dest="onDcache",
                  help="onDcache(1), onDcache(0)")

parser.add_option("--sample", action='store',
                  default="DY",
                  dest="sample",
                  help="Sample Name")

parser.add_option('--JES', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='JES',
                  help='JEC Systematic variation. Options are "nominal, up, down"')

parser.add_option('--jetPtSmear', metavar='F', type='float', action='store',
                  default=0.0,
                  dest='jetPtSmear',
                  help='JER smearing. Standard values are 0.1 (nominal), 0.0 (down), 0.2 (up)')

parser.add_option('--jetEtaSmear', metavar='F', type='float', action='store',
                  default=0.0,
                  dest='jetEtaSmear',
                  help='Jet Phi smearing. Standard values are 0.1 (nominal), 0.0 (down), 0.2 (up)')

parser.add_option("--data", action='store_true',
                  default=False,
                  dest="data",
                  help="data / no pileup")

parser.add_option("--runMuons", action='store_true',
                  default=False,
                  dest="runMuons",
                  help="Electrons(1), Muons(0)")

parser.add_option("--bTag",action='store',
                  default="",
                  dest="bTag",
                  help="b-tag SF")

## parser.add_option("--useC8APrune", action='store_true',
##                   default=True,
##                   dest="useC8APrune",
##                   help="switch on(1) / off(0) C8APrune jets")

parser.add_option("--useBPrimeGenInfo",  action='store_true',
                  default=False,
                  dest="useBPrimeGenInfo",
                  help="switch on(1) / off(0) gen particle info") 

parser.add_option("--events", action='store', default="-1",
                  dest="maxevents",
                  type="int",
                  help="Events to process (-1 means all)" )

# Parse and get arguments
(options, args) = parser.parse_args()

runMu = options.runMuons
#c8aPruneJets = options.useC8APrune
bprimeGenInfo = options.useBPrimeGenInfo
dcache = options.onDcache
maxevents = options.maxevents

print('options', options)
# JEC
jecScale = 0.0
if options.JES == 'up' :
    jecScale = 1.0
elif options.JES == 'down' :
    jecScale = -1.0
flatJecUnc = 0.0

# Import what we need from FWLite
from DataFormats.FWLite import Events, Handle
ROOT.gSystem.Load('libCondFormatsJetMETObjects')

# Get the file list.
if options.files:
    #files = glob.glob( options.files )
    files = [options.files]
    print('getting files', files)
elif options.txtfiles:
    files = []
    with open(options.txtfiles, 'r') as input_:
        for line in input_:
            files.append(line.strip())
else:
    files = []

#print('getting files: ', files)

if dcache:
	files = ["dcap://" + x for x in files]
	print('new files', *files, sep='\n')
	#print('new files', files[0], files[1], ..., sep='\n')
            
#sys.exit(0)

#JEC
jecParStr = std.string('Jec12_V2_Uncertainty_AK5PFchs.txt')
jecUnc = JetCorrectionUncertainty( jecParStr )
  
#------------------------------------------------------------------

# Get the FWLite "Events"
print("Processing files %s" % files)
events = Events (files)

# Get a "handle" (i.e. a smart pointer) to the vector of jets
#jetsH = Handle ("std::vector<pat::Jet>")
#jetsLabel = ("goodPatJetsPFlow", "jets")
#jetsLabel = ("goodPatJetsPFlow", "jets")
#
#tausH = Handle ("std::vector<pat::Tau>")
#tausLabel = ("pfTupleMuSelectedJets")
#
#metH = Handle ("std::vector<pat::MET>")
#metLabel = ("pfTupleMuSelectedJets")
#
#trigH = Handle("pat::TriggerEvent")
#trigLabel = ("patTriggerEvent")
#
#vertH  = Handle ("std::vector<reco::Vertex>")
#vertLabel = ("goodOfflinePrimaryVertices")
#
leptonsH = Handle("std::vector<pat::Muon>")
leptonsLabel = ('pfTupleMuSelectedJets', 'muons')
jetsH = Handle ("std::vector<pat::Jet>")
jetsLabel = ("pfTupleMuSelectedJets", "jets")

metH = Handle ("std::vector<pat::MET>")
metLabel = ('pfTupleMuSelectedJets', "MET")

trigH = Handle("pat::TriggerEvent")
trigLabel = ("patTriggerEvent", "")

vertH  = Handle ("std::vector<reco::Vertex>")
vertLabel = ("goodOfflinePrimaryVertices")

pileupWeightsH = Handle ("std::vector<float>")
pileupWeightsLabel = ("pileupReweightingProducer","pileupWeights")


tausH = Handle ("std::vector<pat::Tau>")
tausLabel = ("pfTupleMuSelectedJets",'taus')
#
# Keep some timing information
nEventsAnalyzed = 0
timer = TStopwatch()
timer.Start()

def incrementTotals( value, njets, nbjets, ntjets ):
    njets  = int(njets)
    nbjets = int(nbjets)
    ntjets = int(ntjets)

    if not njets in value:
        value[njets] = {}

    if not nbjets in value[njets]:
        value[njets][nbjets] = {}

    if not ntjets in value[njets][nbjets]:
        value[njets][nbjets][ntjets] = 0

    value[njets][nbjets][ntjets] += 1

    return value

# loop over events
i = 0
binCount = {}
tauCounter = {}
for event in events:
    if maxevents != -1 and ( maxevents <= i ):
        break
    tausInEvent = 0
    i = i + 1
    if i % 100 == 0 :
        print("EVENT ", i)
    nEventsAnalyzed = nEventsAnalyzed + 1
    #if nEventsAnalyzed == 5000: break
    # Get the objects 
    event.getByLabel(vertLabel,  vertH)
    event.getByLabel(jetsLabel,  jetsH)    
    event.getByLabel(leptonsLabel, leptonsH)
    event.getByLabel(metLabel, metH)
    event.getByLabel(tausLabel, tausH)
    #event.getByLabel(trigLabel, trigH)
    jets    = jetsH.product()
    taus    = tausH.product()
    met     = metH.product()[0]
    leptons = leptonsH.product()
    #print(trigH)
    #print(trigH.product())
    njets   = 0
    nbjet   = 0
    ntjet   = 0
    for jet in jets:
        if jet.pt() < 20:
            continue

        if jet.bDiscriminator('combinedSecondaryVertexBJetTags') >= 0.679:
            nbjet += 1

        njets += 1
    
    for tau in taus:
        if tau.pt() < 20:
            continue

        if tau.tauID("byMediumIsolation"):
            ntjet += 1
            tausInEvent += 1

    binCount = incrementTotals( binCount, njets, nbjet, ntjet )
    if not tausInEvent in tauCounter:
        tauCounter[tausInEvent] = 0
    tauCounter[tausInEvent] += 1

    timer.Stop()

print(binCount)
print(tauCounter)
if options.outputFile:
    open( options.outputFile, 'w' ).write(json.dumps(binCount))

rtime = timer.RealTime(); # Real time (or "wall time")                             
ctime = timer.CpuTime(); # CPU time                                                
print("Analyzed events: {0:6d}".format(nEventsAnalyzed))                           
print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds".format(rtime,ctime))
print("{0:4.2f} events / RealTime second .".format( nEventsAnalyzed/rtime))        
print("{0:4.2f} events / CpuTime second .".format( nEventsAnalyzed/ctime)) 

