#! /usr/bin/env python

from __future__ import print_function

# Import everything from ROOT
from ROOT import *
gROOT.Macro("~/rootlogon.C")

import sys
import glob
import math

def isVTagged(ca8jet):
    pt = ca8jet.pt()    
    mass = ca8jet.mass()
    subjet1M = ca8jet.daughter(0).mass() 
    subjet2M = ca8jet.daughter(1).mass()
    mu = max(subjet1M,subjet2M) / ca8jet.correctedJet("Uncorrected").mass()    
    if mu < 0.4 and (mass < 150 and mass > 50) and pt > 200:
        return True
    else:
        return False

def isBTagged(ak5jet):
    bjet=0
    if options.data:
        if ak5jet.bDiscriminator('combinedSecondaryVertexBJetTags') >= 0.679 :
             bjet=1
    else:
        if options.bTag == "OutOfBox" :
            if (ak5jet.userInt('btagRegular') & 1) == 1 :
                bjet=1
        elif options.bTag == "" :
            if (ak5jet.userInt('btagRegular') & 2) == 2 :
                bjet=1
        elif options.bTag =="BTagSFup" :
            if (ak5jet.userInt('btagRegular') & 4) == 4 :
                bjet=1
        elif options.bTag =="BTagSFdown" :
            if (ak5jet.userInt('btagRegular') & 8) == 8 :
                bjet=1
    if bjet==1:
        return True
    else:
        return False

def isTightMu(lep, PVz):
    isPF      =  lep.isPFMuon()
    isGlob    =  lep.isGlobalMuon()
    if isPF and isGlob:    
        normChi2  =  lep.globalTrack().normalizedChi2()
        trkLayers =  lep.track().hitPattern().trackerLayersWithMeasurement()
        mVMuHits  =  lep.globalTrack().hitPattern().numberOfValidMuonHits()
        dB        =  fabs( lep.dB() )
        diffVz    =  fabs( lep.vertex().z() - PVz )
        mPixHits  =  lep.innerTrack().hitPattern().numberOfValidPixelHits()
        matchStat =  lep.numberOfMatchedStations()
    
    if(isPF and isGlob and normChi2<10 and trkLayers>5 and mVMuHits>0 and dB<0.2 and diffVz<0.5 and mPixHits>0 and matchStat >1):
        return True
    else:
        return False
    
def deltaR( eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = phi1 - phi2
    if dphi >= math.pi: dphi -= 2*math.pi
    elif dphi < -math.pi: dphi += 2*math.pi
    return math.sqrt(deta*deta + dphi*dphi)

def smear_factor(eta, variation):
    abseta = abs(eta)
    smear_nominal = 0.0
    smear_up = 0.0
    smear_down = 0.0

    if abseta <= 0.5:
                smear_nominal = 0.052
                smear_up = 0.115
                smear_down = 0.0
    elif abseta <= 1.1:
                smear_nominal = 0.057
                smear_up = 0.114
                smear_down = 0.001
    elif abseta <= 1.7:
                smear_nominal = 0.096
                smear_up = 0.161
                smear_down = 0.032
    elif abseta <= 2.3:
                smear_nominal = 0.134
                smear_up = 0.228
                smear_down = 0.042
    elif abseta < 5.0:
                smear_nominal = 0.288
                smear_up = 0.488
                smear_down = 0.089

    if variation == 0: return smear_nominal
    elif variation == 1: return smear_up
    elif variation == -1: return smear_down
    
#SF for HLT_Mu40
def muonTrig_SF(eta, pt):    
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.90:
        if pt >= 40.   and pt < 50.  : SF = 0.9810
        elif pt >= 50. and pt < 60.  : SF = 0.9810
        elif pt >= 60. and pt < 90.  : SF = 0.9806
        elif pt >= 90. and pt < 140. : SF = 0.9786
        elif pt >= 140. and pt < 500.: SF = 0.9810
        else: SF = 0.9810    
    elif abseta >= 0.90 and abseta < 1.2:
        if pt >= 40.   and pt < 50.  : SF = 0.9626
        elif pt >= 50. and pt < 60.  : SF = 0.9570
        elif pt >= 60. and pt < 90.  : SF = 0.9528
        elif pt >= 90. and pt < 140. : SF = 0.9504
        elif pt >= 140. and pt < 500.: SF = 1.0088
        else: SF = 1.0088    
    elif abseta >= 1.2 and abseta < 2.1:
        if pt >= 40.   and pt < 50.  : SF = 0.9931
        elif pt >= 50. and pt < 60.  : SF = 0.9894
        elif pt >= 60. and pt < 90.  : SF = 0.9827
        elif pt >= 90. and pt < 140. : SF = 0.9908
        elif pt >= 140. and pt < 500.: SF = 0.9970
        else: SF = 0.9970     
    return SF

# SF for muon ID (Tight && relIso <0.12)
def muonID_SF(eta):
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.90:
        SF = 0.9943
    elif abseta >= 0.90 and abseta < 1.2:    
        SF = 0.9933
    elif abseta >= 1.2 and abseta < 2.1:
        SF = 1.0020  
    return SF

# SF for HLT_Ele27_WP80
def electronTrig_SF(eta, pt):    
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.80:
        if pt >= 20. and pt < 30.:
            SF = 0.695
        elif pt >= 30. and pt < 40.:
            SF = 0.984
        elif pt >= 40. and pt < 50.:
            SF = 0.999
        elif pt > 50. and pt < 200.:
            SF = 0.999
        else: SF = 0.999    
    elif abseta >= 0.80 and abseta < 1.48:
        if pt >= 20. and pt < 30.:
            SF = 0.462
        elif pt >= 30. and pt < 40.:
            SF = 0.967
        elif pt >= 40. and pt < 50.:
            SF = 0.983
        elif pt > 50. and pt < 200.:
            SF = 0.988
        else: SF = 0.988    
    elif abseta >= 1.48 and abseta < 2.50:
        if pt >= 20. and pt < 30.:
            SF = 0.804
        elif pt >= 30. and pt < 40.:
            SF = 0.991
        elif pt >= 40. and pt < 50.:
            SF = 1.018
        elif pt > 50. and pt < 200.:
            SF = 0.977
        else: SF = 0.977    
    return SF

# SF for electron ID (MVA >0.9 && relIso <0.1)
def electronID_SF(eta, pt):
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.80:
        if pt >= 20. and pt < 30.:
            SF = 0.972
        elif pt >= 30. and pt < 40.:
            SF = 0.950
        elif pt >= 40. and pt < 50.:
            SF = 0.966
        elif pt > 50. and pt < 200.:
            SF = 0.961
        else: SF = 0.961    
    elif abseta >= 0.80 and abseta < 1.48:
        if pt >= 20. and pt < 30.:
            SF = 0.928
        elif pt >= 30. and pt < 40.:
            SF = 0.957
        elif pt >= 40. and pt < 50.:
            SF = 0.961
        elif pt > 50. and pt < 200.:
            SF = 0.963
        else: SF = 0.963    
    elif abseta >= 1.48 and abseta < 2.50:
        if pt >= 20. and pt < 30.:
            SF = 0.834
        elif pt >= 30. and pt < 40.:
            SF = 0.922
        elif pt >= 40. and pt < 50.:
            SF = 0.941
        elif pt > 50. and pt < 200.:
            SF = 0.971
        else: SF = 0.971    
    return SF


from array import array
from optparse import OptionParser

# Create a command line option parser
parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  default = "",
                  dest='files',
                  help='Input files')

parser.add_option('--txtfiles', metavar='F', type='string', action='store',
                  default = "edmTest.root",
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
                  default=0,
                  dest='jetPtSmear',
                  help='JER smearing. Standard values are 0 (nominal), -1 (down), 1 (up)')

parser.add_option('--jetEtaSmear', metavar='F', type='float', action='store',
                  default=0.0,
                  dest='jetEtaSmear',
                  help='Jet Phi smearing. Standard values are 0.1 (up), 0.0 (nominal), 0.2 (down)')

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
                  help="b-tag SF, Options as '', BTagSFup, BTagSFdown")

parser.add_option("--useBPrimeGenInfo",  action='store_true',
                  default=False,
                  dest="useBPrimeGenInfo",
                  help="switch on(1) / off(0) gen particle info")

parser.add_option('--ak5jetPtMin', metavar='F', type='float', action='store',
                  default=30.,
                  dest='ak5jetPtMin',
                  help='jet pt threshold')

parser.add_option('--lepPtMin', metavar='F', type='float', action='store',
                  default=30.,
                  dest='lepPtMin',
                  help='lepton pt threshold')

parser.add_option("--runDataLoose", action='store_true',
                  default=False,
                  dest="runDataLoose",
                  help="to run over loose leptons in data")

# Parse and get arguments
(options, args) = parser.parse_args()

jetPtMin = options.ak5jetPtMin
lepPtMin = options.lepPtMin
runMu = options.runMuons
bprimeGenInfo = options.useBPrimeGenInfo
dcache = options.onDcache
runDataLoose = options.runDataLoose

print('options', options)

if options.runMuons:
    lepStr = 'Mu'
else:
    lepStr = 'Ele'

condStr = ''    
if runDataLoose and options.data:
    condStr = 'Loose'
    
print('lepType', lepStr)
print('Loose?', condStr)
 
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
    files = glob.glob( options.files )
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
    
fname = options.txtfiles
fileN = fname[fname.rfind('/')+1:]
#sys.exit(0)

#JEC
jecParStr = std.string('Jec12_V3_MC_Uncertainty_AK5PFchs.txt')
jecUnc = JetCorrectionUncertainty( jecParStr )
  
#------------------------------------------------------------------

# Get the FWLite "Events"
events = Events (files)

# Get a "handle" (i.e. a smart pointer) to the vector of jets    
muonsH  = Handle ("std::vector<pat::Muon>")
muonsLabel = ("pfTuple"+lepStr+condStr, "muons")

electronsH  = Handle ("std::vector<pat::Electron>")
electronsLabel = ("pfTuple"+lepStr+condStr, "electrons")
      
jetsH = Handle ("std::vector<pat::Jet>")
jetsLabel = ("pfTuple"+lepStr+condStr, "jets")

c8aPruneJetsH = Handle ("std::vector<pat::Jet>")
c8aPruneJetsLabel = ("pfTuple"+lepStr+"CA8Pruned", "jets")

metH = Handle ("std::vector<pat::MET>")
metLabel = ("pfTuple"+lepStr+condStr, "MET")

c8aPruneMetH = Handle ("std::vector<pat::MET>")
c8aPruneMetLabel = ("pfTuple"+lepStr+"CA8Pruned", "MET")

trigH = Handle("pat::TriggerEvent")
trigLabel = ("patTriggerEvent", "")

vertH  = Handle ("std::vector<reco::Vertex>")
vertLabel = ("goodOfflinePrimaryVertices")

pileupWeightsH = Handle ("std::vector<float>")
pileupWeightsLabel = ("pileupReweightingProducer","pileupWeights")

rhoH =  Handle ("double")
rhoLabel = ("kt6PFJets", "rho")

if bprimeGenInfo:
    BBtoWtWt_H  = Handle("int")
    BBtoWtWt_L  = ( "GenInfo", "BBtoWtWt" )
    BBtoWtZb_H  = Handle("int")
    BBtoWtZb_L  = ( "GenInfo", "BBtoWtZb" )
    BBtoZbZb_H  = Handle("int")
    BBtoZbZb_L  = ( "GenInfo", "BBtoZbZb" )
    BBtoZbHb_H  = Handle("int")
    BBtoZbHb_L  = ( "GenInfo", "BBtoZbHb" )
    BBtoWtHb_H  = Handle("int")
    BBtoWtHb_L  = ( "GenInfo", "BBtoWtHb" )
    BBtoHbHb_H  = Handle("int")
    BBtoHbHb_L  = ( "GenInfo", "BBtoHbHb" )
    WPart1_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    WPart1_L    = ( "GenInfo",   "WPart1")
    WPart2_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    WPart2_L    = ( "GenInfo",   "WPart2")
    WPart3_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    WPart3_L    = ( "GenInfo",   "WPart3")
    WPart4_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    WPart4_L    = ( "GenInfo",   "WPart4")
    ZPart1_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    ZPart1_L    = ( "GenInfo",   "ZPart1")
    ZPart2_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    ZPart2_L    = ( "GenInfo",   "ZPart2")
    ZPart3_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    ZPart3_L    = ( "GenInfo",   "ZPart3")
    ZPart4_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    ZPart4_L    = ( "GenInfo",   "ZPart4")    
    HPart1_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    HPart1_L    = ( "GenInfo",   "HPart1")
    HPart2_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    HPart2_L    = ( "GenInfo",   "HPart2")
    HPart3_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    HPart3_L    = ( "GenInfo",   "HPart3")
    HPart4_H    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
    HPart4_L    = ( "GenInfo",   "HPart4")

    
# Create an output file and a tree
systtag = ''

if options.JES == "up" or options.JES == "down":
	systtag = "_JES" + options.JES
elif options.JES != '':
    systtag = "_" + options.JES
if options.bTag != '':
    systtag = "_" + options.bTag
if options.jetPtSmear == -1:
	systtag = "_JERdown"
if options.jetPtSmear == 1:
	systtag = "_JERup"    
    
print("value of systtag = ", systtag)

f = TFile(options.sample + systtag + ".root", "RECREATE")

f.cd()
t = TTree("tree","tree")

if runMu:
    trigSigMuNonIso_path = array('i', [0])
    t.Branch('trigSigMuNonIso_path', trigSigMuNonIso_path, 'trigSigMuNonIso_path/I')
    
    trigSigMuIso_path = array('i', [0])
    t.Branch('trigSigMuIso_path', trigSigMuIso_path, 'trigSigMuIso_path/I')

    trigSigMuIsoHad_path = array('i', [0])
    t.Branch('trigSigMuIsoHad_path', trigSigMuIsoHad_path, 'trigSigMuIsoHad_path/I')

    isMuTight =  array('d',[0.])
    t.Branch('isMuTight',isMuTight,'isMuTight/D')
else:
    trigEleStop_path = array('i', [0])
    t.Branch('trigEleStop_path', trigEleStop_path, 'trigEleStop_path/I')
    
    trigEleHad_path = array('i', [0])
    t.Branch('trigEleHad_path', trigEleHad_path, 'trigEleHad_path/I')
    
    trigSigEle_path = array('i', [0])
    t.Branch('trigSigEle_path', trigSigEle_path, 'trigSigEle_path/I')

    eSCEta = array('d',[0.])
    t.Branch('eSCEta',eSCEta,'eSCEta/D')

    eMVA = array('d', [0.])
    t.Branch('eMVA',eMVA,'eMVA/D')

    eSihih = array('d', [0.])
    t.Branch('eSihih',eSihih,'eSihih/D')

    eHOverE = array('d', [0.])
    t.Branch('eHOverE',eHOverE,'eHOverE/D')

    eDphi = array('d', [0.])
    t.Branch('eDphi',eDphi,'eDphi/D')
    
    eDeta = array('d', [0.])
    t.Branch('eDeta',eDeta,'eDeta/D')

trigSF = array('d', [0.])
t.Branch('trigSF', trigSF, 'trigSF/D')

met = array('d',[0.])
t.Branch('met',met,'met/D')

wMt = array('d',[0.])
t.Branch('wMt',wMt, 'wMt/D')

lepEt = array('d',[0.])
t.Branch('lepEt',lepEt,'lepEt/D')

deltaPhiMETe = array('d',[0.])
t.Branch('deltaPhiMETe', deltaPhiMETe, 'deltaPhiMETe/D')                    

deltaPhiMETLeadingJet = array('d',[0.])
t.Branch('deltaPhiMETLeadingJet', deltaPhiMETLeadingJet, 'deltaPhiMETLeadingJet/D')

lepEta = array('d',[0.])
t.Branch('lepEta',lepEta,'lepEta/D')

lepSF = array('d', [0.])
t.Branch('lepSF', lepSF, 'lepSF/D')

lepd0 =  array('d',[0.])
t.Branch('lepd0',lepd0,'lepd0/D')

lepIso = array('d',[0.])
t.Branch('lepIso',lepIso,'lepIso/D')

lepIsoUncorr = array('d',[0.])
t.Branch('lepIsoUncorr',lepIsoUncorr,'lepIsoUncorr/D')

nvertices = array('i',[0])
t.Branch('nVertices',nvertices,'nVertices/I')

njets = array('i',[0])
t.Branch('njets',njets,'nJets/I')

max_nJets = 30
jetEt = array('d',max_nJets*[0.])
t.Branch('jetEt',jetEt,'jetEt[nJets]/D')

jetEt_ca8 = array('d',max_nJets*[0.])
t.Branch('jetEt_ca8',jetEt_ca8,'jetEt_ca8[nJets]/D')

WjetM = array('d', max_nJets*[0.])
t.Branch('WjetM', WjetM, 'WjetM[nJets]/D')

WjetMu = array('d', max_nJets*[0.])
t.Branch('WjetMu', WjetMu, 'WjetMu[nJets]/D')

if bprimeGenInfo:
    WPt_true = array('d', max_nJets*[-1.])
    t.Branch('WPt_true', WPt_true, 'WPt_true[nJets]/D')
    
    ZPt_true = array('d', max_nJets*[-1.])
    t.Branch('ZPt_true', ZPt_true, 'ZPt_true[nJets]/D')
    
    HPt_true = array('d', max_nJets*[-1.])
    t.Branch('HPt_true', HPt_true, 'HPt_true[nJets]/D')
    
    dR_Wjjqq_match = array('d', max_nJets*[-1.])
    t.Branch('dR_Wjjqq_match',dR_Wjjqq_match,'dR_Wjjqq_match[nJets]/D')
    
    dR_Zjjqq_match = array('d', max_nJets*[-1.])
    t.Branch('dR_Zjjqq_match',dR_Zjjqq_match,'dR_Zjjqq_match[nJets]/D')
    
    dR_Hjjqq_match = array('d', max_nJets*[-1.])
    t.Branch('dR_Hjjqq_match',dR_Hjjqq_match,'dR_Hjjqq_match[nJets]/D')
    
    WtWt = array('i',[0])
    t.Branch('WtWt',WtWt,'WtWt/I')
    
    WtZb = array('i',[0])
    t.Branch('WtZb',WtZb,'WtZb/I')
    
    ZbZb = array('i',[0])
    t.Branch('ZbZb',ZbZb,'ZbZb/I')
    
    ZbHb = array('i',[0])
    t.Branch('ZbHb',ZbHb,'ZbHb/I')
    
    WtHb = array('i',[0])
    t.Branch('WtHb',WtHb,'WtHb/I')
    
    HbHb = array('i',[0])
    t.Branch('HbHb',HbHb,'HbHb/I')

nVTags = array('i',[0])
t.Branch('nVTags',nVTags,'nVTags/I')

nTagsCSVM = array('i',[0])
t.Branch('nTagsCSVM',nTagsCSVM,'nTagsCSVM/I')

nTagsCSVMUncor = array('i',[0])
t.Branch('nTagsCSVMUncor',nTagsCSVMUncor,'nTagsCSVMUncor/I')

bDistriminator = array('d', max_nJets*[0.])
t.Branch('bDistriminator', bDistriminator, 'bDistriminator[nJets]/D')

minDR_je = array('d',[0.])
t.Branch('minDR_je',minDR_je,'minDR_je/D')

minDR_ca8je = array('d',[0.])
t.Branch('minDR_ca8je',minDR_ca8je,'minDR_ca8je/D')

minDR_bV = array('d',max_nJets*[0.])
t.Branch('minDR_bV',minDR_bV,'minDR_bV[nJets]/D')

m3 = array('d',[0.])
t.Branch('m3',m3,'m3/D')

mj = array('d',[0.])
t.Branch('mj',mj,'mj/D')

ht = array('d',[0.])
t.Branch('ht',ht,'ht/D')

sphericity = array('d',[0.])
t.Branch('sphericity',sphericity,'sphericity/D')

aplanarity = array('d',[0.])
t.Branch('aplanarity',aplanarity,'aplanarity/D')

centrality = array('d',[0.])
t.Branch('centrality', centrality,'centrality/D')

if not options.data :
    pileupWeight = array('d',[0.])
    t.Branch('pileupWeight',pileupWeight,'pileupWeight/D')
    
    pileupWeightUp = array('d',[0.])
    t.Branch('pileupWeightUp', pileupWeightUp,'pileupWeightUp/D')
    
    pileupWeightDown = array('d',[0.0])
    t.Branch('pileupWeightDown', pileupWeightDown, 'pileupWeightDown/D')
else:
    runNumber = array('i',[0])
    t.Branch('runNumber',runNumber,'runNumber/I')
    
    eventNumber = array('L',[0])
    t.Branch('eventNumber',eventNumber,'eventNumber/I')
    
    lumiNumber = array('i',[0])
    t.Branch('lumiNumber', lumiNumber,'lumiNumber/I')

# Keep some timing information
nEventsAnalyzed = 0
timer = TStopwatch()
timer.Start()

iWtWt = 0
iWtZb = 0
iZbZb = 0
iZbHb = 0
iWtHb = 0
iHbHb = 0
# loop over events
i = 0 
for event in events:
    i = i + 1
    if i % 1000 == 0 :
    	print("EVENT ", i)
    nEventsAnalyzed = nEventsAnalyzed + 1
    #if nEventsAnalyzed == 10000: break
    # Get the objects 
    event.getByLabel(vertLabel,  vertH)
    event.getByLabel(jetsLabel,  jetsH)
    event.getByLabel(muonsLabel, muonsH)
    event.getByLabel(electronsLabel, electronsH)
    event.getByLabel(metLabel, metH)
    event.getByLabel(trigLabel, trigH)    
    event.getByLabel(c8aPruneJetsLabel,  c8aPruneJetsH)
    event.getByLabel(c8aPruneMetLabel,  c8aPruneMetH)
    event.getByLabel(rhoLabel,  rhoH)
    
    # the bprime gen info categorization
    if bprimeGenInfo:
        event.getByLabel(BBtoWtWt_L, BBtoWtWt_H)
        event.getByLabel(BBtoWtZb_L, BBtoWtZb_H)
        event.getByLabel(BBtoZbZb_L, BBtoZbZb_H)
        event.getByLabel(BBtoZbHb_L, BBtoZbHb_H)
        event.getByLabel(BBtoWtHb_L, BBtoWtHb_H)
        event.getByLabel(BBtoHbHb_L, BBtoHbHb_H)
                     
        event.getByLabel(WPart1_L,   WPart1_H)
        event.getByLabel(WPart2_L,   WPart2_H)
        event.getByLabel(WPart3_L,   WPart3_H)
        event.getByLabel(WPart4_L,   WPart4_H)
        event.getByLabel(ZPart1_L,   ZPart1_H)
        event.getByLabel(ZPart2_L,   ZPart2_H)
        event.getByLabel(ZPart3_L,   ZPart3_H)
        event.getByLabel(ZPart4_L,   ZPart4_H)
        event.getByLabel(HPart1_L,   HPart1_H)
        event.getByLabel(HPart2_L,   HPart2_H)
        event.getByLabel(HPart3_L,   HPart3_H)
        event.getByLabel(HPart4_L,   HPart4_H)

        BBtoWtWt = BBtoWtWt_H.product()[0]
        BBtoWtZb = BBtoWtZb_H.product()[0]
        BBtoZbZb = BBtoZbZb_H.product()[0]
        BBtoZbHb = BBtoZbHb_H.product()[0]
        BBtoWtHb = BBtoWtHb_H.product()[0]
        BBtoHbHb = BBtoHbHb_H.product()[0]
        
        WPart1 = WPart1_H.product()
        WPart2 = WPart2_H.product()
        WPart3 = WPart3_H.product()
        WPart4 = WPart4_H.product()
        ZPart1 = ZPart1_H.product()
        ZPart2 = ZPart2_H.product()
        ZPart3 = ZPart3_H.product()
        ZPart4 = ZPart4_H.product()
        HPart1 = HPart1_H.product()
        HPart2 = HPart2_H.product()
        HPart3 = HPart3_H.product()
        HPart4 = HPart4_H.product()

        WPart1P4 = WPart1 + WPart2
        WPart2P4 = WPart3 + WPart4
        ZPart1P4 = ZPart1 + ZPart2
        ZPart2P4 = ZPart3 + ZPart4
        HPart1P4 = HPart1 + HPart2
        HPart2P4 = HPart3 + HPart4

        WtWt[0] = BBtoWtWt
        WtZb[0] = BBtoWtZb
        ZbZb[0] = BBtoZbZb
        ZbHb[0] = BBtoZbHb
        WtHb[0] = BBtoWtHb
        HbHb[0] = BBtoHbHb
        
        if BBtoWtWt == 1:iWtWt = iWtWt+1
        if BBtoWtZb == 1:iWtZb = iWtZb+1
        if BBtoZbZb == 1:iZbZb = iZbZb+1
        if BBtoZbHb == 1:iZbHb = iZbHb+1
        if BBtoWtHb == 1:iWtHb = iWtHb+1
        if BBtoHbHb == 1:iHbHb = iHbHb+1

        if "BprimeBprimeToBZTWinc" in fileN and BBtoWtWt == 0 and  BBtoWtZb == 0 and BBtoZbZb == 0:
            print('running over WtZb sample')
            print('impossible: the MC should be either WtWt or WtZb or ZbZb')
            print('which event', event.object().id().event())
        elif "BprimeBprimeToBHBZinc" in fileN and BBtoZbHb == 0 and  BBtoHbHb == 0 and BBtoZbZb == 0:
            print('running over ZbHb sample')
            print('impossible: the MC should be either ZbHb or HbHb or ZbZb')
            print('which event', event.object().id().event())
        elif "BprimeBprimeToBHTWinc" in fileN and BBtoWtHb == 0 and  BBtoHbHb == 0 and BBtoWtWt == 0:
            print('running over WtHb sample')
            print('impossible: the MC should be either WtHb or HbHb or WtWt')
            print('which event', event.object().id().event())    
            
    # PileupReweighting
    if not options.data :
        event.getByLabel(pileupWeightsLabel, pileupWeightsH)
        pileupProduct = pileupWeightsH.product()
	pileupWeight[0] = pileupProduct[0]
	pileupWeightUp[0] = pileupProduct[1]
        pileupWeightDown[0] = pileupProduct[2]     
    else:
        runNumber[0] = event.object().id().run()
        lumiNumber[0] = event.object().id().luminosityBlock() 
        eventNumber[0] = event.object().id().event()
        
  
    # Get the "product" of the handle (i.e. what it's "pointing to" in C++)
    if muonsH.isValid():
        muons = muonsH.product()
    if electronsH.isValid():
        electrons = electronsH.product()

    #Require exactly one lepton
    if  muonsH.isValid() and electronsH.isValid():
        if len(muons) == 0 and len(electrons) == 0:
            continue
    
    nMuons = 0
    if  muonsH.isValid():
        for imu in muons:
            if imu.pt() > lepPtMin:
                nMuons += 1    
           
    nElectrons = 0
    if electronsH.isValid():
        for iel in electrons:
            if iel.ecalDrivenMomentum().pt() > lepPtMin:
                nElectrons += 1
            
    # remove any remaining dilepton event...
    #if nElectrons+nMuons > 1 :
        #print('ele', nElectrons, 'mu', nMuons)
    #    continue        

    # to be sure of one lepton...
    if runMu==1 and nMuons!=1:
        continue
    if runMu==0 and nElectrons!=1 :
        continue
    
    # assigning one varaible to handle both lepton flavours
    if runMu:
        leptons = muons
    else:
        leptons = electrons

    # get other objects
    rho = (rhoH.product())[0]
    
    vertices = vertH.product()
    
    trigObj = trigH.product()
    
    jets_ca8 = c8aPruneJetsH.product()
    metObj_ca8 = (c8aPruneMetH.product())[0]
    
    jets = jetsH.product()
    metObj = (metH.product())[0]

    if len(jets) == 0:
        continue
    
    #Systematic variations studies:
    # ============================
    
    # get the P4 of the edm MET
    metP4 = metObj.p4()
    
    #L1, L2, L3 JEC are already applied to jets in EDM Ntuples   
    for ijet in jets :
    
        ## get the uncorrected jets 
        uncorrJet = ijet.correctedP4(0)
        
        ##genJets
        genJetPt  = ijet.userFloat('genJetPt')
        genJetPhi = ijet.userFloat('genJetPhi')
        genJetEta = ijet.userFloat('genJetEta')
        genJetMass= ijet.userFloat('genJetMass')
        
        ##Jet energy scale variation
        jetScale = 1.0
        if not options.data and abs(jecScale) > 0.0001 :
            jecUnc.setJetEta( ijet.eta() )
            jecUnc.setJetPt( ijet.pt() )
            upOrDown = bool(jecScale > 0.0)
            unc1 = abs(jecUnc.getUncertainty(upOrDown))
            unc2 = flatJecUnc
            unc = math.sqrt(unc1*unc1 + unc2*unc2)
            jetScale = 1 + unc * jecScale

        ##Jet energy resolution smearing
        if not options.data and genJetPt>15.0:     
            scale = smear_factor(ijet.eta(), options.jetPtSmear)
            recopt = ijet.pt()
            uncorrpt = ijet.correctedJet("Uncorrected").pt()
            genpt = genJetPt
            deltapt = (recopt-genpt)*scale
            ptScale = max(0.0, (recopt+deltapt)/recopt)
            jetScale*=ptScale

        ##Jet angular resolution smearing
        etaScale = 1.0
        phiScale = 1.0
        if not options.data and abs(options.jetEtaSmear)>0.0001 and genJetPt>15.0:
            scale = options.jetEtaSmear
            recoeta = ijet.eta()
            recophi = ijet.phi()
            geneta = genJetEta
            genphi = genJetPhi
            deltaeta = (recoeta-geneta)*scale
            deltaphi = (recophi-genphi)*scale
            etaScale = max(0.0, (recoeta+deltaeta)/recoeta)
            phiScale = max(0.0, (recophi+deltaphi)/recophi)
            
        #Reset the jet p4        
        ijet.polarP4().SetEta(ijet.eta() * etaScale)
        ijet.polarP4().SetPhi(ijet.phi() * phiScale)

        #print('ijet pt before ---->', ijet.p4().pt())
        ijet.setP4( ijet.p4() * jetScale )
        #print('ijet pt after ---->', ijet.p4().pt(), 'jetScale', jetScale)
        
        #remove the uncorrected jets
        metP4.SetPx(metP4.px() + uncorrJet.px())
        metP4.SetPy(metP4.py() + uncorrJet.py())

        #apply the SF and add back the jets and also correct the MET
        metP4.SetPx(metP4.px() - uncorrJet.px() * jetScale)
        metP4.SetPy(metP4.py() - uncorrJet.py() * jetScale)
        
    #Reset MET
    metObj.setP4(metP4)

    #########################
    if runMu:
        leptonsPt = leptons[0].pt()
        leptonsPx = leptons[0].px()
        leptonsPy = leptons[0].py()
        leptonsPz = leptons[0].pz()
        leptonsP  = leptons[0].p()
    else:
        leptonsPt = leptons[0].ecalDrivenMomentum().pt()
        leptonsPx = leptons[0].ecalDrivenMomentum().px()
        leptonsPy = leptons[0].ecalDrivenMomentum().py()
        leptonsPz = leptons[0].ecalDrivenMomentum().pz()
        leptonsP  = leptons[0].ecalDrivenMomentum().P()
        
    if leptonsPt <= lepPtMin : continue
    
    # store the trigger paths
    if runMu:
            trigSigMuNonIso_path[0] = -1
            trigSigMuIso_path[0] = -1
            trigSigMuIsoHad_path[0] = -1
            mu40_eta2p1 = "HLT_Mu40_eta2p1_v"
            mu24_Iso    = "HLT_IsoMu24_eta2p1_v"
            mu17_eta2p1_Had = "HLT_IsoMu17_eta2p1_TriCentral"
    else:        
        trigEleStop_path[0] = -1
        trigEleHad_path[0]  = -1
        trigSigEle_path[0]  = -1
        eleStop   = "HLT_Ele25_CaloIdVT_CaloIsoVL_TrkIdVL_TrkIsoT_TriCentralPFNoPUJet"
        eleHad    = "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentral"
        singleEle = "HLT_Ele27_WP80_v"

    trigPaths = trigObj.paths() #TriggerPathCollection
    for ipath in trigPaths:
        if runMu:   
            if mu40_eta2p1 in ipath.name():
                trigSigMuNonIso_path[0] =  trigObj.path(ipath.name()).wasAccept() and trigObj.path(ipath.name()).wasRun()
                #if trigSigMuNonIso_path[0]==1: print("your path ", ipath.name(), "was run and accepted")
            if mu24_Iso in ipath.name():
                trigSigMuIso_path[0] =  trigObj.path(ipath.name()).wasAccept() and trigObj.path(ipath.name()).wasRun()
                #if trigSigMuIso_path[0]==1: print("your path ", ipath.name(), "was run and accepted")
            if mu17_eta2p1_Had+"PFJet30_v" in ipath.name() or mu17_eta2p1_Had+"PFNoPUJet30_v" or mu17_eta2p1_Had+"PFNoPUJet30_30_20_v" or mu17_eta2p1_Had+"PFNoPUJet45_35_25_v":
                trigSigMuIsoHad_path[0] =  trigObj.path(ipath.name()).wasAccept() and trigObj.path(ipath.name()).wasRun()
                #if trigSigMuIso_path[0]==1: print("your path ", ipath.name(), "was run and accepted")    
        else:    
            if eleStop+"30_v" in ipath.name() or eleStop+"45_35_25_v" in ipath.name() or eleStop+"50_40_30_v" in ipath.name():
                trigEleStop_path[0] =  trigObj.path(ipath.name()).wasAccept() and trigObj.path(ipath.name()).wasRun()
                #if trigEleStop_path[0]==1: print("your path ", ipath.name(), "was run and accepted")
            if eleHad+"PFJet30_v" in ipath.name() or eleHad+"PFNoPUJet30_v" in ipath.name() or eleHad+"PFNoPUJet30_30_20_v" in ipath.name()or eleHad+"PFNoPUJet45_35_25_v" in ipath.name():
                trigEleHad_path[0] =  trigObj.path(ipath.name()).wasAccept() and trigObj.path(ipath.name()).wasRun()
                #if trigEleHad_path[0]==1: print("your path ", ipath.name(), "was run and accepted")
            if singleEle in ipath.name():
                trigSigEle_path[0] =  trigObj.path(ipath.name()).wasAccept() and trigObj.path(ipath.name()).wasRun()
                #if trigSigEle_path[0]==1: print("your path ", ipath.name(), "was run and accepted")
        
    nvertices[0] =  vertices.size()
    if vertices.size() > 0:
        PVz = vertices[0].z()
    else:
        print("no primary vertex found, settign PVz=0")
        PVz=0
    met[0] = metObj.pt()
    lepEt[0] = leptonsPt
    lepEta[0] = (leptons[0]).eta()
    lepd0[0] =  (leptons[0]).dB()
    
    if not runMu:
        eSCEta[0]  = (leptons[0]).superCluster().eta()
        eMVA[0]    = (leptons[0]).electronID("mvaTrigV0")
        eSihih[0]  = (leptons[0]).sigmaIetaIeta()
        eHOverE[0] = (leptons[0]).hadronicOverEm()
        eDphi[0]   = (leptons[0]).deltaEtaSuperClusterTrackAtVtx()
        eDeta[0]   = (leptons[0]).deltaPhiSuperClusterTrackAtVtx()
        
    chIso = (leptons[0]).userIsolation(pat.PfChargedHadronIso)
    nhIso = (leptons[0]).userIsolation(pat.PfNeutralHadronIso)
    phIso = (leptons[0]).userIsolation(pat.PfGammaIso)
    puIso = (leptons[0]).userIsolation(pat.PfPUChargedHadronIso) 
    
      
    if runMu :
        isMuTight[0] = isTightMu(leptons[0], PVz)
        lepIso[0] = (chIso + max(0.0, nhIso + phIso - 0.5*puIso))/leptonsPt
        if not options.data:
            lepSF[0]  = muonID_SF( (leptons[0]).eta())
            trigSF[0] = muonTrig_SF((leptons[0]).eta(), leptonsPt)
        else:    
            lepSF[0]  = 1
            trigSF[0] = 1
    else:
        AEff = (leptons[0]).userFloat('AEff')
        lepIso[0] = (chIso + max(0.0, nhIso + phIso - rho*AEff))/leptonsPt
        if not options.data :
            lepSF[0]  = electronID_SF((leptons[0]).eta(), leptonsPt)
            trigSF[0] = electronTrig_SF((leptons[0]).eta(), leptonsPt)
        else:
            lepSF[0]  = 1
            trigSF[0] = 1
            
    lepIsoUncorr[0] = (chIso + nhIso + phIso)/leptonsPt
    sumEt = leptonsPt + metObj.pt()
    
    lepton_vector = TLorentzVector()
    lepton_vector.SetPtEtaPhiM( leptonsPt, leptons[0].eta(), leptons[0].phi(), leptons[0].mass() )
    nu_p4 = metObj.p4()
    wPt = lepton_vector.Pt() + nu_p4.Pt()
    wPx = lepton_vector.Px() + nu_p4.Px()
    wPy = lepton_vector.Py() + nu_p4.Py()
    wMT = TMath.Sqrt(wPt*wPt-wPx*wPx-wPy*wPy)
    wMt[0] = wMT
    
    # sphericity and aplanarity from Andrew Ivanov
    # see: http://cepa.fnal.gov/psm/simulation/mcgen/lund/pythia_manual/pythia6.3/pythia6301/node213.html
    sum = leptonsP*leptonsP + metObj.p()*metObj.p()
    for jet in jets: sum+=jet.p()*jet.p()
    
    tensor = TMatrix(3,3)
    # mxx
    tensor[0][0] = leptonsPx*leptonsPx + metObj.px()*metObj.px()
    for jet in jets:
        if jet.pt() > jetPtMin: tensor[0][0]+=jet.px()*jet.px()
    tensor[0][0]/=sum
    # myy
    tensor[1][1] = leptonsPy*leptonsPy + metObj.py()*metObj.py()
    for jet in jets:
        if jet.pt() > jetPtMin: tensor[1][1]+=jet.py()*jet.py()
    tensor[1][1]/=sum
    # mzz
    tensor[2][2] = leptonsPz*leptonsPz + metObj.pz()*metObj.pz()
    for jet in jets:
        if jet.pt() > jetPtMin: tensor[2][2]+=jet.pz()*jet.pz()
    tensor[2][2]/=sum
    # mxy
    tensor[0][1] = leptonsPx*leptonsPy + metObj.px()*metObj.py()
    for jet in jets:
        if jet.pt() > jetPtMin: tensor[0][1]+=jet.px()*jet.py()
    tensor[0][1]/=sum
    tensor[1][0] = tensor[0][1]
    # mxz
    tensor[0][2] = leptonsPx*leptonsPz + metObj.px()*metObj.pz()
    for jet in jets:
        if jet.pt() > jetPtMin: tensor[0][2]+=jet.px()*jet.pz()
    tensor[0][2]/=sum
    tensor[2][0] = tensor[0][2]
    # myz
    tensor[1][2] = leptonsPy*leptonsPz + metObj.py()*metObj.pz()
    for jet in jets:
        if jet.pt() > jetPtMin: tensor[1][2]+=jet.py()*jet.pz()
    tensor[1][2]/=sum
    tensor[2][1] = tensor[1][2]

    eigenval = TVector(3)
    tensor.EigenVectors(eigenval)

    sphericity[0] = 3.0*(eigenval(1)+eigenval(2))/2.0
    aplanarity[0] = 3.0*eigenval(2)/2.0

    #print("eigen values: {0:4.2f}, {1:4.2f}, {2:4.2f}".format(eigenval(0),eigenval(1), eigenval(2)) )
    #print("sphericity {0:4.2f}, aplanarity = {1:4.2f}".format( sphericity, aplanarity))
    #print("mxx = {0:4.2f}, myy = {1:4.2f}, mzz = {2:4.2f}".format( tensor(0,0), tensor(1,1), tensor(2,2) ))
    #print("mxy = {0:4.2f}, mxz = {1:4.2f}, myz = {2:4.2f}".format( tensor(0,1), tensor(0,2), tensor(1,2) ))
    #print("myx = {0:4.2f}, mzx = {1:4.2f}, mzy = {2:4.2f}".format( tensor(1,0), tensor(2,0), tensor(2,1) ))
    
    nj = 0
    ntagsCSVM = 0
    sumJetPt = 0
    sumJetE = 0
    minDeltaR_lepjet = 5.0
    dR_Wjjqq = -1.0
    dR_Zjjqq = -1.0
    nVtags = 0
    WPt = 0
    ZPt = 0
    
    jet_p4 = []
    sum_jetP4 = TLorentzVector(0.0,0.0,0.0,0.0)
    nBtags = []
    for jetid, jet in enumerate(jets) :
        if jet.pt() <= jetPtMin: continue
        jetEt[nj] = jet.pt()
        sumJetPt += jet.pt()
        sumJetE += jet.energy()
        jet_vector = TLorentzVector()
        jet_vector.SetPtEtaPhiM( jet.pt(), jet.eta(), jet.phi(), jet.mass() )
        sum_jetP4 += jet_vector
        jet_p4.append(jet_vector)
        minDeltaR_lepjet = TMath.Min ( jet_vector.DeltaR(lepton_vector), minDeltaR_lepjet )
        bDistriminator[nj] = jet.bDiscriminator('combinedSecondaryVertexBJetTags')
        if isBTagged(jet):
            ntagsCSVM = ntagsCSVM + 1
            nBtags.append(jetid)       
        #print('btags',  ntagsCSVM)           
        nj = nj + 1
        sumEt += jet.pt()

        
    # mass of sum of all jets
    mj[0] = sum_jetP4.M()
    
    # count the jets that passes a certain jet pt threshold
    njets[0] = nj

    # m3
    M3 = 0.0
    highestPt = 0.0
    if nj >= 3:
        for j in range(0, nj-2):
            for k in range(j+1, nj-1):
                for l in range(k+1, nj):
                    threeJets = jet_p4[j] + jet_p4[k] + jet_p4[l]
                    if highestPt < threeJets.Perp():
                        M3 = threeJets.M()
                        highestPt=threeJets.Perp()
    m3[0] = M3

    # empty the list for the next event
    del jet_p4[:]
    
    cj = 0
    minDeltaR_lepca8jet = 5.0
    nBtags_remove = []

    #for i in range(max_nJets):
	#minDR_bV[i] = 0

    if len(jets_ca8) != 0:
        for ca8jet in jets_ca8:
        
            matched = false
            ca8jet_vector = TLorentzVector()
            ca8jet_vector.SetPtEtaPhiM( ca8jet.pt(), ca8jet.eta(), ca8jet.phi(), ca8jet.mass() )
            
            minDR_bjetV = 0.5
            for jetid, ak5jet in enumerate(jets) :
                if ak5jet.pt() <= jetPtMin: continue
                ak5jet_vector = TLorentzVector()
                ak5jet_vector.SetPtEtaPhiM( ak5jet.pt(), ak5jet.eta(), ak5jet.phi(), ak5jet.mass() )
                
                # min dR b/w ak5 jet and ca8 jet
                minDR_bjetV = TMath.Min ( ak5jet_vector.DeltaR(ca8jet_vector), minDR_bjetV )
                    
                if ak5jet_vector.DeltaR(ca8jet_vector) < 0.3:
                    matched = true 
                    # double tag
                    if isVTagged(ca8jet) and isBTagged(ak5jet):                        
                        nBtags_remove.append(jetid) 
                        
                       
            minDR_bV[cj] = minDR_bjetV
            #print("min DR_ak5_ca8", minDR_bV[cj])

            # require ca8 jet to match to at least one ak5 jet
            if not matched: continue
            
            # dR b/w lepton and CA8 jet:
            minDeltaR_lepca8jet = TMath.Min ( ca8jet_vector.DeltaR(lepton_vector), minDeltaR_lepca8jet )
            
            # V-tagging
            jetEt_ca8[cj] = ca8jet.pt()    
            WjetM[cj] = ca8jet.mass()
            subjet1M = ca8jet.daughter(0).mass() 
            subjet2M = ca8jet.daughter(1).mass()
            mu = max(subjet1M,subjet2M) / ca8jet.correctedJet("Uncorrected").mass()

            # widen to accomodate Higgs
            if (WjetM[cj] < 150 and WjetM[cj] > 50) and jetEt_ca8[cj] > 200:
                WjetMu[cj] = mu

            # nVtags
            if isVTagged(ca8jet):
                nVtags = nVtags + 1
    
            # gen parton related info:
            if bprimeGenInfo:               
                dR_Wqq_match1 = deltaR( ca8jet.eta(), ca8jet.phi(), WPart1P4.Eta(), WPart1P4.Phi())
                dR_Wqq_match2 = deltaR( ca8jet.eta(), ca8jet.phi(), WPart2P4.Eta(), WPart2P4.Phi())
                dR_Zqq_match1 = deltaR( ca8jet.eta(), ca8jet.phi(), ZPart1P4.Eta(), ZPart1P4.Phi())
                dR_Zqq_match2 = deltaR( ca8jet.eta(), ca8jet.phi(), ZPart2P4.Eta(), ZPart2P4.Phi())
                dR_Hqq_match1 = deltaR( ca8jet.eta(), ca8jet.phi(), HPart1P4.Eta(), HPart1P4.Phi())
                dR_Hqq_match2 = deltaR( ca8jet.eta(), ca8jet.phi(), HPart2P4.Eta(), HPart2P4.Phi())
                
                #if there are two W->qq, pick the one with min DeltaR, else pick the one which exists 
                if WPart1P4.Pt() != 0 and WPart2P4.Pt() != 0:
                    dR_Wjjqq = TMath.Min(dR_Wqq_match1,dR_Wqq_match2)
                    if dR_Wjjqq == dR_Wqq_match1: WPt = WPart1P4.Pt()
                    elif dR_Wjjqq == dR_Wqq_match2: WPt = WPart2P4.Pt()
                elif WPart1P4.Pt() != 0:
                    dR_Wjjqq = dR_Wqq_match1
                    WPt = WPart1P4.Pt()
                elif WPart2P4.Pt() != 0:
                    dR_Wjjqq = dR_Wqq_match2
                    WPt = WPart2P4.Pt()
                else:
                    dR_Wjjqq = -1
                    WPt = -1
                    
                dR_Wjjqq_match[cj] = dR_Wjjqq
                WPt_true[cj] = WPt

                #if there are two Z->qq, pick the one with min DeltaR, else pick the one which exists 
                if ZPart1P4.Pt() != 0 and ZPart2P4.Pt() != 0:
                    dR_Zjjqq = TMath.Min(dR_Zqq_match1,dR_Zqq_match2)
                    if dR_Zjjqq == dR_Zqq_match1: ZPt = ZPart1P4.Pt()
                    elif dR_Zjjqq == dR_Zqq_match2: ZPt = ZPart2P4.Pt()
                elif ZPart1P4.Pt() != 0:
                    dR_Zjjqq = dR_Zqq_match1
                    ZPt = ZPart1P4.Pt()
                elif ZPart2P4.Pt() != 0:
                    dR_Zjjqq = dR_Zqq_match2
                    ZPt = ZPart2P4.Pt()
                else:
                    dR_Zjjqq = -1
                    ZPt = -1
                    
                dR_Zjjqq_match[cj] = dR_Zjjqq
                ZPt_true[cj] = ZPt

                #if there are two H->qq, pick the one with min DeltaR, else pick the one which exists 
                if HPart1P4.Pt() != 0 and HPart2P4.Pt() != 0:
                    dR_Hjjqq = TMath.Min(dR_Hqq_match1,dR_Hqq_match2)
                    if dR_Hjjqq == dR_Hqq_match1: HPt = HPart1P4.Pt()
                    elif dR_Hjjqq == dR_Hqq_match2: HPt = HPart2P4.Pt()
                elif HPart1P4.Pt() != 0:
                    dR_Hjjqq = dR_Hqq_match1
                    HPt = HPart1P4.Pt()
                elif HPart2P4.Pt() != 0:
                    dR_Hjjqq = dR_Hqq_match2
                    HPt = HPart2P4.Pt()
                else:
                    dR_Hjjqq = -1
                    HPt = -1
                    
                dR_Hjjqq_match[cj] = dR_Hjjqq
                HPt_true[cj] = HPt
                
        cj = cj + 1

    
    #fill the rest of variables
    if sumJetE != 0:
        centrality[0] = sumJetPt/sumJetE    
    ht[0] = sumEt
    nTagsCSVMUncor[0] = len(nBtags)
    #print ("all b-tagged jets", len(nBtags), ":  to be removed", len(nBtags_remove))
    #print("nBtags: {0} nBtags_remove: {1}".format(nBtags, nBtags_remove))        
    nBtags = len([x for x in nBtags if x not in nBtags_remove])
    #print("nBTags", nBtags)
    nTagsCSVM[0] = nBtags
    nVTags[0] = nVtags    
    minDR_je[0] = minDeltaR_lepjet
    minDR_ca8je[0] = minDeltaR_lepca8jet
    met_vector = TLorentzVector()
    met_vector.SetPxPyPzE( metObj.px(), metObj.py(), metObj.pz(), metObj.et())
    deltaPhiMETe[0] = lepton_vector.DeltaPhi( met_vector )
    leadingJetVector = TLorentzVector()
    if leadingJetVector.Pt() > jetPtMin:
        leadingJetVector.SetPxPyPzE( jets[0].px(), jets[0].py(), jets[0].pz(), jets[0].energy())
        deltaPhiMETLeadingJet[0] = met_vector.DeltaPhi( leadingJetVector )
    
    t.Fill()
# Done processing the events!
# Stop our timer
timer.Stop()

print('BBtoWtWt', iWtWt)
print('BBtoWtZb', iWtZb)
print('BBtoZbZb', iZbZb)
print('BBtoZbHb', iZbHb)
print('BBtoWtHb', iWtHb)
print('BBtoHbHb', iHbHb)

# Print out our timing information
rtime = timer.RealTime(); # Real time (or "wall time")
ctime = timer.CpuTime(); # CPU time
print("Analyzed events: {0:6d}".format(nEventsAnalyzed))
print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds".format(rtime,ctime))
print("{0:4.2f} events / RealTime second .".format( nEventsAnalyzed/rtime))
print("{0:4.2f} events / CpuTime second .".format( nEventsAnalyzed/ctime))

# "cd" to our output file
f.cd()

# Write our tree
t.Write()

# Close it
f.Close()
