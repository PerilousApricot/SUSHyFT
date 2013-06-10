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


options.register('caloMetMin',
                 0.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Min MET for calo met")

options.register('jptMetMin',
                 0.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Min MET for jpt met")


options.register('pfMetMin',
                 0.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Min MET for pf met")

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
    JSONfile = 'Cert_132440-144114_7TeV_StreamExpress_Collisions10_JSON_v2.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'file:syncex_shyft_382_mc.root'
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/InclusiveMu15/shyft_38xOn35x_v1/91f2fc34c53b68691c104fb43fa3e9f4/shyft_382_mc_1_1_rw3.root'
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v2/b8014e49c41bd22a9b4664626194b599/shyft_382_mc_1_1_fU1.root'
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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("gooddata_7oct2010_v5_noiso.root")
                                   )


process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose'),
                                        metSrc = cms.InputTag('patMETsPFlowLoose'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlowLoose'),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(options.pfMetMin),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                            cutsToIgnore=cms.vstring('RelIso','D0')
                                            )
                                        )                                    
                                    )

process.jptShyftAna = cms.EDAnalyzer('EDSHyFT',
                                     shyftAnalysis = inputShyftAnalysis.clone(
                                         metSrc = cms.InputTag('patMETsTC'),
                                         jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),                                         
                                         jetPtMin = cms.double(30.0),
                                         metMin = cms.double(options.jptMetMin),
                                         minJets = cms.int32(5),
                                         heavyFlavour = cms.bool( useFlavorHistory ),
                                         doMC = cms.bool( inputDoMC),
                                         sampleName = cms.string(inputSampleName),
                                         identifier = cms.string('JPT'),
                                         muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                             cutsToIgnore=cms.vstring('RelIso', 'D0')
                                             )
                                        )
                                     
                                     )

if inputDoMC :
    caloBTag = 'simpleSecondaryVertexBJetTags'
else :
    caloBTag = 'simpleSecondaryVertexHighEffBJetTags'

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
                                          jetPtMin = cms.double(30.0),
                                          metMin = cms.double(options.caloMetMin),
                                          minJets = cms.int32(5),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( inputDoMC),
                                          sampleName = cms.string(inputSampleName),
                                          btaggerString = cms.string(caloBTag),
                                          identifier = cms.string('CALO'),
                                          muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                              cutsToIgnore=cms.vstring('RelIso', 'D0')
                                              )
                                          )                                      
                                      )

process.p = cms.Path(
    process.pfShyftAna*process.jptShyftAna*process.caloShyftAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
