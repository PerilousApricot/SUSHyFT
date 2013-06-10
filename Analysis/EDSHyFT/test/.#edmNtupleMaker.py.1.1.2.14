import sys
sys.argv.append('-b')
import ROOT
sys.argv.remove('-b')

import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMNtuple")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
import sys
#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('ignoreDileptonVeto',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore dilepton veto in selection")

options.register ('runData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "if running over data (1) else (0)")
options.register('eleEt',
                  30.,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.float,
                 "electron et threshold")

options.register('runLoose',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Run extra sequence(1) for loose selction  or ignore them (0)")
                 
options.parseArguments()

print options

if options.runData == 1:
    runData = True
else: runData  = False

runNoEleID = options.runLoose

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )
if options.ignoreDileptonVeto:
    inputCutsToIgnore.append( 'Dilepton Veto' )
## Source
if not runData:
    process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
   '/store/user/meloam/ZJetToMuMu_Pt-80to120_TuneZ2star_8TeV_pythia6/None/20130206162922/00000/407A66CB-E175-E211-BCF0-003048F316E8.root') )                           
else:
    process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    '/store/user/meloam/SingleMu/meloam_feb12_tlbsm53x2_Run2012C_24Aug2012_v1/20130212222033/00000/4463A7D0-9075-E211-95CC-003048F2E8C2.root' ) )


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

if runData:
    process.GlobalTag.globaltag = 'GR_P_V40_AN1::All'
else:
    process.GlobalTag.globaltag = 'START53_V7E::All'

process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

# apply the JEC on fly
payloads = [
    'Jec12_V2_L1FastJet_AK5PFchs.txt',
    'Jec12_V2_L2Relative_AK5PFchs.txt', 
    'Jec12_V2_L3Absolute_AK5PFchs.txt',
    'Jec12_V2_L2L3Residual_AK5PFchs.txt',
    'Jec12_V2_Uncertainty_AK5PFchs.txt',   
]

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis
#_______________________________BTagging SF and Pileup________________________________________

if not runData:
    process.pileupReweightingProducer = cms.EDProducer("PileupReweightingPoducer",
                                         FirstTime = cms.untracked.bool(False),
                                         oneDReweighting = cms.untracked.bool(True),
                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                         PileupDataFile = cms.untracked.string('PUData_finebin_dist.root')
                                                       )

    # creates value maps to jets as userInt index:
    #-1 -- ignore, 1 -- right out of the box, 2 -- Nominal SF, 4 -- SF up, 8 -- SF down.
    process.goodPatJetsPFSF = cms.EDProducer("BTaggingSFProducer",
        JetSource = cms.InputTag('goodPatJetsPFlow'),
        DiscriminatorTag = cms.string('combinedSecondaryVertexBJetTags'),
        DiscriminatorValue = cms.double(0.679),
        EffMapFile = cms.string('Analysis/EDSHyFT/data/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph_CA8PrunedPF_CSVM_bTaggingEfficiencyMap.root')
    )

    process.GenInfo = cms.EDProducer('BoostedParticles')

#_____________________________________PF__________________________________________________


from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as shyftSelectionInput
if runData:
    goodAK5Patjet = 'goodPatJetsPFlow'
    goodCA8Patjet = 'goodPatJetsCA8PrunedPF'
else:
    goodAK5Patjet = 'goodPatJetsPFlow'
    goodCA8Patjet = 'goodPatJetsCA8PrunedPF'

process.pfTupleEle = cms.EDFilter('EDSHyFTSelector',
    shyftSelection = shyftSelectionInput.clone(
	muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
	electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    # TODO: which one?? allegedly patMETs was okay?
	metSrc = cms.InputTag('patMETs'),
    tauSrc = cms.InputTag('selectedPatTausPFlow'),
	jetSrc = cms.InputTag('goodPatJetsPFlow'),
	pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    tauTrig = cms.string('butz'),
	ePlusJets = cms.bool( True ),
	muPlusJets = cms.bool( False ),
	eEt = cms.double(options.eleEt),
	jetPtMin = cms.double(30.0),
    tauPtMin = cms.double(20.0),
    tauEtaMax = cms.double(2.4),
	minJets = cms.int32(1),
	useNoPFIso = cms.bool(True),
	useNoID  = cms.bool(True),
	useData = cms.bool(runData),
	identifier = cms.string('AK5 PF'),
	cutsToIgnore=cms.vstring(inputCutsToIgnore),
	jecPayloads = cms.vstring( payloads ),
    ),
    matchByHand = cms.bool(False)
)

## electron+jets decay mode
process.pfTupleEleCA8Pruned = process.pfTupleEle.clone()
process.pfTupleEleCA8Pruned.shyftSelection.jetSrc = cms.InputTag(goodCA8Patjet)
process.pfTupleEleCA8Pruned.shyftSelection.identifier = cms.string('CA8 Prunded PF')
process.pfTupleEleCA8Pruned.matchByHand = cms.bool(True)
process.pfTupleEleCA8Pruned.ePlusJets = cms.bool(True)
process.pfTupleEleCA8Pruned.muPlusJuets = cms.bool(False)

## muon+jets decay mode
process.pfTupleMuCA8Pruned = process.pfTupleEle.clone()
process.pfTupleMuCA8Pruned.shyftSelection.jetSrc = cms.InputTag(goodCA8Patjet)
process.pfTupleMuCA8Pruned.shyftSelection.identifier = cms.string('CA8 Prunded PF')
process.pfTupleMuCA8Pruned.matchByHand = cms.bool(True)
process.pfTupleMuCA8Pruned.ePlusJets = cms.bool( False )
process.pfTupleMuCA8Pruned.muPlusJets = cms.bool( True )

## electron+jets decay mode (selected pat)
process.pfTupleEleSelectedJets = process.pfTupleEle.clone()
process.pfTupleEleSelectedJets.shyftSelection.jetSrc = cms.InputTag(goodAK5Patjet)
process.pfTupleEleSelectedJets.shyftSelection.identifier = cms.string('Good PAT PF')
process.pfTupleEleSelectedJets.matchByHand = cms.bool(True)
process.pfTupleEleSelectedJets.ePlusJets = cms.bool(True)
process.pfTupleEleSelectedJets.muPlusJuets = cms.bool(False)

## muon+jets decay mode (selected pat)
process.pfTupleMuSelectedJets = process.pfTupleEle.clone()
process.pfTupleMuSelectedJets.shyftSelection.jetSrc = cms.InputTag(goodAK5Patjet)
process.pfTupleMuSelectedJets.shyftSelection.identifier = cms.string('Good PAT PF')
process.pfTupleMuSelectedJets.matchByHand = cms.bool(True)
process.pfTupleMuSelectedJets.ePlusJets = cms.bool( False )
process.pfTupleMuSelectedJets.muPlusJets = cms.bool( True )

if not runData:
    ## configure output module
    process.p0 = cms.Path( process.patTriggerDefaultSequence)
    process.p1 = cms.Path( process.pfTupleEleCA8Pruned)
    process.p2 = cms.Path( process.pfTupleMuCA8Pruned)
    process.p3 = cms.Path()
    # should I include the btag SF?
    process.p4 = cms.Path( process.pfTupleEleSelectedJets)
    process.p5 = cms.Path( process.pfTupleMuSelectedJets)
else:
    ## configure output module
    process.p0 = cms.Path( process.patTriggerDefaultSequence)
    process.p1 = cms.Path( process.pfTupleEleCA8Pruned)
    process.p2 = cms.Path( process.pfTupleMuCA8Pruned)
    process.p3 = cms.Path()
    # should I include the btag SF?
    process.p4 = cms.Path( process.pfTupleEleSelectedJets)
    process.p5 = cms.Path( process.pfTupleMuSelectedJets)



if not runData:
    process.p3 = cms.Path( process.pileupReweightingProducer * process.GenInfo )

process.out = cms.OutputModule("PoolOutputModule",
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring( 'p0', 'p1', 'p2', 'p3') ),
                               fileName =  cms.untracked.string('edmTest.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_pfTuple*_*_*',
                                                                      'keep *_patTriggerEvent_*_*',
                                                                      'keep *_patTrigger_*_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*',
                                                                      'keep *_caPrunedPFlow_SubJets_*'
                                                                      ),
                               )
if not runData:
    process.out.outputCommands += [
                               #'keep *_prunedGenParticles_*_*',
                               'keep *_GenInfo*_*_*',
                               'keep *_*_pileupWeights_*',
                               'keep PileupSummaryInfos_*_*_*',
                               ]

## output path
process.outpath = cms.EndPath(process.out)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

open('junk.py','w').write(process.dumpPython())
