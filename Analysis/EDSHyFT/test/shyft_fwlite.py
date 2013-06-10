#! /usr/bin/env python
import os
import glob
import math
import copy

from ROOT import TMath
from optparse import OptionParser

parser = OptionParser()


############################################
#            Job steering                  #
############################################

# Input files to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')

# Output name to use. 
parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='shyft_fwlite',
                  dest='outname',
                  help='output name')

# Sample name
parser.add_option('--sampleName', metavar='F', type='string', action='store',
                  default='Top',
                  dest='sampleName',
                  help='output name')

# This will use the loose selections, and negate the isolation
# criteria
parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='use loose leptons (exclusive from tight)')

# no MET cut
parser.add_option('--noMET', metavar='F', action='store_true',
                  default=False,
                  dest='noMET',
                  help='no MET cut')

# invert MET cut
parser.add_option('--invMET', metavar='F', action='store_true',
                  default=False,
                  dest='invMET',
                  help='invert MET cut')

# Using data or not. For MC, truth information is accessed.
parser.add_option('--useData', metavar='F', action='store_true',
                  default=True,
                  dest='useData',
                  help='use data')

# MET Unclustered energy systematics
parser.add_option('--metSys', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='metSys',
                  help='MET Systematic variation. Options are "nominal, up, down"')

# JEC systematics
parser.add_option('--jecSys', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='jecSys',
                  help='JEC Systematic variation. Options are "nominal, up, down"')

# JER systematics
parser.add_option('--jetSmear', metavar='F', type='float', action='store',
                  default=0.1,
                  dest='jetSmear',
                  help='JER smearing. Standard values are 0.1 (nominal), 0.0 (down), 0.2 (up)')

# Pileup systematics
parser.add_option('--pileupReweight', metavar='F', type='string', action='store',
                  default='unity',
                  dest='pileupReweight',
                  help='Pileup reweighting. Options are "nominal, up, down, unity"')

# BTag systematics
parser.add_option('--btagSys', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='btagSys',
                  help='BTag Systematic variation. Options are "nominal, up, down, up2, down2"')

# LFTag systematics
parser.add_option('--lftagSys', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='lftagSys',
                  help='LFTag Systematic variation. Options are "nominal, up, down, up2, down2"')

#Min Jets
parser.add_option('--minJets', metavar='F', type='int', action='store',
                  default=1,
                  dest='minJets',
                  help='Min number of jets')
#Jet Pt Cut
parser.add_option('--jetPt', metavar='F', type='float', action='store',
                  default=35.0,
                  dest='jetPt',
                  help='Jet Pt cut')

# electrons or muons
parser.add_option('--lepType', metavar='F', type='int', action='store',
                  default=1,
                  dest='lepType',
                  help='Lepton type. Options are 0 = muons, 1 = electrons')

# PU weigths 1D or 3D
parser.add_option('--PUWeights', metavar='P', type='string', action='store',
                  default='3DSinEle',
                  dest='PUWeights',
                  help='PU weights type. Options are "1D, 3DSinEle, 3DEleHad" ')

# barrel only
parser.add_option('--barrel', metavar='F', action='store_true',
                  default=False,
                  dest='barrel',
                  help='barrel region only')

# adding dirs
parser.add_option('--addDirs', metavar='F', action='store_true',
                  default=False,
                  dest='addDirs',
                  help='add splitting to barrel/endcap')

# EleHad data
parser.add_option('--useEleHad', metavar='F', action='store_true',
                  default=False,
                  dest='useEleHad',
                  help='eleHad Data, apply the jet pt reweighting to 3rd leading jet')

(options, args) = parser.parse_args()

if not options.files:
    if not options.useData:
        options.files='/store/user/meloam/ZJetToMuMu_Pt-80to120_TuneZ2star_8TeV_pythia6/melo_v3__ZJetToMuMu_Pt-80to120_TuneZ2star_8TeV_pythia6_None-20130206162922_USER/77d719c5702be485d26a9b383688b09c/shyftDump2_3_2_xkA.root'
    else:
        options.files='/store/user/meloam/SingleMu/melo_v3__SingleMu_meloam_feb12_tlbsm53x2_Run2012C_24Aug2012_v1-20130212222033_USER/562ac012a02badb8cb519b40e75790e9/shyftDump2_16_1_J85.root'

minJets = options.minJets
argv = []

# Import everything from ROOT
import ROOT
ROOT.gROOT.Macro("~/rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

from Analysis.SHyFTScripts.combinations import *

ROOT.gSystem.Load('libCondFormatsJetMETObjects')

#from CondFormats.JetMETObjects import *


print 'Getting files from this dir: ' + options.files

# Get the file list. 
files = glob.glob( options.files )
print files


# Create the output file. 
f = ROOT.TFile(options.outname + ".root", "recreate")
f.cd()
if options.addDirs:
    dirnames = ['', 'EB', 'EE']
else:
    dirnames = ['']

directories = []
# fill array of TDirectories and create them if necessary
for d in dirnames:
    directories.append(f.GetDirectory(''))
    if d!='':
        directories.pop()
        directories.append(f.mkdir(d,d))

# TODO make configuratble
maxJets = 9
maxBTags = 5
maxTTags = 5


# Make histograms
print "Creating histograms"
nEvents=[]
nMuons=[]
nElectrons=[]
nMETs=[]
nJets=[]
nJets3=[]
nBTags=[]
nTTags=[]
nVertices=[]
npuTruth=[]
npuReweight=[]
bmass=[]
cmass=[]
lfmass=[]
elePt=[]
eleEta=[]
elePhi=[]
elePFIso=[]
lepJetdR=[]
ptJet0=[]
ptJet1=[]
ptJet2=[]
ptJet3=[]
ptJet4=[]
m3=[]
nVertices3j1t=[]
npuTruth3j1t=[]
npuReweight3j1t=[]
elePt3j1t=[]
eleEta3j1t=[]
elePhi3j1t=[]
elePFIso3j1t=[]
ptJet0_3j1t=[]
ptJet1_3j1t=[]
ptJet2_3j1t=[]
ptJet3_3j1t=[]
ptJet4_3j1t=[]
wMT3j1t=[]
hT3j1t=[]
m3j1t=[]
met3j1t=[]

# creating simple histograms with no jet,tag binning
simplePlots = [
    [nEvents, "nEvents",         "Number of Events;N_{events};Number",                          5, -0.5,  4.5],
    [nMuons, "nMuons",           "Number of Muons, p_{T} > 35 GeV;N_{Muons};Number",            5, -0.5,  4.5 ],
    [nElectrons ,"nElectrons",   "Number of Electrons, p_{T} > 35 GeV;N_{Electrons};Number",    5, -0.5,  4.5 ],
    [nMETs      ,"nMET",         "MET > 20 GeV;MET;Events/5 GeV",                               120, 0,    300 ],
    [nJets      ,"nJets",        "Number of Jets, p_{T} > 35 GeV;N_{Jets};Number",              20, -0.5, 19.5 ],
    [nJets3     ,"nJets3",       "Number of #geq 3 Jets, p_{T} > 35 GeV;N_{Jets};Number",       20, -0.5, 19.5 ],
    [nBTags      ,"nBTags",        "Number of BTags",                                           maxBTags, 0, maxBTags],
    [nTTags     ,"nTTags",       "Number of TauTags",                                           maxTTags, 0, maxTTags],
    [nVertices  ,"nVertices",    "Number of Primary Vertices",                                  25, -0.5, 24.5],
    [npuTruth   ,"npuTruth",     "Number of Primary Interactions MCTrue",                       25, -0.5, 24.5],
    [npuReweight,"npuReweight",  "Number of Primary Interactions reweighted",                   25, -0.5, 24.5],
    [elePt  ,"elePt", "lepton p_{T} (GeV),", 100, 0., 200.],
    [eleEta ,"eleEta",  "lepton #eta ", 60,-2.5,2.5],
    
    [elePhi ,"elePhi", "lepton #phi", 50, -3.2, 3.2],
    [elePFIso ,"elePFIso", "lepton relative PF isolation", 50, 0.0, 0.2],
    [lepJetdR ,"lepJetdR", "dR b/w jet and lepton",    32,    0,  3.2],
    [ptJet0 ,"ptJet0", "p_{T} Of Leading Jet", 40, 0., 800.],
    [ptJet1 ,"ptJet1", "p_{T} Of 2nd Leading Jet", 40, 0., 400.],
    [ptJet2 ,"ptJet2", "p_{T} Of 3rd Leading Jet", 30, 0., 300.],
    [ptJet3 ,"ptJet3", "p_{T} Of 4th Leading Jet", 40, 0., 200.],
    [ptJet4 ,"ptJet4", "p_{T} Of #geq 5th Leading Jet", 40, 0., 200.],
    [m3     ,"m3", "m3",  60, 0., 600.],
    
    #Special
    [nVertices3j1t ,"nVertices3j1t",    "Number of Primary Vertices, #geq 3jets, #geq 1tag", 25, -0.5, 24.5],
    [npuTruth3j1t ,"npuTruth3j1t",    "Number of Primary Interactions, #geq 3jets, #geq 1tag", 25, -0.5, 24.5],
    [npuReweight3j1t ,"npuReweight3j1t", "Number of Primary Interactions reweighted, #geq 1jets, #geq 1tag", 25, -0.5, 24.5],
    [elePt3j1t ,"elePt3j1t", "lepton P_{T} (GeV), #geq 3jets, #geq 1tag", 100,0.,200.],
    [eleEta3j1t ,"eleEta3j1t", "lepton #eta (GeV), #geq 3jets, #geq 1tag", 60,-3.0,3.0],
    [elePhi3j1t ,"elePhi3j1t", "lepton #phi,  #geq 3jets, #geq 1tag", 50, -3.2, 3.2],
    [elePFIso3j1t ,"elePFIso3j1t", "lepton PF relIso,  #geq 3jets, #geq 1tag", 50, 0.0, 0.2],
    [ptJet0_3j1t ,"ptJet0_3j1t", "p_{T} Of Leading Jet, #geq 3jets, #geq 1tag", 40, 0., 800.],
    [ptJet1_3j1t ,"ptJet1_3j1t", "p_{T} Of 2nd Leading Jet, #geq 3jets, #geq 1tag", 40, 0., 400.],
    [ptJet2_3j1t ,"ptJet2_3j1t", "p_{T} Of 3rd Leading Jet, #geq 3jets, #geq 1tag", 30, 0., 300.],
    [ptJet3_3j1t ,"ptJet3_3j1t", "p_{T} Of 4th Leading Jet, #geq 3jets, #geq 1tag", 40, 0., 200.],
    [ptJet4_3j1t ,"ptJet4_3j1t", "p_{T} Of #geq 5th Leading Jet, #geq 3jets, #geq 1tag", 40, 0., 200.],
    [wMT3j1t,"wMT3j1t", "wMT, #geq 3jets, #geq 1tag",  120, 0., 300.],
    [hT3j1t ,"hT3j1t", "hT, #geq 3jets, #geq 1tag", 120, 0., 1200.],
    [m3j1t  ,"m3j1t", "m3, #geq 3jets, #geq 1tag",  60, 0., 600.],
    [met3j1t ,"met3j1t", "MET (GeV), #geq 1tag", 120,0.,300.0],
    ]

if not options.useData:
    simplePlots.append([bmass ,"bmass", "B Sec Vtx Mass", 40, 0, 10])
    simplePlots.append([cmass ,"cmass", "C Sec Vtx Mass", 40, 0, 10])
    simplePlots.append([lfmass ,"lfmass", "LF Sec Vtx Mass", 40, 0, 10])

for h in simplePlots:
    for idir in xrange(0,len(dirnames)):
        directories[idir].cd()
        h[0].append(ROOT.TH1F(h[1],h[2],h[3],h[4],h[5]))
        h[0][-1].SetDirectory(directories[idir])


nPVPlots = []
secvtxMassPlots = []
lepEtaPlots = []
lepPtPlots = []
centralityPlots = []
sumEtPlots = []
#jet1PtPlots = []
METPlots = []
wMTPlots = []
hTPlots = []

# Plots split 3 ways (jet, btag, tautag) for SUSY
nPVPlotsTau = []
secvtxMassPlotsTau = []
lepEtaPlotsTau = []
lepPtPlotsTau = []
centralityPlotsTau = []
sumEtPlotsTau = []
#jet1PtPlots = []
METPlotsTau = []
wMTPlotsTau = []
hTPlotsTau = []

# TODO - add tau-specific plots to this script
tauPtPlots = []
tauEtaPlots = []
tauPhiPlots = []
tauMassPlots = []
flavors = ['_b','_c','_q','']

allVarPlots = [
    nPVPlots,
    secvtxMassPlots,
    lepEtaPlots,
    lepPtPlots,
    centralityPlots,
    sumEtPlots,
    #jet1PtPlots,
    METPlots,
    wMTPlots,
    hTPlots,
    ]

allVarPlotsWithTaus = [
    nPVPlotsTau,
    secvtxMassPlotsTau,
    lepEtaPlotsTau,
    lepPtPlotsTau,
    centralityPlotsTau,
    sumEtPlotsTau,
    #jet1PtPlots,
    METPlotsTau,
    wMTPlotsTau,
    hTPlotsTau,
    ]


names = ['nPV', 'secvtxMass','lepEta','lepPt', 'centrality','sumEt', 'MET', 'wMT', 'hT']
titles = ['number of Primary Vertices','SecVtx Mass','Lepton #eta', 'Lepton pt', 'Centrality','#sum E_{T}','MET', 'M_{WT}', 'hT']
bounds = [ [25, -0.5, 24.5],
           [40,0.,10.],
           [30,0.,3.0],
           [100,0.,200],
           [120,0.,1.2],
           [100,0.,1000.],
           [120,0.,300.],
           [120,0.,300.],
           [120,0.,1200.]
           ]

mbb = []
dRbb = []

for ijet in range(0,maxJets+1):
    mbb.append([])
    dRbb.append([])
    if ijet < 2:
        continue
    for idir in range(0, len(dirnames)):
        directories[idir].cd()
        mbb[ijet].append( ROOT.TH1F("mbb_" + str(ijet) + 'j', "Mass of bb Pair", 150, 0., 1500.) )
        mbb[ijet][-1].SetDirectory(directories[idir])
        dRbb[ijet].append( ROOT.TH1F("dRbb_" + str(ijet) + 'j', "#Delta R_{bb}", 150, -ROOT.TMath.Pi(), ROOT.TMath.Pi() ) )
        dRbb[ijet][-1].SetDirectory(directories[idir])
        
for iplot in range(0,len(allVarPlots)):
    varPlots = allVarPlots[iplot]
    varPlotsTau = allVarPlotsWithTaus[iplot]
    for ijet in range(0,maxJets+1):
        varPlots.append( [] )
        varPlotsTau.append( [] )
        for itag in range(0,maxBTags+1):
            if itag > ijet:
                continue
            varPlots[ijet].append( [] )
            varPlotsTau[ijet].append( [] )
            if names[iplot]=='secvtxMass' and itag==0:
                continue
            if ( names[iplot]=='jetPt1' or names[iplot]=='sumPt' or names[iplot]=='centrality' ) and ijet==0:
                continue
            for itau in range(0,maxTTags+1):
                if itau > ijet:
                    continue
                varPlotsTau[ijet][itag].append([])
                for iflav in range(0,len(flavors)):
                    flav = flavors[iflav]
                    if itau == 0:
                        varPlots[ijet][itag].append([])
                    varPlotsTau[ijet][itag][itau].append([])
                    for idir in range(0, len(dirnames)):
                        directories[idir].cd()
                        if itau == 0:
                            varPlots[ijet][itag][iflav].append( ROOT.TH1F(options.sampleName + "_" + names[iplot] + "_" + str(ijet) + 'j_' + str(itag) + 't' + flav,
                                                                titles[iplot] + ", njets = " + str(ijet) + ', ntags = ' + str(itag),
                                                                bounds[iplot][0], bounds[iplot][1], bounds[iplot][2])
                                                     )
                        titlePostfix = ", njets=%s, nbtag=%s, nttag=%s" % \
                                (ijet, itag, itau)
                        varPlotsTau[ijet][itag][itau][iflav].append(
                                    ROOT.TH1F( options.sampleName + "_" + \
                                                names[iplot] + "_Tau_" + \
                                                "%sj_%sb_%st" % (ijet, itag, itau) + \
                                                flav,
                                               titles[iplot] + titlePostfix,
                                               bounds[iplot][0],
                                               bounds[iplot][1],
                                               bounds[iplot][2]) )
                        varPlots[ijet][itag][iflav][-1].SetDirectory(directories[idir])

############################################
#     Jet energy scale uncertainties       #
############################################

jecParStr = ROOT.std.string('Jec12_V3_Uncertainty_AK5PFchs.txt')
jecUnc = ROOT.JetCorrectionUncertainty( jecParStr )



############################################
# Physics level parameters for systematics #
############################################

# Kinematic cuts:
looseMuonIsoMax = 0.2
looseElectronIsoMax = 0.2
ssvheCut = 0.679
tauIdCut = 0.5
if options.noMET:
        metMin = 0.0
else:
    metMin = 20.0
    
if options.lepType == 0:
    muonPtMin = 35.0
    electronPtMin = 20.0
    jetPtMin = options.jetPt
    lepStr = 'Mu'
else:
    muonPtMin = 35.0
    electronPtMin = 35.0
    jetPtMin = options.jetPt
    lepStr = 'Ele'
    
# Per-jet scale factors:
sfB = 1.00
sfC = 1.00
sfQ = 1.00
if options.btagSys == 'up':
    sfB = 1.10
    sfC = 1.10
elif options.btagSys == 'down':
    sfB = 0.90
    sfC = 0.90
elif options.btagSys == 'up2':
    sfB = 1.20
    sfC = 1.20
elif options.btagSys == 'down2':
    sfB = 0.80
    sfC = 0.80
    
if options.lftagSys == 'up':
    sfQ = 1.10
elif options.lftagSys == 'down':
    sfQ = 0.90
elif options.lftagSys == 'up2':
    sfQ = 1.20
elif options.lftagSys == 'down2':
    sfQ = 0.80

#MET Scales
metScale = 0.0
if options.metSys == 'up':
    metScale = 1.0
if options.metSys == 'down':
    metScale = -1.0
    
# JEC scales
jecScale = 0.0
if options.jecSys == 'up':
    jecScale = 1.0
elif options.jecSys == 'down':
    jecScale = -1.0
flatJecUnc = 0.0
#flatJecUnc = 0.05

cutFlow = [
    [0,'Inclusive'],
    [0,'==1 Lepton'],
    [0,'==1 Lepton, 0 other lepton'],
    [0,'MET Cut min'],
    [0,'>= 1 Jets'],
    [0,'>= 3 Jets']
    ]


events = Events (files)

# Make the entirety of the handles required for the
# analysis. 
postfix = ""
Epostfix = ""
Mpostfix = ""
if options.useLoose:
    postfix = "Loose"
    if options.lepType == 0:
        Mpostfix = "Loose"
    else:
        Epostfix = "Loose"

jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "pt" )
genJetPtHandle          = Handle( "std::vector<float>" )
genJetPtLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "genJetPt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "mass" )
jetSecvtxMassHandle         = Handle( "std::vector<float>" )
jetSecvtxMassLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "secvtxMass" )
jetSSVHEHandle         = Handle( "std::vector<float>" )
jetSSVHELabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "ssvhe" )
jetFlavorHandle         = Handle( "std::vector<float>" )
jetFlavorLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "flavor" )
jetTauPtHandle         = Handle( "std::vector<float>" )
jetTauPtLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "tauJetPt" )
jetTauEtaHandle         = Handle( "std::vector<float>" )
jetTauEtaLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "tauJetEta" )
jetTauPhiHandle         = Handle( "std::vector<float>" )
jetTauPhiLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "tauJetPhi" )
jetTauMassHandle         = Handle( "std::vector<float>" )
jetTauMassLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "tauJetMass" )
tauTagHandle      =Handle( "std::vector<float>" )
tauDB3HitLooseHandle         = Handle( "std::vector<float>" )
tauDB3HitLooseLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byLooseCombinedIsolationDeltaBetaCorr3Hits" )
tauDB3HitMediumHandle         = Handle( "std::vector<float>" )
tauDB3HitMediumLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byLooseCombinedIsolationDeltaBetaCorr3Hits" )
tauDB3HitTightHandle         = Handle( "std::vector<float>" )
tauDB3HitTightLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byLooseCombinedIsolationDeltaBetaCorr3Hits" )
tauMVALooseHandle         = Handle( "std::vector<float>" )
tauMVALooseLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byLooseIsolationMVA2" )
tauMVAMediumHandle         = Handle( "std::vector<float>" )
tauMVAMediumLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byMediumIsolationMVA2" )
tauMVATightHandle         = Handle( "std::vector<float>" )
tauMVATightLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byTightIsolationMVA2" )






#postfix=""
muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons"+  Mpostfix,   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons"+  Mpostfix,   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons"+  Mpostfix,   "phi" )
muonPfisoHandle         = Handle( "std::vector<float>" )
muonPfisoLabel    = ( "pfShyftTupleMuons"+  Mpostfix,   "pfiso" )

#postfix="Loose"
electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons"+  Epostfix,   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons"+  Epostfix,   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons"+  Epostfix,   "phi" )
electronPfisoHandle         = Handle( "std::vector<float>" )
electronPfisoLabel    = ( "pfShyftTupleElectrons"+  Epostfix,   "pfiso" )

if options.metSys == 'up':
    metHandle = Handle( "std::vector<float>" )
    metLabel = ("pfShyftTupleMETMetRes110",   "pt" )
    metPhiHandle = Handle( "std::vector<float>" )
    metPhiLabel = ("pfShyftTupleMETMetRes110",   "phi" )
elif options.metSys == 'down':
    metHandle = Handle( "std::vector<float>" )
    metLabel = ("pfShyftTupleMETMetRes090",   "pt" )
    metPhiHandle = Handle( "std::vector<float>" )
    metPhiLabel = ("pfShyftTupleMETMetRes090",   "phi" )    
else:
    metHandle = Handle( "std::vector<float>" )
    metLabel = ("pfShyftTupleMET" + lepStr +  postfix,   "pt" )
    metPhiHandle = Handle( "std::vector<float>" )
    metPhiLabel = ("pfShyftTupleMET" + lepStr +  postfix,   "phi" )

pileupHandle = Handle( "std::vector<float>" )
if options.PUWeights == '1D':
    pileupLabel = ("PUNtupleDumperOld",   "PUweightNominalUpDown" )
    print 'running old PU weights'
elif options.PUWeights == '3DSinEle':    
    pileupLabel = ("PUNtupleDumperSingleEle",   "pileupWeights" )
    print 'running 3D PU weights for SingleEle data'
elif options.PUWeights == '3DEleHad':    
    pileupLabel = ("PUNtupleDumperEleHad",   "pileupWeights" )
    print 'running 3D PU weights for EleHad data'

vertH  = Handle ("std::vector<reco::Vertex>")
vertLabel = ("goodOfflinePrimaryVertices")

puInfoHandle = Handle("std::vector<PileupSummaryInfo>")
puInfoLabel = ("addPileupInfo")

PUweight = 1.0

# loop over events
count = 0
print "Getting event count"
ntotal = events.size()
print " ... got %s events total" % ntotal
percentDone = 0.0
ipercentDone = 0
ipercentDoneLast = -1
print "Start looping"
for event in events:
    cutFlow[0][0] += 1 # number of inclusive events
    ipercentDone = int(percentDone)
    if ipercentDone != ipercentDoneLast:
        ipercentDoneLast = ipercentDone
        print 'Processing {0:10.0f}/{1:10.0f}: {2:5.0f}%'.format(
            count, ntotal, ipercentDone )
    count = count + 1
    percentDone = float(count) / float(ntotal) * 100.0
    nEvents[0].Fill(count, PUweight)
    
    #if count > 1000: break
    #Require exactly one lepton (e or mu)
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
        muonPts = None
    else:
        muonPts = muonPtHandle.product()
    
    event.getByLabel (electronPtLabel, electronPtHandle)
    if not electronPtHandle.isValid():
        electronPts = None
    else:
        electronPts = electronPtHandle.product()

    # Get the isolation values if needed
    #if options.useLoose:
    if muonPts is not None:
        event.getByLabel (muonPfisoLabel, muonPfisoHandle)
        if not muonPfisoHandle.isValid():
            continue
        muonPfisos = muonPfisoHandle.product()
    if electronPts is not None:
        event.getByLabel (electronPfisoLabel, electronPfisoHandle)
        if not electronPfisoHandle.isValid():
            print 'here'
            continue
        electronPfisos = electronPfisoHandle.product()

    # get the PU weight before filling any histogram
    if not options.useData and options.pileupReweight!='unity':
        event.getByLabel( pileupLabel, pileupHandle )
        if not pileupHandle.isValid():
            print 'You want pileup reweighting for MC but there is no weights stored. '\
                  'Use "--pileupReweight unity" to skip this.'
        PUw = pileupHandle.product()
        if len(PUw)!=3:
            print 'I expect 3 numbers in the PUweightNominalUpDown vector!'
        else:
            if options.pileupReweight=='nominal':PUweight=PUw[0]
            elif options.pileupReweight=='up': PUweight=PUw[1]
            elif options.pileupReweight=='down': PUweight=PUw[2]
            else:
                print 'unknown option in --pileupReweight, use unity'
                PUweight=1.0
    
    # number of primary vertices
    event.getByLabel(vertLabel,  vertH)
    if vertH.isValid():
        vertices = vertH.product()
        
    #num of true interations
    if not options.useData:
        event.getByLabel(puInfoLabel, puInfoHandle)
        if puInfoHandle.isValid():
            nPV = puInfoHandle.product()
        
        sumNvtx = 0.0    
        for iPV in nPV:
            npv = iPV.getPU_NumInteractions()
            sumNvtx += float(npv)

        aveNvtx = sumNvtx/3.    
        #print 'outside nPV', npv , 'Ave', aveNvtx

    # use this if we want to fill barrel/endcap histograms
    dirindex=0
    dirlist=[0]
    
    # number of leptons
    nMuonsVal = 0
    if muonPts is not None:
        # Now get the rest of the lepton 4-vector 
        event.getByLabel (muonEtaLabel, muonEtaHandle)
        muonEtas = muonEtaHandle.product()
        event.getByLabel (muonPhiLabel, muonPhiHandle)
        muonPhis = muonPhiHandle.product()
        
        for imuonPt in range(0,len(muonPts)):
            muonPt = muonPts[imuonPt]
            if muonPt > muonPtMin:
                if options.useLoose:
                    if muonPfisos[imuonPt] / muonPt < looseMuonIsoMax:
                        continue
                    else:
                        nMuonsVal += 1
                else:
                    nMuonsVal += 1
            nMuons[0].Fill( nMuonsVal, PUweight )
            if options.addDirs:
                if abs(muonEtas[0]) > 1.5:
                    dirindex=2
                else:
                    dirindex=1
                nMuons[dirindex].Fill( nMuonsVal, PUweight )
                
    nElectronsVal = 0   
    if electronPts is not None:
        # Now get the rest of the lepton 4-vector
        event.getByLabel (electronEtaLabel, electronEtaHandle)
        electronEtas = electronEtaHandle.product()
        event.getByLabel (electronPhiLabel, electronPhiHandle)
        electronPhis = electronPhiHandle.product()
        
        if options.barrel and abs(electronEtas[0]) > 1.5: continue
        
        for ielectronPt in range(0,len(electronPts)):
            electronPt = electronPts[ielectronPt]
            if electronPt > electronPtMin:
                nElectronsVal += 1
            nElectrons[0].Fill( nElectronsVal, PUweight )    
            if options.addDirs:
                if abs(electronEtas[0]) > 1.5:
                    dirindex=2
                else:
                    dirindex=1   
                nElectrons[dirindex].Fill( nElectronsVal, PUweight )
            
    if dirindex>0:
        nEvents[dirindex].Fill(count, PUweight)
        dirlist.append(dirindex)

    #Require exactly one lepton
    if muonPts is None and electronPts is None:
        continue
    # to be sure...
    if nElectronsVal+nMuonsVal != 1:
        continue
    
    #number of 1 lepton
    cutFlow[1][0] += 1

    if options.lepType == 0 and muonPts is None:
        continue
    if options.lepType == 1 and electronPts is None:
        continue
    # to be sure again
    if options.lepType == 0 and nMuonsVal!=1:
        continue
    if options.lepType == 1 and nElectronsVal!=1:
        continue

        
    ##number of 1 lepton and no other lepton
    cutFlow[2][0] += 1
        
    # Now get the MET
    event.getByLabel( metLabel, metHandle )
    if metHandle.isValid():
        metRaw = metHandle.product()[0]
        event.getByLabel( metPhiLabel, metPhiHandle )
        metPhiRaw = metPhiHandle.product()[0]
    else:
        continue  # if MET reconstruction failed

    jets = []
    btaggedJets = []
    ttaggedJets = []
    met_px = metRaw * math.cos( metPhiRaw )
    met_py = metRaw * math.sin( metPhiRaw )

    # Now get the Jets
    event.getByLabel( jetPtLabel, jetPtHandle )
    jetPts = jetPtHandle.product()
    if not options.useData:
        event.getByLabel( genJetPtLabel, genJetPtHandle )
        if genJetPtHandle.isValid(): 
            genJetPts = genJetPtHandle.product()
        elif abs(options.jetSmear)>0.0001:
            print "You want to use jetSmear but there is no genJetPt collection!!"
            exit()
    event.getByLabel( jetEtaLabel, jetEtaHandle )
    jetEtas = jetEtaHandle.product()
    event.getByLabel( jetPhiLabel, jetPhiHandle )
    jetPhis = jetPhiHandle.product()
    event.getByLabel( jetMassLabel, jetMassHandle )
    jetMasses = jetMassHandle.product()
    
    #JES and JER
    for ijet in range(0,len(jetPts) ):
        jetScale = 1.0
        if not options.useData and abs(jecScale) > 0.0001:
            #print 'Modifying jet pts according to jecScale = ' + str(jecScale)
            jecUnc.setJetEta( jetEtas[ijet] )
            jecUnc.setJetPt( jetPts[ijet] )

            upOrDown = bool(jecScale > 0.0)

            unc1 = abs(jecUnc.getUncertainty(upOrDown))
            unc2 = flatJecUnc
            unc = math.sqrt(unc1*unc1 + unc2*unc2)
            #print 'Correction = ' + str( 1 + unc * jecScale)
            jetScale = 1 + unc * jecScale

        ## also do Jet energy resolution variation 
        if not options.useData and abs(options.jetSmear)>0.0001 and genJetPts[ijet]>15.0:
            scale = options.jetSmear
            recopt = jetPts[ijet]
            genpt = genJetPts[ijet]
            deltapt = (recopt-genpt)*scale
            ptscale = max(0.0, (recopt+deltapt)/recopt)
            jetScale*=ptscale

        ## get the uncorrected jets
        thisJet = ROOT.TLorentzVector()
        thisJet.SetPtEtaPhiM(jetPts[ijet],
                             jetEtas[ijet],
                             jetPhis[ijet],
                             jetMasses[ijet])
        
        #remove the uncorrected jets
        met_px = met_px + thisJet.Px()
        met_py = met_py + thisJet.Py()
## """ 
##         #unclustered MET resolution
##         unclMETScale = 1.0
##         if not options.useData and abs(metScale)> 0.0:
##             #remove the electron and muon
##             if muonPts is not None:
##                 for imuonPt in range(0,len(muonPts)):
##                     muonPt = muonPts[imuonPt]
##                     muonPhi = muonsPhis[imuonPt]
##                     mu_px = muonPts[imuonPt]*math.cos(muonPhis[imuonPt])
##                     mu_py = muonPts[imuonPt]*math.sin(muonPhis[imuonPt])
##                     met_px = met_px + mu_px 
##                     met_py = met_py + mu_py 
##             if electronPts is not None:
##                 for ielectronPt in range(0,len(electronPts)):
##                     electronPt = electronPts[ielectronPt]
##                     electronPhi = electronPhis[ielectronPt]
##                     el_px = electronPts[ielectronPt]*math.cos(electronPhis[ielectronPt])
##                     el_py = electronPts[ielectronPt]*math.sin(electronPhis[ielectronPt])
##                     met_px = met_px + el_px
##                     met_py = met_py + el_py
                    
##             #apply the 10% variation of 0.9 or 1.1
##             unclMETScale = 1 +  0.1*metScale
##             met_px = met_px*unclMETScale
##             met_py = met_py*unclMETScale
            
##             #add back the electron and muon
##             if muonPts is not None:
##                 for imuonPt in range(0,len(muonPts)):
##                     muonPt = muonPts[imuonPt]
##                     muonPhi = muonsPhis[imuonPt]
##                     mu_px = muonPts[imuonPt]*math.cos(muonPhis[imuonPt])
##                     mu_py = muonPts[imuonPt]*math.sin(muonPhis[imuonPt])
##                     met_px = met_px - mu_px 
##                     met_py = met_py - mu_py 
##             if electronPts is not None:
##                 for ielectronPt in range(0,len(electronPts)):
##                     electronPt = electronPts[ielectronPt]
##                     electronPhi = electronPhis[ielectronPt]
##                     el_px = electronPts[ielectronPt]*math.cos(electronPhis[ielectronPt])
##                     el_py = electronPts[ielectronPt]*math.sin(electronPhis[ielectronPt])
##                     met_px = met_px - el_px
##                     met_py = met_py - el_py  
## """
        #apply the SF and add back the jets and also correct the MET
        thisJet = thisJet * jetScale
        met_px = met_px - thisJet.Px()
        met_py = met_py - thisJet.Py()
        #if thisJet.Pt() > jetPtMin:
        jets.append( thisJet )

    met = math.sqrt(met_px*met_px + met_py*met_py)
    #print 'met = ', met
    #print 'nJets: ', len(jets), 'minJets required: ', minJets
   
    #throw the event to mimick the final jets of pt >30 GeV(edmNtuple cut) for data(TriCentralJet30)  
    if len(jets) < minJets:
        continue
         
    # cutting on met after scaling
    if not options.invMET and met < metMin:
        continue
    elif options.invMET and met >= metMin:
        #print 'met = ', met, 'minMin = ',metMin 
        continue
    
    cutFlow[3][0] += 1
    for idir in dirlist:
        nMETs[idir].Fill(met, PUweight)
    
    # cut on jet pt
    njets = 0
    for jet in jets:
        #print jet.Pt()
        if jet.Pt() > jetPtMin:
            njets += 1
    
    #very important, fill only the properties after right amount of jets
    #print 'minJets =', minJets, 'njets =' , njets, 'jetPt =' , jetPtMin
    if njets < minJets:
        continue    
    
    cutFlow[4][0] += 1

    if njets > 2:
        cutFlow[5][0] += 1
        for idir in dirlist:
            nJets3[idir].Fill(njets, PUweight)

    # possibly not needed?
    if False and not options.useData and options.useEleHad and njets > 2:
        # BELOW IS DISABLED
        if jets[2].Pt() >= 35.0 and jets[2].Pt() < 37.5:
            PUweight = PUweight * 0.87
        elif jets[2].Pt() >=37.5 and jets[2].Pt() < 40.0:          
            PUweight = PUweight * 0.92
        elif jets[2].Pt() >= 40.0 and jets[2].Pt() < 45.0:          
            PUweight = PUweight * 0.94                      
        elif jets[2].Pt() >= 45.0 and jets[2].Pt() < 50.0:          
            PUweight = PUweight * 0.96                       
        elif jets[2].Pt() >= 50.0 and jets[2].Pt() < 55.0:          
            PUweight = PUweight * 0.99            
        elif jets[2].Pt() >= 55.0 and jets[2].Pt() < 60.0:          
            PUweight = PUweight * 1.0
        elif jets[2].Pt() >= 60.0 and jets[2].Pt() < 65.0:          
            PUweight = PUweight * 0.98
        elif jets[2].Pt() >= 65.0 and jets[2].Pt() < 70.0:          
            PUweight = PUweight * 0.99    
        elif jets[2].Pt() >= 70:
             PUweight = PUweight * 1.0 
             

    #print 'PUweight after----------', PUweight        
    ##variables to be filled:
    ##_____________________
    for idir in dirlist:
        nVertices[idir].Fill(vertices.size(), PUweight)
        if not options.useData:
            npuTruth[idir].Fill(aveNvtx, 1)
            npuReweight[idir].Fill(aveNvtx, PUweight)
            
    lepEta = -999.0
    lepPt  = -999.0   
    lepPhi = -999.0
    lepPFIso = -999.0
    
    if options.lepType == 0:
        lepEta = muonEtas[0]
        lepPt  = muonPts[0]
        lepPhi = muonPhis[0]
        lepPFIso = muonPfisos[0]/lepPt
    else:
        lepEta = electronEtas[0]
        lepPt  = electronPts[0]
        lepPhi = electronPhis[0]        
        lepPFIso = electronPfisos[0]/lepPt
        #print 'lepPFIso = ', lepPFIso, 'lep Pt = ', lepPt, 'iso = ', electronPfisos[0]
    for idir in dirlist:
        elePt[idir].Fill( lepPt, PUweight )
        eleEta[idir].Fill( lepEta, PUweight )
        
        elePhi[idir].Fill( lepPhi, PUweight )
        elePFIso[idir].Fill( lepPFIso, PUweight)
    
    hT = lepPt + met
    #print 'hT after met ', hT
    
    lep_px = lepPt * math.cos( lepPhi )
    lep_py = lepPt * math.sin( lepPhi )
    wPt = lepPt + met
    wPx = lep_px + met_px
    wPy = lep_py + met_py
    wMT = math.sqrt(wPt*wPt-wPx*wPx-wPy*wPy)
    #print 'wMT = ', wMT
    
    #M3 for >=3 jets
    M3 = 0.0
    highestPt = 0.0
    if njets >= 3:
        for j in range(0, njets-2):
            for k in range(j+1, njets-1):
                for l in range(k+1, njets):
                    threeJets = jets[j] + jets[k] + jets[l]
                    if highestPt < threeJets.Perp():
                        M3 = threeJets.M()
                        highestPt=threeJets.Perp()
    for idir in dirlist:
        m3[idir].Fill(M3, PUweight)
    #print 'M3 = ', M3
    
    # Now get the number of SSVHEM tags and vertex mass.
    # If using MC, get the jet flavor also
    event.getByLabel (jetSSVHELabel, jetSSVHEHandle)
    jetSSVHEs = jetSSVHEHandle.product()
    event.getByLabel( jetSecvtxMassLabel, jetSecvtxMassHandle )
    jetSecvtxMasses = jetSecvtxMassHandle.product()
    if not options.useData:
        event.getByLabel( jetFlavorLabel, jetFlavorHandle )
        jetFlavors = jetFlavorHandle.product()
    # grab the different tau products
    
    event.getByLabel( tauDB3HitMediumLabel, tauTagHandle )
    tauIDs = tauTagHandle.product()
    event.getByLabel( jetTauPtLabel, jetTauPtHandle )
    tauPts = jetTauPtHandle.product()
    event.getByLabel( jetTauEtaLabel, jetTauEtaHandle )
    tauEtas = jetTauEtaHandle.product()
    event.getByLabel( jetTauPhiLabel, jetTauPhiHandle )
    tauPhis = jetTauPhiHandle.product()
    event.getByLabel( jetTauMassLabel, jetTauMassHandle )
    tauMasses = jetTauMassHandle.product()
    #tauDB3HitMediumHandle         = Handle( "std::vector<float>" )
    #tauDB3HitMediumLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byLooseCombinedIsolationDeltaBetaCorr3Hits" )
    #tauDB3HitTightHandle         = Handle( "std::vector<float>" )
    #tauDB3HitTightLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byLooseCombinedIsolationDeltaBetaCorr3Hits" )
    #tauMVALooseHandle         = Handle( "std::vector<float>" )
    #tauMVALooseLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byLooseIsolationMVA2" )
    #tauMVAMediumHandle         = Handle( "std::vector<float>" )
    #tauMVAMediumLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byMediumIsolationMVA2" )
    #tauMVATightHandle         = Handle( "std::vector<float>" )
    #tauMVATightLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "byTightIsolationMVA2" )


    # Compute the number of tags, the secondary vertex mass,
    # and the jet flavor (MC only)
    nbtags = 0
    nttags = 0
    secvtxMass = 0.0
    flavorIndex = -1
    numB = 0
    numC = 0
    numQ = 0
    sumEt = 0.
    sumPt = 0.
    sumE = 0.
    deltaR = 5.0
    jet1Pt = -1.0
    effs = []
    # The vertex mass for the event is the vertex mass
    # of the first tagged jet (ordered by pt).
    # The flavor for the event is the highest flavor
    # in the event out of b, c, and light flavor.
    for ijet in range(0,len(jets)):
        jetP4 = jets[ijet]
        # all jets above certain threshold
        if jetP4.Pt() < jetPtMin:
            continue
        #if jet1Pt < 0.0:
        #    jet1Pt = jetP4.Pt()
        deta = jetP4.Eta() - lepEta
        dphi = jetP4.Phi() - lepPhi
        if dphi >= math.pi: dphi -= 2*math.pi
        elif dphi < -math.pi: dphi += 2*math.pi    
        deltaR = TMath.Min ( math.sqrt(deta*deta + dphi*dphi), deltaR)
        
        hT    = hT + jetP4.Et()    
        sumEt = sumEt + jetP4.Et()
        sumPt = sumPt + jetP4.Pt()
        sumE = sumE + jetP4.E()
        ssvhe = jetSSVHEs[ijet]
        isf = 1.0
        iflavor = -1
        if not options.useData:
            jetFlavor = jetFlavors[ijet]
            
            #print 'jet flavor = ' + str(jetFlavor)
            if abs(jetFlavor) == 5:
                numB = numB + 1
                isf = sfB
                iflavor = 0
            elif abs(jetFlavor) == 4:
                numC = numC + 1
                isf = sfC
                iflavor = 1
            else:
                numQ = numQ + 1
                isf = sfQ
                iflavor = 2
        # Only consider tagged jets for the vertex mass
        if ssvhe > ssvheCut:
            nbtags += 1
            btaggedJets.append( jetP4 )
            # The
            if secvtxMass <= 0.0001: # Stop at the first nontrivial secvtx mass
                secvtxMass = jetSecvtxMasses[ijet]
        
        tauid  = tauIDs[ijet]
        taueta = tauEtas[ijet]
        taupt  = tauPts[ijet]
        tauphi = tauPhis[ijet]
        taumass= tauMasses[ijet]
        if tauid > tauIdCut:
            nttags += 1
            ttaggedJets.append( jetP4 )


        # TODO: ADD TAU SF WEIGHTING
        # For the SF weighting, use:
        # the scale factors if tagged
        # zero if not tagged
        if not options.useData:
            if ssvhe > ssvheCut:
                effs.append( EffInfo(ijet, isf, iflavor) )
            else:
                effs.append( EffInfo(ijet, 0.0, iflavor) )

    if numB > 0:
        flavorIndex = 0
    elif numC > 0:
        flavorIndex = 1
    else:
        flavorIndex = 2
    for idir in dirlist:
        if not options.useData and secvtxMass > 0.0001:
            if   numB > 0: bmass[idir].Fill(secvtxMass, PUweight)
            elif numC > 0: cmass[idir].Fill(secvtxMass, PUweight)
            elif numQ > 0: lfmass[idir].Fill(secvtxMass, PUweight)

        nJets[idir].Fill( njets, PUweight )
        nBTags[idir].Fill( nbtags, PUweight )
        nTTags[idir].Fill( nttags, PUweight )
        lepJetdR[idir].Fill( deltaR, PUweight)
    
    if njets > maxJets:
        njets = maxJets
        
    if nbtags > maxBTags:
        nbtags = maxBTags

    if nttags > maxTTags:
        nttags = maxTTags
        
    #if not options.useData:
    #    print 'Njets = {0:6.0f}, Ntags = {1:6.0f}, flavorIndex = {2:3.0f}, histname = {3:12s}'.format(
    #        njets, ntags, flavorIndex, secvtxMassPlots[njets][ntags][flavorIndex].GetName() )
        
    #else:
    #    print 'Njets = {0:6.0f}, Ntags = {1:6.0f}, histname = {2:12s}'.format(
    #        njets, ntags, secvtxMassPlots[njets][ntags][3].GetName() )

    # Now fill discriminator variables
    
    if njets >= 2:
        taggedJet0 = jets[0]
        taggedJet1 = jets[1]
        bbCand = taggedJet0 + taggedJet1
        imbb = bbCand.M()
        idR = taggedJet0.DeltaR( taggedJet1 )
        for idir in dirlist:
            mbb[njets][idir].Fill( imbb, PUweight )
            dRbb[njets][idir].Fill( idR, PUweight )
            
    for idir in dirlist:
        if nbtags >= 1: 
            ptJet0[idir].Fill(jets[0].Pt(), PUweight )
            if njets>1:
                ptJet1[idir].Fill(jets[1].Pt(), PUweight ) 
            if njets>2:    
                ptJet2[idir].Fill(jets[2].Pt(), PUweight )
            if njets>3:    
                ptJet3[idir].Fill(jets[3].Pt(), PUweight )
            if njets>4:
                for j in range(4, njets):
                    ptJet4[idir].Fill(jets[j].Pt(), PUweight )# loop over 5th to njets

    for idir in dirlist:
        if njets >= 3 and nbtags >= 1:
            nVertices3j1t[idir].Fill(vertices.size(), PUweight)
            if not options.useData:
                npuTruth3j1t[idir].Fill(aveNvtx, 1)
                npuReweight3j1t[idir].Fill(aveNvtx, PUweight)
            elePt3j1t[idir].Fill(lepPt, PUweight)
            eleEta3j1t[idir].Fill(lepEta, PUweight)
            elePhi3j1t[idir].Fill(lepPhi, PUweight)
            elePFIso3j1t[idir].Fill(lepPFIso, PUweight)
            wMT3j1t[idir].Fill(wMT, PUweight)
            hT3j1t[idir].Fill(hT, PUweight)
            m3j1t[idir].Fill(M3, PUweight)        
            met3j1t[idir].Fill(met, PUweight)
            ptJet0_3j1t[idir].Fill(jets[0].Pt(), PUweight )
            if njets>1:
                ptJet1_3j1t[idir].Fill(jets[1].Pt(), PUweight ) 
            if njets>2:    
                ptJet2_3j1t[idir].Fill(jets[2].Pt(), PUweight )
            if njets>3:    
                ptJet3_3j1t[idir].Fill(jets[3].Pt(), PUweight )
            if njets>4:
                for j in range(4, njets):
                    ptJet4_3j1t[idir].Fill(jets[j].Pt(), PUweight )# loop over 5th to njets
                    
    if options.useData:
        # always fill the "total"
        for idir in dirlist:
            if nbtags > 0:
                secvtxMassPlots[njets][nbtags][3][idir].Fill( secvtxMass, PUweight )
            nPVPlots[njets][nbtags][3][idir].Fill( vertices.size(), PUweight )
            lepEtaPlots[njets][nbtags][3][idir].Fill( lepEta, PUweight )
            lepPtPlots[njets][nbtags][3][idir].Fill( lepPt, PUweight )
            centralityPlots[njets][nbtags][3][idir].Fill( sumEt / sumE, PUweight )
            sumEtPlots[njets][nbtags][3][idir].Fill( sumEt, PUweight )
            #jet1PtPlots[njets][nbtags][3][idir].Fill( jet1Pt, PUweight )
            METPlots[njets][nbtags][3][idir].Fill( met, PUweight )
            wMTPlots[njets][nbtags][3][idir].Fill( wMT, PUweight )
            hTPlots[njets][nbtags][3][idir].Fill( hT, PUweight )

            if nbtags > 0:
                secvtxMassPlotsTau[njets][nbtags][nttags][3][idir].Fill( secvtxMass, PUweight )
            nPVPlotsTau[njets][nbtags][nttags][3][idir].Fill( vertices.size(), PUweight )
            lepEtaPlotsTau[njets][nbtags][nttags][3][idir].Fill( lepEta, PUweight )
            lepPtPlotsTau[njets][nbtags][nttags][3][idir].Fill( lepPt, PUweight )
            centralityPlotsTau[njets][nttags][nbtags][3][idir].Fill( sumEt / sumE, PUweight )
            sumEtPlotsTau[njets][nbtags][nttags][3][idir].Fill( sumEt, PUweight )
            #jet1PtPlots[njets][nbtags][3][idir].Fill( jet1Pt, PUweight )
            METPlotsTau[njets][nbtags][nttags][3][idir].Fill( met, PUweight )
            wMTPlotsTau[njets][nbtags][nttags][3][idir].Fill( wMT, PUweight )
            hTPlotsTau[njets][nbtags][nttags][3][idir].Fill( hT, PUweight )


            if flavorIndex >= 0:
                if nbtags > 0:
                    secvtxMassPlots[njets][nbtags][flavorIndex][idir].Fill( secvtxMass, PUweight ) # Fill each jet flavor individually
                nPVPlots[njets][nbtags][flavorIndex][idir].Fill( vertices.size(), PUweight )    
                lepEtaPlots[njets][nbtags][flavorIndex][idir].Fill( lepEta, PUweight )
                lepPtPlots[njets][nbtags][flavorIndex][idir].Fill( lepPt, PUweight )
                centralityPlots[njets][nbtags][flavorIndex][idir].Fill( sumEt / sumE, PUweight )
                sumEtPlots[njets][nbtags][flavorIndex][idir].Fill( sumEt, PUweight )
                #jet1PtPlots[njets][nbtags][flavorIndex][idir].Fill( jet1Pt, PUweight )
                METPlots[njets][nbtags][flavorIndex][idir].Fill( met, PUweight )
                wMTPlots[njets][nbtags][flavorIndex][idir].Fill( wMT, PUweight )
                hTPlots[njets][nbtags][flavorIndex][idir].Fill( hT, PUweight )

            if flavorIndex >= 0:
                if nbtags > 0:
                    secvtxMassPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( secvtxMass, PUweight ) # Fill each jet flavor individually
                nPVPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( vertices.size(), PUweight )    
                lepEtaPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( lepEta, PUweight )
                lepPtPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( lepPt, PUweight )
                centralityPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( sumEt / sumE, PUweight )
                sumEtPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( sumEt, PUweight )
                #jet1PtPlotsTau[njets][nbtags][flavorIndex][idir].Fill( jet1Pt, PUweight )
                METPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( met, PUweight )
                wMTPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( wMT, PUweight )
                hTPlotsTau[njets][nbtags][nttags][flavorIndex][idir].Fill( hT, PUweight )

    else:

        # otherwise, loop over all of the SF combinatorics to tag itag out of njet jets
        # and weight the distributions by the resultant probability. 
        effCombos = EffInfoCombinations( effs, verbose=False )
        # TODO blergh - add the tau tagging probability

        for itag in range(0,njets+1):
            pTag = effCombos.pTag( itag )
            jtag = itag
            if jtag > maxBTags:
                jtag = maxBTags
            # use pileup reweighting factor
            pTag*=PUweight
            # always fill the "total"
            for idir in dirlist:
                if jtag > 0:
                    secvtxMassPlots[njets][jtag][3][idir].Fill( secvtxMass, pTag )
                nPVPlots[njets][jtag][3][idir].Fill( vertices.size(), pTag)    
                lepEtaPlots[njets][jtag][3][idir].Fill( lepEta, pTag )
                lepPtPlots[njets][jtag][3][idir].Fill( lepPt, pTag )
                centralityPlots[njets][jtag][3][idir].Fill( sumEt / sumE, pTag )
                sumEtPlots[njets][jtag][3][idir].Fill( sumEt, pTag )
                #jet1PtPlots[njets][jtag][3][idir].Fill( jet1Pt, pTag )
                METPlots[njets][jtag][3][idir].Fill( met, pTag )
                wMTPlots[njets][jtag][3][idir].Fill( wMT, pTag )
                hTPlots[njets][jtag][3][idir].Fill( hT, pTag )

                # for tau histograms
                if jtag > 0:
                    secvtxMassPlotsTau[njets][jtag][nttags][3][idir].Fill( secvtxMass, pTag )
                nPVPlotsTau[njets][jtag][nttags][3][idir].Fill( vertices.size(), pTag)    
                lepEtaPlotsTau[njets][jtag][nttags][3][idir].Fill( lepEta, pTag )
                lepPtPlotsTau[njets][jtag][nttags][3][idir].Fill( lepPt, pTag )
                centralityPlotsTau[njets][jtag][nttags][3][idir].Fill( sumEt / sumE, pTag )
                sumEtPlotsTau[njets][jtag][nttags][3][idir].Fill( sumEt, pTag )
                #jet1PtPlots[njets][jtag][3][idir].Fill( jet1Pt, pTag )
                METPlotsTau[njets][jtag][nttags][3][idir].Fill( met, pTag )
                wMTPlotsTau[njets][jtag][nttags][3][idir].Fill( wMT, pTag )
                hTPlotsTau[njets][jtag][nttags][3][idir].Fill( hT, pTag )

                if flavorIndex >= 0:
                    if jtag > 0:
                        secvtxMassPlots[njets][jtag][flavorIndex][idir].Fill( secvtxMass, pTag ) # Fill each jet flavor individually
                    nPVPlots[njets][jtag][flavorIndex][idir].Fill( vertices.size(), pTag)    
                    lepEtaPlots[njets][jtag][flavorIndex][idir].Fill( lepEta, pTag )
                    lepPtPlots[njets][jtag][flavorIndex][idir].Fill( lepPt, pTag )
                    centralityPlots[njets][jtag][flavorIndex][idir].Fill( sumEt / sumE, pTag )
                    sumEtPlots[njets][jtag][flavorIndex][idir].Fill( sumEt, pTag )
                    #jet1PtPlots[njets][jtag][flavorIndex][idir].Fill( jet1Pt, pTag )
                    METPlots[njets][jtag][flavorIndex][idir].Fill( met, pTag )
                    wMTPlots[njets][jtag][flavorIndex][idir].Fill( wMT, pTag )
                    hTPlots[njets][jtag][flavorIndex][idir].Fill( hT, pTag )

                    if jtag > 0:
                        secvtxMassPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( secvtxMass, pTag ) # Fill each jet flavor individually
                    nPVPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( vertices.size(), pTag)    
                    lepEtaPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( lepEta, pTag )
                    lepPtPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( lepPt, pTag )
                    centralityPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( sumEt / sumE, pTag )
                    sumEtPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( sumEt, pTag )
                    #jet1PtPlots[njets][jtag][flavorIndex][idir].Fill( jet1Pt, pTag )
                    METPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( met, pTag )
                    wMTPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( wMT, pTag )
                    hTPlotsTau[njets][jtag][nttags][flavorIndex][idir].Fill( hT, pTag )




print '----- Cut Flow -----'
for cut in cutFlow:
    print '{0:15s} = {1:10.0f}'.format(
        cut[1], cut[0]
        )

f.cd()
f.Write()
f.Close()
