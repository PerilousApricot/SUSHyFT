import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

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

options.register ('useFlavorHistory',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Flavor History Mode")

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
                 'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Electron trigger to run")

options.register('eleEt',
                  35.,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.float,
                 "electron et threshold")

options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

if options.doMC > 0 :
    inputDoMC = True
else :
    inputDoMC = False
    # get JSON file correctly parced
    JSONfile = 'Cert_160404-173692_7TeV_PromptReco_Collisions11_JSON.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
#if len(options.inputFiles) == 0  and options.ttbsmPAT > 0 :
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        'file:///uscms_data/d2/skhalil/SHyFT_backup/CMSSW_4_2_4/src/PhysicsTools/TagAndProbe/test/utilities/mySkim2.root',
        #'/store/user/lpctlbsm/skhalil/SingleElectron/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_9_1_Zhd.root', 
        )
                                )
else :
    filelist = open( options.inputFiles[0], 'r' )
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        filelist.readlines()
        )
                                )
    
if inputDoMC == False :
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V12::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')


from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputRootFile)
                                   )
payloads = [
    'Jec12_V1_L1FastJet_AK5PFchs.txt',
    'Jec12_V1_L2Relative_AK5PFchs.txt',
    'Jec12_V1_L3Absolute_AK5PFchs.txt',
    'Jec12_V1_L2L3Residual_AK5PFchs.txt',
    'Jec12_V1_Uncertainty_AK5PFchs.txt'
]

process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    ePlusJets = cms.bool( True ),
    muPlusJets = cms.bool( False ),
    eleTrig = cms.string(options.triggerName),	    
    usePFIso = cms.bool(True),
    useVBTFDetIso  = cms.bool(False),
    eEtCut = cms.double(options.eleEt),
    jetPtMin = cms.double(35.0),##
    minJets = cms.int32(5),
    metMin = cms.double(20.0),
    reweightPU = cms.bool(False), 
    useData = cms.bool( not inputDoMC ),       
    heavyFlavour = cms.bool( useFlavorHistory ),
    doMC = cms.bool( inputDoMC),
    sampleName = cms.string(inputSampleName),
    identifier = cms.string('PF'),
    cutsToIgnore=cms.vstring(inputCutsToIgnore),
    jecPayloads = cms.vstring( payloads )
    )
                                    )
    
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    identifier = cms.string('PF no MET')
    )
    )

process.pfShyftAnaMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    metMax = cms.double(20.),
    identifier = cms.string('PF MET < 20')
    )
    )

process.p = cms.Path(
    process.patTriggerDefaultSequence*
    process.pfShyftAna*
    process.pfShyftAnaNoMET*              
    process.pfShyftAnaMETMax20
    )

#suppress the L1 trigger error messages
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit =
cms.untracked.int32(0) )
