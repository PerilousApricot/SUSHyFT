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

options.register('ignoreDilepton',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Ignore dilepton selection cut")

options.register ('runData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "if running over data (1) else (0)")

options.register('btagMap',
                 'BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "BTag Efficiency Map File")

options.register('useMuTrigs',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use muon triggers (1) or not (0)")
    
options.register('useEleTrigs',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use electron triggers (1) or not (0)")

options.register('runEleQCDSamples',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "To run on only electron QCD samples (1) or not (0)")

options.register('runMuonQCDSamples',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "To run on only muon QCD samples (1) or not (0)")
                                  
options.parseArguments()

print options

if options.runData == 1:
    runData = True
else: runData  = False

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if not runData:
    process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
   '/store/user/meloam/ZJetToMuMu_Pt-80to120_TuneZ2star_8TeV_pythia6/None/20130206162922/00000/407A66CB-E175-E211-BCF0-003048F316E8.root') )                           
else:
    process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    '/store/user/meloam/SingleMu/meloam_feb12_tlbsm53x2_Run2012C_24Aug2012_v1/20130212222033/00000/4463A7D0-9075-E211-95CC-003048F2E8C2.root' ) )
    #'/store/user/lpctlbsm/cjenkins/QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6/QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2/c04f3b4fa74c8266c913b71e0c74901d/tlbsm_53x_v2_mc_9_1_ysy.root',


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

# get the right GT for trigger and apply the JEC on fly
# note L1FastJet corrections are different for data and MC only, however both are kept for consistency
if runData:
    process.GlobalTag.globaltag = 'GR_P_V40_AN1::All'
    payloads = [
        'Jec12_V3_L1FastJet_AK5PFchs.txt',
        'Jec12_V3_L2Relative_AK5PFchs.txt',
        'Jec12_V3_L3Absolute_AK5PFchs.txt',
        'Jec12_V3_L2L3Residual_AK5PFchs.txt',
        'Jec12_V3_Uncertainty_AK5PFchs.txt',
        ]
else:
    process.GlobalTag.globaltag = 'START53_V7F::All'
    payloads = [
        'Jec12_V3_MC_L1FastJet_AK5PFchs.txt',
        'Jec12_V3_MC_L2Relative_AK5PFchs.txt',
        'Jec12_V3_MC_L3Absolute_AK5PFchs.txt',
        'Jec12_V3_MC_L2L3Residual_AK5PFchs.txt',
        'Jec12_V3_MC_Uncertainty_AK5PFchs.txt',
        ]	


process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

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
    print 'Analysis/EDSHyFT/data/'+options.btagMap+'_AK5PF_CSVM_bTaggingEfficiencyMap.root'
    
    process.goodPatJetsPFSF = cms.EDProducer("BTaggingSFProducer",
                                             JetSource = cms.InputTag('goodPatJetsPFlow'),
                                             DiscriminatorTag = cms.string('combinedSecondaryVertexBJetTags'),
                                             DiscriminatorValue = cms.double(0.679),
                                             EffMapFile = cms.string('Analysis/EDSHyFT/data/'+options.btagMap+'_AK5PF_CSVM_bTaggingEfficiencyMap.root')
                                             )

    process.GenInfo = cms.EDProducer('BoostedParticles')


#____________________________________Trigger Filter________________________________________
mutopTrig = 'HLT_IsoMu17_eta2p1_TriCentral'
estopTrig = 'HLT_Ele25_CaloIdVT_CaloIsoVL_TrkIdVL_TrkIsoT_TriCentral'
etopTrig  = 'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentral'

from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if options.useMuTrigs == 0 and options.useEleTrigs == 0 :
    process.hltSelectionMu = cms.Sequence()
    process.hltSelectionEle = cms.Sequence()
else :
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = [mutopTrig+'PFJet30_v*',
                                                                                                       mutopTrig+'PFNoPUJet30_v*',
                                                                                                       mutopTrig+'PFNoPUJet30_30_20_v*',
                                                                                                       mutopTrig+'PFNoPUJet45_35_25_v*',
                                                                                                       mutopTrig+'PFNoPUJet50_40_30_v*',
                                                                                                       'HLT_IsoMu24_eta2p1_v*',
                                                                                                       'HLT_Mu40_eta2p1_v*',
                                                                                                       ])
    process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  [etopTrig+'PFJet30_v*',
                                                                                                         etopTrig+'PFJet50_40_30_v*',
                                                                                                         etopTrig+'PFNoPUJet30_v*',
                                                                                                         etopTrig+'PFNoPUJet30_30_20_v*',
                                                                                                         etopTrig+'PFNoPUJet45_35_25_v*',
                                                                                                         etopTrig+'PFNoPUJet50_40_30_v*',
                                                                                                         estopTrig+'PFNoPUJet30_v*',
                                                                                                         estopTrig+'PFNoPUJet45_35_25_v*', 
                                                                                                         estopTrig+'PFNoPUJet50_40_30_v*',
                                                                                                         'HLT_Ele27_WP80_v*',   
                                                                                                         ])
    process.hltSelectionMu.throw = False
    process.hltSelectionEle.throw = False


    if options.useMuTrigs == 0 and options.useEleTrigs == 1 :
        process.hltSelectionMu =  cms.Sequence()
    elif options.useMuTrigs == 1 and options.useEleTrigs == 0 :
        process.hltSelectionEle =  cms.Sequence()


 
#_____________________________________PF__________________________________________________


from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as shyftSelectionInput

if runData:
    goodAK5Patjet = 'goodPatJetsPFlow'
    goodCA8Patjet = 'goodPatJetsCA8PrunedPF'
else:
    goodAK5Patjet = 'goodPatJetsPFSF'
    goodCA8Patjet = 'goodPatJetsCA8PrunedPF'
    
## electron+jets decay mode
## ========================
process.pfTupleEle = cms.EDFilter('EDSHyFTSelector',
                                  shyftSelection = shyftSelectionInput.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag(goodAK5Patjet),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    tauSrc = cms.InputTag('selectedPatTausPFlow'),
    ePlusJets = cms.bool( True ),
    muPlusJets = cms.bool( False ),
    eEt = cms.double( 25.0 ),
    tauEtaMax = cms.double(2.4),
    muPtMin = cms.double( 25.0 ),
    jetPtMin = cms.double(25.0),
    tauPtMin = cms.double(20.0),
    minJets = cms.int32(1),
    eRelIso = cms.double( 0.2 ), #loose iso
    muRelIso = cms.double( 0.2), #loose iso
    useNoPFIso = cms.bool(False),
    useNoID  = cms.bool(False), # use eMVA > 0.5
    useData = cms.bool(runData),
    identifier = cms.string('AK5 PF'),
    cutsToIgnore=cms.vstring(inputCutsToIgnore),
    jecPayloads = cms.vstring( payloads ),
    ),
                                  matchByHand = cms.bool(False),
                                  useData = cms.bool(runData)                              
                                  )

## e+jets with loose collections
process.pfTupleEleLoose = process.pfTupleEle.clone()
process.pfTupleEleLoose.shyftSelection.muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose')
process.pfTupleEleLoose.shyftSelection.electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose')
process.pfTupleEleLoose.shyftSelection.useNoPFIso = cms.bool(True)
process.pfTupleEleLoose.shyftSelection.eRelIso = cms.double( 10.0)
process.pfTupleEleLoose.shyftSelection.useNoID  = cms.bool(True)
process.pfTupleEleLoose.shyftSelection.identifier = cms.string('AK5 PF Loose electrons')

## e+jets with ca8jets
process.pfTupleEleCA8Pruned = process.pfTupleEle.clone()
process.pfTupleEleCA8Pruned.shyftSelection.jetSrc = cms.InputTag(goodCA8Patjet)
process.pfTupleEleCA8Pruned.shyftSelection.identifier = cms.string('CA8 Prunded PF')
process.pfTupleEleCA8Pruned.matchByHand = cms.bool(True)

## e+jets MET unclus systematics
process.pfTupleEleMetRes090 =  process.pfTupleEle.clone()
process.pfTupleEleMetRes090.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleEleMetRes090.shyftSelection.unclMetScale = cms.double( 0.90 )
process.pfTupleEleMetRes090.shyftSelection.identifier = cms.string('PFMETRES090')

process.pfTupleEleMetRes110 =  process.pfTupleEle.clone()
process.pfTupleEleMetRes110.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleEleMetRes110.shyftSelection.unclMetScale = cms.double( 1.10 )
process.pfTupleEleMetRes110.shyftSelection.identifier = cms.string('PFMETRES110')

## mu+jets decay mode
## =================
process.pfTupleMu = process.pfTupleEle.clone()
process.pfTupleMu.shyftSelection.ePlusJets = cms.bool(False)
process.pfTupleMu.shyftSelection.muPlusJets = cms.bool(True)

## mu+jets with loose collections
process.pfTupleMuLoose = process.pfTupleMu.clone()
process.pfTupleMuLoose.shyftSelection.muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose')
process.pfTupleMuLoose.shyftSelection.electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose')
process.pfTupleMuLoose.shyftSelection.useNoPFIso = cms.bool(True)
process.pfTupleMuLoose.shyftSelection.eRelIso = cms.double( 10.0)
process.pfTupleMuLoose.shyftSelection.identifier = cms.string('AK5 PF Loose muons')

## mu+jets with ca8jets
process.pfTupleMuCA8Pruned = process.pfTupleMu.clone()
process.pfTupleMuCA8Pruned.shyftSelection.jetSrc = cms.InputTag(goodCA8Patjet)
process.pfTupleMuCA8Pruned.shyftSelection.identifier = cms.string('CA8 Prunded PF')
process.pfTupleMuCA8Pruned.matchByHand = cms.bool(True)

## mu+jets MET unclus systematics
process.pfTupleMuMetRes090 =  process.pfTupleMu.clone()
process.pfTupleMuMetRes090.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleMuMetRes090.shyftSelection.unclMetScale = cms.double( 0.90 )
process.pfTupleMuMetRes090.shyftSelection.identifier = cms.string('PFMETRES090')

process.pfTupleMuMetRes110 =  process.pfTupleMu.clone()
process.pfTupleMuMetRes110.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleMuMetRes110.shyftSelection.unclMetScale = cms.double( 1.10 )
process.pfTupleMuMetRes110.shyftSelection.identifier = cms.string('PFMETRES110')

## configure output module
process.p0 = cms.Path( process.patTriggerDefaultSequence )

if runData:
    process.p1 = cms.Path( process.hltSelectionEle * process.pfTupleEle)
    process.p2 = cms.Path( process.hltSelectionMu * process.pfTupleMu)
    process.p3 = cms.Path( process.hltSelectionEle * process.pfTupleEleCA8Pruned)
    process.p4 = cms.Path( process.hltSelectionMu * process.pfTupleMuCA8Pruned)
    process.p5 = cms.Path( process.hltSelectionEle * process.pfTupleEleLoose)
    process.p6 = cms.Path( process.hltSelectionMu * process.pfTupleMuLoose)
    process.p7 = cms.Path()
    process.p8 = cms.Path()
    process.p9 = cms.Path()
    process.p10 = cms.Path()
    process.p11 = cms.Path()
elif options.runEleQCDSamples:
    process.p1 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEle)
    process.p2 = cms.Path()
    process.p3 = cms.Path( process.pfTupleEleCA8Pruned)
    process.p4 = cms.Path()
    process.p5 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEleLoose)
    process.p6 = cms.Path()
    process.p7 = cms.Path( process.pileupReweightingProducer * process.GenInfo )
    process.p8 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEleMetRes090)
    process.p9 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEleMetRes110)
    process.p10 = cms.Path()
    process.p11 = cms.Path()
elif options.runMuonQCDSamples:
    process.p1 = cms.Path()
    process.p2 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMu)
    process.p3 = cms.Path()
    process.p4 = cms.Path( process.pfTupleMuCA8Pruned)
    process.p5 = cms.Path()
    process.p6 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMuLoose)
    process.p7 = cms.Path( process.pileupReweightingProducer * process.GenInfo )
    process.p8 = cms.Path()
    process.p9 = cms.Path()
    process.p10 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMuMetRes090)
    process.p11 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMuMetRes110)  
else:
    process.p1 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEle)
    process.p2 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMu)
    process.p3 = cms.Path( process.pfTupleEleCA8Pruned)
    process.p4 = cms.Path( process.pfTupleMuCA8Pruned)
    process.p5 = cms.Path()
    process.p6 = cms.Path()
    process.p7 = cms.Path( process.pileupReweightingProducer * process.GenInfo )
    process.p8 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEleMetRes090)
    process.p9 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEleMetRes110)
    process.p10 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMuMetRes090)
    process.p11 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMuMetRes110)
    
process.out = cms.OutputModule("PoolOutputModule",
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring( 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7' ,'p8', 'p9', 'p10', 'p11') ),
                               fileName =  cms.untracked.string('edmTest.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_pfTuple*_*_*',
                                                                      'drop *_pfTuple*CA8Pruned_*_*',
                                                                      'keep *_pileup*_*_*',
                                                                      'keep *_pfTuple*CA8Pruned_jets_*',
                                                                      'keep *_pfTuple*CA8Pruned_MET_*',
                                                                      'keep *_patTriggerEvent_*_*',
                                                                      'keep patTriggerPaths_patTrigger_*_*',
                                                                      'keep *_patTrigger_*_*',
                                                                      'keep *_kt6PFJetsForIsolation_rho_*',
                                                                      'keep *_kt6PFJets_rho_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*',
                                                                      'keep *_caPrunedPFlow_SubJets_*'
                                                                      ),
                               )
if not runData:
    process.out.outputCommands += [
                                #'drop *_pfTuple*Loose_*_*',
                                'drop *_pfTuple*MetRes*_*_*',
                                'keep *_pfTuple*MetRes*_MET_*',
                                'keep *_GenInfo*_*_*',
                                'keep *_*_pileupWeights_*',
                                'keep PileupSummaryInfos_*_*_*',
                                ]
 
## output path
process.outpath = cms.EndPath(process.out)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

open('junk.py','w').write(process.dumpPython())
