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

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010B-Nov4ReReco_shyft_387_v2/5a2240d5c992747bfe14fad04174e9c6/shyft_386_10_1_ZoM.root',
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010B-Nov4ReReco_shyft_387_v2/5a2240d5c992747bfe14fad04174e9c6/shyft_386_11_1_h0X.root',
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010B-Nov4ReReco_shyft_387_v2/5a2240d5c992747bfe14fad04174e9c6/shyft_386_12_1_uXd.root',
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010B-Nov4ReReco_shyft_387_v2/5a2240d5c992747bfe14fad04174e9c6/shyft_386_13_1_4ls.root',
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010B-Nov4ReReco_shyft_387_v2/5a2240d5c992747bfe14fad04174e9c6/shyft_386_14_1_vcP.root',
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Mu/Run2010B-Nov4ReReco_shyft_387_v2/5a2240d5c992747bfe14fad04174e9c6/shyft_386_15_1_lOK.root'
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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputRootFile)
                                   )


process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                        muTrig = cms.string(options.muTrig),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC ),
                                        useData = cms.bool( not inputDoMC ),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF')
                                        )
                                    )

process.pfShyftAnaLoose = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose'),
                                        metSrc = cms.InputTag('patMETsPFlowLoose'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlowLoose'),
                                        muTrig = cms.string(options.muTrig),                                                  
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        useData = cms.bool( not inputDoMC ),
                                        sampleName = cms.string(inputSampleName),
                                        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                            cutsToIgnore=cms.vstring('RelIso','D0')
                                            ),
                                        identifier = cms.string('PF Loose')
                                                  
                                        )                                    
                                    )


process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('PF no MET')
        )
    )



process.pfShyftAnaLooseNoMET = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose'),
                                        metSrc = cms.InputTag('patMETsPFlowLoose'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlowLoose'),
                                        muTrig = cms.string(options.muTrig),                                                  
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(0.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        useData = cms.bool( not inputDoMC ),
                                        sampleName = cms.string(inputSampleName),
                                        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                            cutsToIgnore=cms.vstring('RelIso','D0')
                                            ),
                                        identifier = cms.string('PF Loose No MET')
                                                  
                                        )                                    
                                    )

process.pfShyftAnaLooseNoMETWithD0 = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose'),
                                        metSrc = cms.InputTag('patMETsPFlowLoose'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlowLoose'),
                                        muTrig = cms.string(options.muTrig),                                                        
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(0.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        useData = cms.bool( not inputDoMC ),
                                        sampleName = cms.string(inputSampleName),
                                        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                            cutsToIgnore=cms.vstring('RelIso')
                                            ),
                                        identifier = cms.string('PF Loose No MET With D0 Cut')
                                                  
                                        )                                    
                                    )

process.pfShyftAnaLooseWithD0 = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose'),
                                        metSrc = cms.InputTag('patMETsPFlowLoose'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlowLoose'),
                                        muTrig = cms.string(options.muTrig),                                                   
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        useData = cms.bool( not inputDoMC ),
                                        sampleName = cms.string(inputSampleName),
                                        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                            cutsToIgnore=cms.vstring('RelIso')
                                            ),
                                        identifier = cms.string('PF Loose With D0 Cut')                                                  
                                        )                                    
                                    )


process.pfRecoShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuons'),
                                        electronSrc = cms.InputTag('selectedPatElectrons'),
                                        metSrc = cms.InputTag('patMETsPF'),
                                        jetSrc = cms.InputTag('selectedPatJetsAK5PF'),
                                        muTrig = cms.string(options.muTrig),                                            
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        useData = cms.bool( not inputDoMC ),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF With RECO Leptons')
                                        )                                    
                                    )


process.pfRecoShyftAnaNoMET = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuons'),
                                        electronSrc = cms.InputTag('selectedPatElectrons'),
                                        metSrc = cms.InputTag('patMETsPF'),
                                        jetSrc = cms.InputTag('selectedPatJetsAK5PF'),
                                        muTrig = cms.string(options.muTrig),                                                 
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(0.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        useData = cms.bool( not inputDoMC ),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF With RECO Leptons No MET')
                                        )                                    
                                    )

process.pfRecoShyftAnaNoMETLoose = cms.EDAnalyzer('EDSHyFT',
                                                  shyftAnalysis = inputShyftAnalysis.clone(
                                                      muonSrc = cms.InputTag('selectedPatMuons'),
                                                      electronSrc = cms.InputTag('selectedPatElectrons'),
                                                      metSrc = cms.InputTag('patMETsPF'),
                                                      jetSrc = cms.InputTag('selectedPatJetsAK5PF'),
                                                      muTrig = cms.string(options.muTrig),                                                      
                                                      jetPtMin = cms.double(25.0),
                                                      minJets = cms.int32(5),
                                                      metMin = cms.double(0.0),
                                                      heavyFlavour = cms.bool( useFlavorHistory ),
                                                      doMC = cms.bool( inputDoMC),
                                                      useData = cms.bool( not inputDoMC ),
                                                      sampleName = cms.string(inputSampleName),
                                                      muonIdTight = inputShyftAnalysis.muonIdTight.clone(
                                                          cutsToIgnore=cms.vstring('RelIso', 'D0')
                                                          ),
                                                      identifier = cms.string('PF With RECO Leptons No MET LOOSE')                                                              
                                                      )                                    
                                                  )

process.jptShyftAna = cms.EDAnalyzer('EDSHyFT',
                                     shyftAnalysis = inputShyftAnalysis.clone(
                                         metSrc = cms.InputTag('patMETsTC'),
                                         jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),
                                         muTrig = cms.string(options.muTrig),                                         
                                         jetPtMin = cms.double(30.0),
                                         metMin = cms.double(20.0),
                                         minJets = cms.int32(5),
                                         heavyFlavour = cms.bool( useFlavorHistory ),
                                         doMC = cms.bool( inputDoMC),
                                         useData = cms.bool( not inputDoMC ),
                                         sampleName = cms.string(inputSampleName),
                                         identifier = cms.string('JPT')
                                        )
                                     
                                     )


process.jptShyftAnaNoMET = process.jptShyftAna.clone(
    shyftAnalysis=process.jptShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('JPT no MET')
        )
    )

process.jptShyftAnaLooseNoMET = process.jptShyftAna.clone(
    shyftAnalysis=process.jptShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
            cutsToIgnore=cms.vstring('RelIso', 'D0')
            ),
        identifier = cms.string('JPT Loose No MET')        
        )
    )


process.jptShyftAnaLooseNoMETWithD0 = process.jptShyftAna.clone(
    shyftAnalysis=process.jptShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
            cutsToIgnore=cms.vstring('RelIso')
            ),
        identifier = cms.string('JPT Loose No MET With D0 Cut')        
        )
    )


process.jptShyftAnaLooseWithD0 = process.jptShyftAna.clone(
    shyftAnalysis=process.jptShyftAna.shyftAnalysis.clone(
        metMin = cms.double(20.0),
        muonIdTight = inputShyftAnalysis.muonIdTight.clone(
            cutsToIgnore=cms.vstring('RelIso')
            ),
        identifier = cms.string('JPT Loose With D0 Cut')        
        )
    )

if inputDoMC :
    caloBTag = 'simpleSecondaryVertexBJetTags'
else :
    caloBTag = 'simpleSecondaryVertexHighEffBJetTags'

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
                                          jetPtMin = cms.double(30.0),
                                          metMin = cms.double(30.0),
                                          minJets = cms.int32(5),
                                          muTrig = cms.string(options.muTrig),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( inputDoMC),
                                          useData = cms.bool( not inputDoMC ),
                                          sampleName = cms.string(inputSampleName),
                                          btaggerString = cms.string(caloBTag),
                                          identifier = cms.string('CALO')
                                          )                                      
                                      )


process.caloShyftAnaNoMET = process.caloShyftAna.clone(
    shyftAnalysis=process.caloShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('CALO no MET')
        )
    )

process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaNoMET*
    process.pfShyftAnaLoose*
    process.pfShyftAnaLooseNoMET*
    process.pfShyftAnaLooseNoMETWithD0*
    process.pfShyftAnaLooseWithD0
#    process.pfRecoShyftAna*
#    process.pfRecoShyftAnaNoMET*
#    process.pfRecoShyftAnaNoMETLoose
    )


process.MessageLogger.cerr.FwkReport.reportEvery = 1000
