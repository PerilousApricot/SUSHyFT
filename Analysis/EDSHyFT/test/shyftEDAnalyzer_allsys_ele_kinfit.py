import FWCore.ParameterSet.Config as cms
#from PhysicsTools.PatAlgos.patTemplate_cfg import *
#from PhysicsTools.PatAlgos.tools.coreTools import *

process = cms.Process("KinFit")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

## options.register ('useFlavorHistory',
##                   0,
##                   VarParsing.multiplicity.singleton,
##                   VarParsing.varType.int,
##                   "Flavor History Mode")

options.register('sampleNameInput',
                 'Wjets',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

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

import sys

inputDoMC=True
inputSampleName = options.sampleNameInput
runQCDSamples = options.runLoose

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/lpctlbsm/skhalil/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_9_1_qHp.root',
        )
                                )                           
payloads = [
    'Jec12_V1_L1FastJet_AK5PFchs.txt',
    'Jec12_V1_L2Relative_AK5PFchs.txt',
    'Jec12_V1_L3Absolute_AK5PFchs.txt',
    'Jec12_V1_L2L3Residual_AK5PFchs.txt',
    'Jec12_V1_Uncertainty_AK5PFchs.txt',    
]
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

#_____________________________________PF__________________________________________________


process.pfShyftSkim = cms.EDFilter('EDWPlusJetsSelector',
                                   inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    ePlusJets = cms.bool( True ),
    muPlusJets = cms.bool(False),
    usePFIso = cms.bool(True),
    eEtCut = cms.double(options.eleEt),
    useVBTFDetIso  = cms.bool(False),
    jetPtMin = cms.double(35.0),##
    minJets = cms.int32(4),
    metMin = cms.double(0.0), 
    doMC = cms.bool( inputDoMC),
    sampleName = cms.string(inputSampleName),
    jetAlgo = cms.string("pf"),
    jetSmear = cms.double(0.1),
    jecPayloads = cms.vstring( payloads ),
    cutsToIgnore=cms.vstring(inputCutsToIgnore),
    identifier = cms.string('PF'),
    jecPayloads = cms.vstring( payloads )
    )
                                       )

process.pfShyftSkimLoose = process.pfShyftSkim.clone()
process.pfShyftSkimLoose.useWP95Selection = cms.bool(True)
process.pfShyftSkimLoose.useWP70Selection = cms.bool(False)
process.pfShyftSkimLoose.identifier = cms.string('PF, relIso<0.2, WP95')
                                     

############################
## adding KinFitter stuff
############################

from TopQuarkAnalysis.TopObjectResolutions.stringResolutions_etEtaPhi_cff import *

# original version /TopQuarkAnalysis/TopKinFitter/python/TtSemiLepKinFitProducer_Electrons_cfi.py
# using TCHEM b-tagger
process.kinFitTtSemiLepEventTCHEM = cms.EDProducer("TtSemiLepKinFitProducerElectron",
    jets = cms.InputTag("pfShyftSkim:jets"),
    leps = cms.InputTag("pfShyftSkim:electrons"),
    mets = cms.InputTag("pfShyftSkim:met"),

    # ------------------------------------------------
    # maximum number of jets to be considered in the
    # jet combinatorics (has to be >= 4, can be set to
    # -1 if you want to take all)
    # ------------------------------------------------
    maxNJets = cms.int32(5),

    #-------------------------------------------------
    # maximum number of jet combinations finally
    # written into the event, starting from the "best"
    # (has to be >= 1, can be set to -1 if you want to 
    # take all)
    #-------------------------------------------------
    maxNComb = cms.int32(2),

    # ------------------------------------------------
    # option to take only a given jet combination
    # instead of going through the full combinatorics
    # ------------------------------------------------
    match = cms.InputTag(""),
    useOnlyMatch = cms.bool(False),

    # ------------------------------------------------
    # option to use b-tagging
    # ------------------------------------------------
    bTagAlgo          = cms.string("trackCountingHighEffBJetTags"),
    minBDiscBJets     = cms.double(3.3),
    maxBDiscLightJets = cms.double(3.3),
    useBTagging       = cms.bool(True),

    # ------------------------------------------------
    # settings for the KinFitter
    # ------------------------------------------------    
    maxNrIter = cms.uint32(500),
    maxDeltaS = cms.double(5e-05),
    maxF      = cms.double(0.0001),
    # ------------------------------------------------
    # select parametrisation
    # 0: EMom, 1: EtEtaPhi, 2: EtThetaPhi
    # ------------------------------------------------
    jetParametrisation = cms.uint32(1),
    lepParametrisation = cms.uint32(1),
    metParametrisation = cms.uint32(1),

    jetEnergyResolutionSmearFactor = cms.double(1.0),
    # ------------------------------------------------
    # set constraints
    # 1: Whad-mass, 2: Wlep-mass, 3: thad-mass,
    # 4: tlep-mass, 5: nu-mass, 6: equal t-masses,
    # by default: Px conservation and Py conservation
    # ------------------------------------------------                                   
    constraints = cms.vuint32(1, 2, 6),

    # ------------------------------------------------
    # set mass values used in the constraints
    # ------------------------------------------------    
    mW   = cms.double(80.4),
    mTop = cms.double(173.),
                                              
    # using new object resolutions
    udscResolutions             = udscResolutionPF.functions,
    bResolutions                = bjetResolutionPF.functions,
    lepResolutions              = elecResolution.functions,
    metResolutions              = metResolutionPF.functions,
                                              )

process.tprimeNtupleDumperTCHEM = cms.EDProducer("TprimeNtupleDumper",
    do_MC = cms.bool(False),
    resonanceId = cms.int32(6),                                             
    kinFitterLabel = cms.string("kinFitTtSemiLepEventTCHEM"),
    selectorLabel  = cms.string("pfShyftSkim"),
                                            )
# add pure min Chi2 and TCHE b-taggers for comparison
process.kinFitTtSemiLepEventCHI2 = process.kinFitTtSemiLepEventTCHEM.clone()
process.kinFitTtSemiLepEventCHI2.useBTagging = False

process.tprimeNtupleDumperCHI2 = process.tprimeNtupleDumperTCHEM.clone()
process.tprimeNtupleDumperCHI2.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2")

## process.kinFitTtSemiLepEventSSVHEM = process.kinFitTtSemiLepEventTCHEM.clone()
## process.kinFitTtSemiLepEventSSVHEM.useBTagging = True
## process.kinFitTtSemiLepEventSSVHEM.bTagAlgo = "simpleSecondaryVertexHighEffBJetTags"
## process.kinFitTtSemiLepEventSSVHEM.minBDiscBJets = 1.74
## process.kinFitTtSemiLepEventSSVHEM.maxBDiscLightJets = 1.74

## process.tprimeNtupleDumperSSVHEM = process.tprimeNtupleDumperTCHEM.clone()
## process.tprimeNtupleDumperSSVHEM.kinFitterLabel = cms.string("kinFitTtSemiLepEventSSVHEM")

process.kinFitTtSemiLepEventCSVM = process.kinFitTtSemiLepEventTCHEM.clone()
process.kinFitTtSemiLepEventCSVM.useBTagging = True
process.kinFitTtSemiLepEventCSVM.bTagAlgo = "combinedSecondaryVertexBJetTags"
process.kinFitTtSemiLepEventCSVM.minBDiscBJets =  0.679
process.kinFitTtSemiLepEventCSVM.maxBDiscLightJets =  0.679

process.tprimeNtupleDumperCSVM = process.tprimeNtupleDumperTCHEM.clone()
process.tprimeNtupleDumperCSVM.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVM")

# and for systematic samples too     process.kinFitTtSemiLepEvent.clone()
# minimum Chi2
process.kinFitTtSemiLepEventCHI2JES095 = process.kinFitTtSemiLepEventCHI2.clone()
process.kinFitTtSemiLepEventCHI2JES095.jets = cms.InputTag("pfShyftSkimJES095:jets")
process.kinFitTtSemiLepEventCHI2JES095.leps = cms.InputTag("pfShyftSkimJES095:electrons")
process.kinFitTtSemiLepEventCHI2JES095.mets = cms.InputTag("pfShyftSkimJES095:met")

process.tprimeNtupleDumperCHI2JES095 = process.tprimeNtupleDumperCHI2.clone()
process.tprimeNtupleDumperCHI2JES095.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2JES095")
process.tprimeNtupleDumperCHI2JES095.selectorLabel  = cms.string("pfShyftSkimJES095")

process.kinFitTtSemiLepEventCHI2JES105 = process.kinFitTtSemiLepEventCHI2.clone()
process.kinFitTtSemiLepEventCHI2JES105.jets = cms.InputTag("pfShyftSkimJES105:jets")
process.kinFitTtSemiLepEventCHI2JES105.leps = cms.InputTag("pfShyftSkimJES105:electrons")
process.kinFitTtSemiLepEventCHI2JES105.mets = cms.InputTag("pfShyftSkimJES105:met")

process.tprimeNtupleDumperCHI2JES105 = process.tprimeNtupleDumperCHI2.clone()
process.tprimeNtupleDumperCHI2JES105.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2JES105")
process.tprimeNtupleDumperCHI2JES105.selectorLabel  = cms.string("pfShyftSkimJES105")

process.kinFitTtSemiLepEventCHI2Loose = process.kinFitTtSemiLepEventCHI2.clone()
process.kinFitTtSemiLepEventCHI2Loose.jets = cms.InputTag("pfShyftSkimLoose:jets")
process.kinFitTtSemiLepEventCHI2Loose.leps = cms.InputTag("pfShyftSkimLoose:electrons")
process.kinFitTtSemiLepEventCHI2Loose.mets = cms.InputTag("pfShyftSkimLoose:met")

process.tprimeNtupleDumperCHI2Loose = process.tprimeNtupleDumperCHI2.clone()
process.tprimeNtupleDumperCHI2Loose.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2Loose")
process.tprimeNtupleDumperCHI2Loose.selectorLabel  = cms.string("pfShyftSkimLoose")

# TCHEM b-tagging
process.kinFitTtSemiLepEventTCHEMJES095 = process.kinFitTtSemiLepEventTCHEM.clone()
process.kinFitTtSemiLepEventTCHEMJES095.jets = cms.InputTag("pfShyftSkimJES095:jets")
process.kinFitTtSemiLepEventTCHEMJES095.leps = cms.InputTag("pfShyftSkimJES095:electrons")
process.kinFitTtSemiLepEventTCHEMJES095.mets = cms.InputTag("pfShyftSkimJES095:met")

process.tprimeNtupleDumperTCHEMJES095 = process.tprimeNtupleDumperTCHEM.clone()
process.tprimeNtupleDumperTCHEMJES095.kinFitterLabel = cms.string("kinFitTtSemiLepEventTCHEMJES095")
process.tprimeNtupleDumperTCHEMJES095.selectorLabel  = cms.string("pfShyftSkimJES095")

process.kinFitTtSemiLepEventTCHEMJES105 = process.kinFitTtSemiLepEventTCHEM.clone()
process.kinFitTtSemiLepEventTCHEMJES105.jets = cms.InputTag("pfShyftSkimJES105:jets")
process.kinFitTtSemiLepEventTCHEMJES105.leps = cms.InputTag("pfShyftSkimJES105:electrons")
process.kinFitTtSemiLepEventTCHEMJES105.mets = cms.InputTag("pfShyftSkimJES105:met")

process.tprimeNtupleDumperTCHEMJES105 = process.tprimeNtupleDumperTCHEM.clone()
process.tprimeNtupleDumperTCHEMJES105.kinFitterLabel = cms.string("kinFitTtSemiLepEventTCHEMJES105")
process.tprimeNtupleDumperTCHEMJES105.selectorLabel  = cms.string("pfShyftSkimJES105")

process.kinFitTtSemiLepEventTCHEMLoose = process.kinFitTtSemiLepEventTCHEM.clone()
process.kinFitTtSemiLepEventTCHEMLoose.jets = cms.InputTag("pfShyftSkimLoose:jets")
process.kinFitTtSemiLepEventTCHEMLoose.leps = cms.InputTag("pfShyftSkimLoose:electrons")
process.kinFitTtSemiLepEventTCHEMLoose.mets = cms.InputTag("pfShyftSkimLoose:met")

process.tprimeNtupleDumperTCHEMLoose = process.tprimeNtupleDumperTCHEM.clone()
process.tprimeNtupleDumperTCHEMLoose.kinFitterLabel = cms.string("kinFitTtSemiLepEventTCHEMLoose")
process.tprimeNtupleDumperTCHEMLoose.selectorLabel  = cms.string("pfShyftSkimLoose")

## # SSVHEM b-tagging
## process.kinFitTtSemiLepEventSSVHEMJES095 = process.kinFitTtSemiLepEventSSVHEM.clone()
## process.kinFitTtSemiLepEventSSVHEMJES095.jets = cms.InputTag("pfShyftSkimJES095:jets")
## process.kinFitTtSemiLepEventSSVHEMJES095.leps = cms.InputTag("pfShyftSkimJES095:electrons")
## process.kinFitTtSemiLepEventSSVHEMJES095.mets = cms.InputTag("pfShyftSkimJES095:met")

## process.tprimeNtupleDumperSSVHEMJES095 = process.tprimeNtupleDumperSSVHEM.clone()
## process.tprimeNtupleDumperSSVHEMJES095.kinFitterLabel = cms.string("kinFitTtSemiLepEventSSVHEMJES095")
## process.tprimeNtupleDumperSSVHEMJES095.selectorLabel  = cms.string("pfShyftSkimJES095")

## process.kinFitTtSemiLepEventSSVHEMJES105 = process.kinFitTtSemiLepEventSSVHEM.clone()
## process.kinFitTtSemiLepEventSSVHEMJES105.jets = cms.InputTag("pfShyftSkimJES105:jets")
## process.kinFitTtSemiLepEventSSVHEMJES105.leps = cms.InputTag("pfShyftSkimJES105:electrons")
## process.kinFitTtSemiLepEventSSVHEMJES105.mets = cms.InputTag("pfShyftSkimJES105:met")

## process.tprimeNtupleDumperSSVHEMJES105 = process.tprimeNtupleDumperSSVHEM.clone()
## process.tprimeNtupleDumperSSVHEMJES105.kinFitterLabel = cms.string("kinFitTtSemiLepEventSSVHEMJES105")
## process.tprimeNtupleDumperSSVHEMJES105.selectorLabel  = cms.string("pfShyftSkimJES105")

# CSVM b-tagging
process.kinFitTtSemiLepEventCSVMJES095 = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMJES095.jets = cms.InputTag("pfShyftSkimJES095:jets")
process.kinFitTtSemiLepEventCSVMJES095.leps = cms.InputTag("pfShyftSkimJES095:electrons")
process.kinFitTtSemiLepEventCSVMJES095.mets = cms.InputTag("pfShyftSkimJES095:met")

process.tprimeNtupleDumperCSVMJES095 = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMJES095.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMJES095")
process.tprimeNtupleDumperCSVMJES095.selectorLabel  = cms.string("pfShyftSkimJES095")

process.kinFitTtSemiLepEventCSVMJES105 = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMJES105.jets = cms.InputTag("pfShyftSkimJES105:jets")
process.kinFitTtSemiLepEventCSVMJES105.leps = cms.InputTag("pfShyftSkimJES105:electrons")
process.kinFitTtSemiLepEventCSVMJES105.mets = cms.InputTag("pfShyftSkimJES105:met")

process.tprimeNtupleDumperCSVMJES105 = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMJES105.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMJES105")
process.tprimeNtupleDumperCSVMJES105.selectorLabel  = cms.string("pfShyftSkimJES105")

process.kinFitTtSemiLepEventCSVMLoose = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMLoose.jets = cms.InputTag("pfShyftSkimLoose:jets")
process.kinFitTtSemiLepEventCSVMLoose.leps = cms.InputTag("pfShyftSkimLoose:electrons")
process.kinFitTtSemiLepEventCSVMLoose.mets = cms.InputTag("pfShyftSkimLoose:met")

process.tprimeNtupleDumperCSVMLoose = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMLoose.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMLoose")
process.tprimeNtupleDumperCSVMLoose.selectorLabel  = cms.string("pfShyftSkimLoose")

################################################
#_______________Systematics__________________
#################################################

#____________________JES up and down _______________________

process.pfShyftSkimJES095 = process.pfShyftSkim.clone()
process.pfShyftSkimJES095.jetScale = cms.double(-1.0)
process.pfShyftSkimJES095.jetUncertainty = cms.double(0.0)
process.pfShyftSkimJES095.identifier = cms.string('PFJES095')

process.pfShyftSkimJES105 = process.pfShyftSkim.clone()
process.pfShyftSkimJES105.jetScale = cms.double(1.0)
process.pfShyftSkimJES105.jetUncertainty = cms.double(0.0)
process.pfShyftSkimJES105.identifier = cms.string('PFJES105')


process.p1 = cms.Path( process.pfShyftSkim * (process.kinFitTtSemiLepEventCHI2 * process.tprimeNtupleDumperCHI2 +
                                              process.kinFitTtSemiLepEventTCHEM * process.tprimeNtupleDumperTCHEM +
                                              process.kinFitTtSemiLepEventCSVM * process.tprimeNtupleDumperCSVM                                             
                                              )
                       )
process.p2 = cms.Path( process.pfShyftSkimJES095 * (process.kinFitTtSemiLepEventCHI2JES095 * process.tprimeNtupleDumperCHI2JES095 +
                                                    process.kinFitTtSemiLepEventTCHEMJES095 * process.tprimeNtupleDumperTCHEMJES095 +
                                                    process.kinFitTtSemiLepEventCSVMJES095 * process.tprimeNtupleDumperCSVMJES095
                                                    )
                       )
process.p3 = cms.Path( process.pfShyftSkimJES105 * (process.kinFitTtSemiLepEventCHI2JES105 * process.tprimeNtupleDumperCHI2JES105 +
                                                    process.kinFitTtSemiLepEventTCHEMJES105 * process.tprimeNtupleDumperTCHEMJES105 +
                                                    process.kinFitTtSemiLepEventCSVMJES105 * process.tprimeNtupleDumperCSVMJES105
                                                    )
                       )
    
#configure output module
if runQCDSamples:
    process.p4 = cms.Path( process.pfShyftSkimLoose * (process.kinFitTtSemiLepEventCHI2Loose * process.tprimeNtupleDumperCHI2Loose +
                                                       process.kinFitTtSemiLepEventTCHEMLoose * process.tprimeNtupleDumperTCHEMLoose +
                                                       process.kinFitTtSemiLepEventCSVMLoose * process.tprimeNtupleDumperCSVMLoose
                                                       )
                           )
    process.out = cms.OutputModule("PoolOutputModule",
                                   SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p1','p2','p3', 'p4') ),
                                   )
    
else:
    process.out = cms.OutputModule("PoolOutputModule",
                                   SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p1','p2','p3') ),
                                   )


process.out.fileName =  cms.untracked.string('ttTest.root')
process.out.outputCommands = cms.untracked.vstring('drop *')


process.out.outputCommands += ['keep *_kinFitTtSemiLepEvent*_*_*',
                               'keep *_pfShyftSkim*_*_*',
                               'keep *_tprimeNtupleDumper*_*_*',
                               'keep PileupSummaryInfos_*_*_*',
                               'keep *_goodOfflinePrimaryVertices_*_*',
                               'keep *_prunedGenParticles_*_*'
                               ]

if runQCDSamples:
    process.out.outputCommands.append( 'keep *_pfShyftLooseSkim*_*_*' )

#process.out.dropMetaData = cms.untracked.string("DROPPED")

## output path
process.outpath = cms.EndPath(process.out)

## process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
## process.MessageLogger.suppressWarning.append('patTrigger')
## process.MessageLogger.cerr.FwkJob.limit=1
## process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

open('junk.py','w').write(process.dumpPython())
