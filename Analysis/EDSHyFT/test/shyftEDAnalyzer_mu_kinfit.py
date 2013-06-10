import FWCore.ParameterSet.Config as cms

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

options.register ('doMC',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use MC truth")

options.register ('sampleNameInput',
                  'top',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Sample name to give histograms")

options.register ('outputRootFile',
                  'shyftStudies.root',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Output root file name")

options.register('ignoreTrigger',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('triggerName',
                 'HLT_Mu30_v1',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Electron trigger to run")

options.register('runLoose',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Run extra sequence(1) for loose selction or ignore them (0)")

options.parseArguments()

print options

import sys

if options.doMC > 0 :
    inputDoMC = True
else :
    inputDoMC = False
   
inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/lpctlbsm/vasquez/SingleMu/ttbsm_v9_Run2011A-PromptReco-v4/f8e845a0332c56398831da6c30999af1/ttbsm_42x_data_326_1_ZF4.root'
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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V12::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')


from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis


process.pfShyftSkim =  cms.EDFilter('EDWPlusJetsSelector',
                                    inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    ePlusJets = cms.bool( False ),
    muPlusJets = cms.bool( True ),
    muTrig = cms.string(options.triggerName),
    jetPtMin = cms.double(35.0),##
    minJets = cms.int32(4),##
    metMin = cms.double(0.0),
    muPtMin = cms.double(35.0),
    identifier = cms.string('PFMu'),
    cutsToIgnore=cms.vstring( inputCutsToIgnore ),
    reweightPU = cms.bool(False),
    useData = cms.bool( not inputDoMC ),
    doMC = cms.bool( inputDoMC),
    jetSmear = cms.double(0.0),
    jecPayloads = cms.vstring( payloads )
    )
                                    )

############################
## adding KinFitter stuff
############################

from TopQuarkAnalysis.TopObjectResolutions.stringResolutions_etEtaPhi_cff import *

# original version /TopQuarkAnalysis/TopKinFitter/python/TtSemiLepKinFitProducer_Electrons_cfi.py
process.kinFitTtSemiLepEventCSVMnoSF = cms.EDProducer("TtSemiLepKinFitProducerMuon",
    jets = cms.InputTag("pfShyftSkim:jets"),
    leps = cms.InputTag("pfShyftSkim:muons"),
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
    bTagAlgo          = cms.string("combinedSecondaryVertexBJetTags"),
    minBDiscBJets     = cms.double(0.679),
    maxBDiscLightJets = cms.double(0.679),
    useBTagging       = cms.bool(True),

    # ------------------------------------------------
    # option to use the btagger of choice: -1 -- ignore, 1 -- right out of the box,
    # 2 -- Nominal SF, 4 -- SF up, 8 -- SF down.
    # ------------------------------------------------                                                                                                    
    btaggingIncludingSF = cms.int32(-1),
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

process.tprimeNtupleDumperCSVMnoSF = cms.EDProducer("TprimeNtupleDumper",
    do_MC = cms.bool(False),
    resonanceId = cms.int32(6),                                              
    kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMnoSF"),
    selectorLabel  = cms.string("pfShyftSkim"),
                                            )
# add pure min Chi2 and CSVM b-taggers for comparison
process.kinFitTtSemiLepEventCHI2 = process.kinFitTtSemiLepEventCSVMnoSF.clone()
process.kinFitTtSemiLepEventCHI2.useBTagging = False

process.tprimeNtupleDumperCHI2 = process.tprimeNtupleDumperCSVMnoSF.clone()
process.tprimeNtupleDumperCHI2.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2")

process.kinFitTtSemiLepEventCSVM = process.kinFitTtSemiLepEventCSVMnoSF.clone()
process.kinFitTtSemiLepEventCSVM.useBTagging = True

process.tprimeNtupleDumperCSVM = process.tprimeNtupleDumperCSVMnoSF.clone()
process.tprimeNtupleDumperCSVM.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVM")


process.p = cms.Path(
    process.patTriggerDefaultSequence*
    process.pfShyftSkim*
    (process.kinFitTtSemiLepEventCHI2 * process.tprimeNtupleDumperCHI2 +
     process.kinFitTtSemiLepEventCSVM * process.tprimeNtupleDumperCSVM)
    )

## configure output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents   = cms.untracked.PSet(SelectEvents = cms.vstring('p') ),                               
    fileName = cms.untracked.string('ttTest.root'),
    outputCommands = cms.untracked.vstring('drop *')
)
process.out.outputCommands += ['keep *_kinFitTtSemiLepEvent*_*_*',
                               'keep *_pfShyftSkim*_*_*',
                               'keep *_tprimeNtupleDumper*_*_*',
                               'keep PileupSummaryInfos_*_*_*',
                               'keep *_goodOfflinePrimaryVertices_*_*',
                               'keep *_patTriggerEvent_*_*',
                               'keep *_patTrigger_*_*'
                               ]

## output path
process.outpath = cms.EndPath(process.out)

#suppress the L1 trigger error messages
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit =
cms.untracked.int32(0) )
