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

options.register('sampleNameInput',
                 'top',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register ('allSys',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run all systematics (1) or just the central one (0)")


options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('eleTrig',
                 'HLT_Ele22_SW_TighterEleId_L1R_v3',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Electron trigger to run")



options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

inputDoMC=True

inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'dcap:///pnfs/cms/WAX/11/store/user/skhalil/Electron/Run2010B-Nov4ReReco_149181to149442_shyft_387_v1/3ea0376194d6ff8faf5a3ccff3084893/shyft_386_9_1_920.root',
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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies.root")
                                   )

shyftAnalysisParams = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuons'),
                                        electronSrc = cms.InputTag('selectedPatElectrons'),
                                        metSrc = cms.InputTag('patMETsPF'),
                                        jetSrc = cms.InputTag('selectedPatJetsAK5PF'),
                                        useEleMC = cms.bool(False),
                                        useAntiSelection = cms.bool(False),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(3),
                                        metMin = cms.double(20.0),                                        
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF Data'),
                                        jetAlgo = cms.string("pf"),
                                        simpleSFCalc = cms.bool(False),
                                        reweightBTagEff = cms.bool(False),
                                        useCustomPayload = cms.bool(False),                                            
                                        jetSmear = cms.double(0.0),
                                        cutsToIgnore=cms.vstring(inputCutsToIgnore)
                                       )

process.pfShyftSkim = cms.EDFilter('EDWPlusJetsSelector',
                                   shyftAnalysisParams.clone()
                                   )


process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = shyftAnalysisParams.clone()                                    
                                    )


process.pfShyftAnaQCD = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    useAntiSelection = cms.bool(True),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PFlow QCD Loose')
    )
    )



process.p = cms.Path(
    process.pfShyftSkim*
    process.pfShyftAna*
    process.pfShyftAnaQCD
    )


process.MessageLogger.cerr.FwkReport.reportEvery = 1000
