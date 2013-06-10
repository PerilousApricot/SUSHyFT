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

options.register('caloMetMin',
                 30.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Min MET for calo met")

options.register('jptMetMin',
                 20.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Min MET for jpt met")


options.register('pfMetMin',
                 20.,
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


inputSampleName = options.sampleNameInput

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                   # 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/InclusiveMu15/shyft_38xOn35x_v1/91f2fc34c53b68691c104fb43fa3e9f4/shyft_382_mc_1_1_rw3.root'
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v2/b8014e49c41bd22a9b4664626194b599/shyft_382_mc_1_1_fU1.root'
                                    )
                                )
else :
    filelist = open( options.inputFiles[0], 'r' )
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    filelist.readlines()
                                    )
                                )

inputDoMC = True

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies_metcut.root")
                                   )



process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                        jetPtMin = cms.double(25.0),
                                        metMin = cms.double(options.pfMetMin),
                                        minJets = cms.int32(5),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        simpleSFCalc = cms.bool(True),                                                  
                                        bcEffScale = cms.double(0.88),
                                        lfEffScale = cms.double(0.87)                                        
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
                                         simpleSFCalc = cms.bool(True),                                                  
                                         bcEffScale = cms.double(0.88),
                                         lfEffScale = cms.double(0.87),                                         
                                        )
                                     
                                     )

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
                                          jetPtMin = cms.double(30.0),
                                          metMin = cms.double(options.caloMetMin),
                                          minJets = cms.int32(5),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( inputDoMC),
                                          sampleName = cms.string(inputSampleName),
                                          btaggerString = cms.string('simpleSecondaryVertexBJetTags'),
                                          identifier = cms.string('CALO'),
                                          simpleSFCalc = cms.bool(True),                                                  
                                          bcEffScale = cms.double(0.88),
                                          lfEffScale = cms.double(0.87),                                          
                                          )                                      
                                      )


process.pfShyftAnaJES095 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('PFJES095')
        )
    )

process.pfShyftAnaJES105 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('PFJES105')
        )
    )

process.jptShyftAnaJES095 = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('JPTJES095')
        )
    )

process.jptShyftAnaJES105 = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('JPTJES105')
        )
    )

process.caloShyftAnaJES09 = process.caloShyftAna.clone(
    shyftAnalysis = process.caloShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(0.9),
        identifier = cms.string('CALOJES090')
        )
    )

process.caloShyftAnaJES11 = process.caloShyftAna.clone(
    shyftAnalysis = process.caloShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.1),
        identifier = cms.string('CALOJES110')
        )
    )

process.p = cms.Path(
#    process.pfShyftAna
    process.pfShyftAna*process.pfShyftAnaJES095*process.pfShyftAnaJES105*
    process.jptShyftAna*process.jptShyftAnaJES095*process.jptShyftAnaJES105*
    process.caloShyftAna*process.caloShyftAnaJES09*process.caloShyftAnaJES11
#    process.jptShyftAna
    )


process.MessageLogger.cerr.FwkReport.reportEvery = 1000
