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

options.register('jetRecoType',
                 'pf',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Jet reco type to run, one of calo,jpt,pf")

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
                                   fileName = cms.string("shyftStudies_disccut.root")
                                   )



process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        metMin = cms.double(20.0)
                                        )                                    
                                    )

process.jptShyftAna = cms.EDAnalyzer('EDSHyFT',
                                     shyftAnalysis = inputShyftAnalysis.clone(
                                         metSrc = cms.InputTag('patMETsTC'),
                                         jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),                                         
                                         jetPtMin = cms.double(30.0),
                                         minJets = cms.int32(5),
                                         heavyFlavour = cms.bool( useFlavorHistory ),
                                         doMC = cms.bool( inputDoMC),
                                         sampleName = cms.string(inputSampleName),
                                         identifier = cms.string('JPT'),
                                         metMin = cms.double(20.0)
                                        )
                                     
                                     )

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
                                          jetPtMin = cms.double(30.0),
                                          minJets = cms.int32(5),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( inputDoMC),
                                          sampleName = cms.string(inputSampleName),
                                          btaggerString = cms.string('simpleSecondaryVertexBJetTags'),
                                          identifier = cms.string('CALO'),
                                          metMin = cms.double(30.0)
                                          )                                      
                                      )

discs = [
    0., 1.74, 1.95, 2.02, 2.15, 2.25
    ]

jetRecoTypeAnaStr =  options.jetRecoType + 'ShyftAna'

process.p = cms.Path(
    getattr( process, jetRecoTypeAnaStr)
    )


for idisc in range(0, len(discs) ) :
    disc = discs[idisc]
    print 'Adding bdiscriminator = ' + str(disc) + ' to process ' + jetRecoTypeAnaStr
    
    setattr( process, jetRecoTypeAnaStr + str(idisc), process.pfShyftAna.clone(
        shyftAnalysis = process.caloShyftAna.shyftAnalysis.clone(
            bDiscriminantCut = cms.double( disc ),
            useDefaultDiscriminant=cms.bool(False),
            identifier = cms.string( options.jetRecoType + 'BDISC ' + str(disc) )
            )
        )
             )
    process.p *= cms.Sequence(getattr( process, jetRecoTypeAnaStr + str(idisc)))


process.MessageLogger.cerr.FwkReport.reportEvery = 10000
