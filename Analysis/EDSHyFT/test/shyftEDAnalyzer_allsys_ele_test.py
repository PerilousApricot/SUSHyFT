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
                 'Wjets',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register ('qcdMC',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run all over QCD MC at WP95 besides other test config (1) or just the test config (0)")

options.register('ignoreTrigger',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Ignore trigger in selection")


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
                                    '/store/user/makouski/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/shyft_414_v1/4102b2143a05266d07e3ed7d177f56c8/shyft_414patch1_mc_9_1_Z8F.root',
                                    '/store/user/makouski/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/shyft_414_v1/4102b2143a05266d07e3ed7d177f56c8/shyft_414patch1_mc_99_1_yiR.root',
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

#_____________________________________PF__________________________________________________
process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                        ePlusJets = cms.bool(True),
                                        muPlusJets = cms.bool(False),
                                        jetPtMin = cms.double(25.0),##
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),                                        
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        jetAlgo = cms.string("pf"),
                                        simpleSFCalc = cms.bool(False),                                        
                                        reweightBTagEff = cms.bool(True),
                                        weightSFCalc = cms.bool(True),                                        
                                        useCustomPayload = cms.bool(False),
                                        bcEffScale = cms.double(1.00),
                                        lfEffScale = cms.double(1.00),
                                        jetSmear = cms.double(0.1),
                                        cutsToIgnore=cms.vstring(inputCutsToIgnore)
                                        )                                    
                                    )

process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('PF no MET')
        )
    )

#______________switch to PF iso < 0.1 with WP70________
process.pfShyftAnaPFIso = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    identifier = cms.string('PF Iso')
    )
    )

process.pfShyftAnaNoMETPFIso = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    metMin = cms.double(0.0),
    identifier = cms.string('PF Iso, no MET')
    )
    )

#____________relax PF iso < 0.15 with WP70________
process.pfShyftAnaPFIso15WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso<0.15, WP70')
    )
    )

process.pfShyftAnaNoMETPFIso15WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    metMin = cms.double(0.0),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso<0.15, WP70, no MET')
    )
    )

#___________________relax PF iso < 0.2 with WP70_______
process.pfShyftAnaPFIso20WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.20),
    identifier = cms.string('PF Iso<0.2, WP70')
    )
    )

process.pfShyftAnaNoMETPFIso20WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    metMin = cms.double(0.0),
    eRelIso = cms.double(0.20),
    identifier = cms.string('PF Iso<0.2, WP70, no MET')
    )
    )

#________switch to PF iso < 0.1 with WP80____________
process.pfShyftAnaPFIso10WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    identifier = cms.string('PF Iso<0.2, WP80')
    )
    )

process.pfShyftAnaNoMETPFIso10WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    metMin = cms.double(0.0),
    identifier = cms.string('PF Iso, no MET')
    )
    )
#_________relax pfiso < 0.15 with WP80____________
process.pfShyftAnaPFIso15WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso<0.15, WP80')
    )
    )

process.pfShyftAnaNoMETPFIso15WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    metMin = cms.double(0.0),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso<0.15, WP80, no MET')
    )
    )

#_____________det iso < 0.1, QCD WP95______________
process.pfShyftAnaQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    identifier = cms.string('PF MET, WP95')
    )
    )

process.pfShyftAnaQCDWP95NoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    identifier = cms.string('PF no MET, WP95')
    )
    )
#__________________PF iso < 0.1, QC WP95________________
process.pfShyftAnaPFIsoQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    usePFIso = cms.bool(True),
    identifier = cms.string('PF MET, PF Iso<0.1, WP95')
    )
    )

process.pfShyftAnaNoMETPFIsoQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    usePFIso = cms.bool(True),
    identifier = cms.string('PF MET, PF Iso<0.1, WP95, NoMET')
    )
    )

#__________________PF iso < 0.15, QC WP95________________
process.pfShyftAnaPFIso15QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF MET, PF Iso<0.15, WP95')
    )
    )

process.pfShyftAnaNoMETPFIso15QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF MET, PF Iso<0.15, WP95, NoMET')
    )
    )

#__________________PF iso < 0.20, QC WP95________________
process.pfShyftAnaPFIso20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.20),
    identifier = cms.string('PF MET, PF Iso<0.2, WP95')
    )
    )

process.pfShyftAnaNoMETPFIso20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.20),
    identifier = cms.string('PF MET, PF Iso<0.2, WP95, NoMET')
    )
    )

#___________________________
process.p = cms.Path(
    process.pfShyftAna*                
    process.pfShyftAnaNoMET*
    process.pfShyftAnaPFIso*
    process.pfShyftAnaNoMETPFIso*
    process.pfShyftAnaPFIso15WP70*
    process.pfShyftAnaNoMETPFIso15WP70*
    process.pfShyftAnaPFIso20WP70*
    process.pfShyftAnaNoMETPFIso20WP70*
    process.pfShyftAnaPFIso10WP80*
    process.pfShyftAnaNoMETPFIso10WP80*
    process.pfShyftAnaPFIso15WP80*
    process.pfShyftAnaNoMETPFIso15WP80
    )

process.s = cms.Path(
    process.pfShyftAnaPFIso*
    process.pfShyftAnaNoMETPFIso*
    process.pfShyftAnaQCDWP95*
    process.pfShyftAnaQCDWP95NoMET*
    process.pfShyftAnaPFIsoQCDWP95*
    process.pfShyftAnaNoMETPFIsoQCDWP95*
    process.pfShyftAnaPFIso15QCDWP95*
    process.pfShyftAnaNoMETPFIso15QCDWP95*
    process.pfShyftAnaPFIso20QCDWP95*
    process.pfShyftAnaNoMETPFIso20QCDWP95
   )


if options.qcdMC == 1 :
    process.p = process.s
 
    
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
