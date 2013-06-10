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

options.register('sampleNameInput',
                 'top',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register('outputRootFile',
                 'shyftStudies.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "OUtput root file name")

options.register('muTrig',
                 'HLT_Mu9',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Muon trigger to run")

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
    JSONfile = 'Cert_136033-149442_7TeV_Nov4ReReco_Collisions10_JSON_Run2010B_HLT_Mu9Region.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010A-Nov4ReReco_shyft_387_v1/5a2240d5c992747bfe14fad04174e9c6/shyft_386_10_1_MIs.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010A-Nov4ReReco_shyft_387_v1/5a2240d5c992747bfe14fad04174e9c6/shyft_386_11_1_56U.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010A-Nov4ReReco_shyft_387_v1/5a2240d5c992747bfe14fad04174e9c6/shyft_386_12_1_vUE.root'
                                )
                            )

if inputDoMC == False :
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as inputShyftAnalysis


process.pfShyftSkim = cms.EDFilter('EDWPlusJetsSelector',
                                   inputShyftAnalysis.clone(
                                       muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                       electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                       metSrc = cms.InputTag('patMETsPFlow'),
                                       jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                       muTrig = cms.string(options.muTrig),
                                       jetPtMin = cms.double(25.0),
                                       minJets = cms.int32(1),
                                       metMin = cms.double(0.0),
                                       heavyFlavour = cms.bool( useFlavorHistory ),
                                       doMC = cms.bool( inputDoMC),
                                       sampleName = cms.string(inputSampleName),
                                       identifier = cms.string('PF Loose')
#                                       muonIdTight = inputShyftAnalysis.muonIdTight.clone(
#                                           cutsToIgnore=cms.vstring('RelIso')
#                                           )
                                       )
                                   )



process.p = cms.Path(
    process.pfShyftSkim
    )



process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('shyft_skim_.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_pfShyftSkim_*_*',
                                                                      'keep *_*_pileupWeights_*',
                                                                      'keep PileupSummaryInfos_*_*_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*',
                                                                      'keep patMETs_patMETsPFlow_*_*'),
                               dropMetaData = cms.untracked.string("DROPPED")
                               )
process.outpath = cms.EndPath(process.out)



# process all the events
process.maxEvents.input = 10000
process.options.wantSummary = True
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
