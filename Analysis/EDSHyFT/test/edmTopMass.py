import FWCore.ParameterSet.Config as cms

process = cms.Process("KinFit")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
#import FWCore.PythonUtilities.LumiList as LumiList

#from PhysicsTools.PatAlgos.patTemplate_cfg import *
#from PhysicsTools.PatAlgos.tools.coreTools import *


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V12::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

#process.patTrigger.addL1Algos = cms.bool(False)

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )


###############################
####### Parameters ############
###############################
#from FWCore.ParameterSet.VarParsing import VarParsing
#options = VarParsing ('python')

#options.parseArguments()

#print options

import sys
import string


# switch on PAT trigger
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger( process, hltProcess="HLT" )

#process.setName_("KinFit")

## Source
#if len(options.inputFiles) == 0 :
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    #['dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/resilient/makouski/SingleElectronMay10ReReco_trigV3/%s'%fn for fn in flist]
#    '/store/user/lpctlbsm/srappocc/SingleElectron/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_355_0_chT.root',
    '/store/user/lpctlbsm/srappocc/SingleElectron/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_356_1_nwE.root',
    '/store/user/lpctlbsm/srappocc/SingleElectron/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_355_1_mfP.root',
    
    )
                            )
#else :
#    filelist = open( options.inputFiles[0], 'r' )
#    prepend = 'dcap:///pnfs/cms/WAX/11'
#    infilenames = cms.untracked.vstring()
#    for line in filelist.readlines():
#        infilenames.append( prepend + string.replace(line,'\n',''))
#    print infilenames
#    process.source = cms.Source("PoolSource",
#                                fileNames = infilenames
#                                )
    

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as inputShyftAnalysis
PROBE_COLLECTION = 'selectedPatElectronsPFlow'
TRIGGER = 'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v3'

process.pfShyftSkim = cms.EDFilter('EDWPlusJetsSelector',
                                   inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag(PROBE_COLLECTION),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    trigSrc = cms.InputTag('patTriggerEvent'), # PFlow
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    muonIdTight = cms.PSet(
      version = cms.string('FALL10'),
      Chi2 = cms.double(10.0),
      D0 = cms.double(0.02),
      ED0 = cms.double(999.0),
      SD0 = cms.double(999.0),
      NHits = cms.int32(11),
      NValMuHits = cms.int32(0),
      ECalVeto = cms.double(999.0),
      HCalVeto = cms.double(999.0),
      RelIso = cms.double(0.05),
      LepZ = cms.double(1.0),
      nPixelHits = cms.int32(1),
      nMatchedStations=cms.int32(1),
      cutsToIgnore = cms.vstring('ED0', 'SD0', 'ECalVeto', 'HCalVeto'),
      RecalcFromBeamSpot = cms.bool(False),
      beamLineSrc = cms.InputTag("offlineBeamSpot"),
      pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
    ),
    muonIdLoose = cms.PSet(
       beamLineSrc = cms.InputTag("offlineBeamSpot"),
       cutsToIgnore = cms.vstring('Chi2', 'D0', 'ED0', 'SD0', 'NHits', 'NValMuHits', 'ECalVeto', 'HCalVeto', 'LepZ', 'nPixelHits', 'nMatchedStations'),
       SD0 = cms.double(999.0),
       version = cms.string('FALL10'),
       nPixelHits = cms.int32(1),
       LepZ = cms.double(1.0),
       Chi2 = cms.double(999.0),
       HCalVeto = cms.double(999.0),
       ED0 = cms.double(999.0),
       ECalVeto = cms.double(999.0),
       nMatchedStations = cms.int32(1),
       NValMuHits = cms.int32(-1),
       RelIso = cms.double(0.2),
       RecalcFromBeamSpot = cms.bool(False),
       NHits = cms.int32(-1),
       D0 = cms.double(999.0),
       pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
    ),
    pvSelector = cms.PSet(
        maxZ = cms.double(15.0),
        minNdof = cms.double(4.0),
        maxRho = cms.double(2.0),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
    ),
    eleTrig = cms.string(TRIGGER),
    ePlusJets = cms.bool(True),
    muPlusJets = cms.bool(False),
    eEtCut = cms.double(30.0),
    jetPtMin = cms.double(30.0),##
    minJets = cms.int32(4),
    metMin = cms.double(0.0),                                        
    doMC = cms.bool( False ),
    identifier = cms.string('PF'),
    jetAlgo = cms.string("pf"),
    weightSFCalc = cms.bool(False),                                        
    useCustomPayload = cms.bool(False),
    bcEffScale = cms.double(1.00),
    lfEffScale = cms.double(1.00),
    jetSmear = cms.double(0.1),
    cutsToIgnore=cms.vstring()
    )
                                   )

from TopQuarkAnalysis.TopObjectResolutions.stringResolutions_etEtaPhi_cff import *

# original version /TopQuarkAnalysis/TopKinFitter/python/TtSemiLepKinFitProducer_Electrons_cfi.py
process.kinFitTtSemiLepEvent = cms.EDProducer("TtSemiLepKinFitProducerElectron",
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
    minBDiscBJets     = cms.double(1.0),
    maxBDiscLightJets = cms.double(3.0),
    useBTagging       = cms.bool(False),

    # ------------------------------------------------
    # settings for the KinFitter
    # ------------------------------------------------    
    maxNrIter = cms.uint32(200),
    maxDeltaS = cms.double(0.2),
    maxF      = cms.double(0.1),
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
                                              
    # using old energy resolutions for the time being
    # 
)

process.tprimeNtupleDumper = cms.EDProducer("TprimeNtupleDumper",
    kinFitterLabel = cms.string("kinFitTtSemiLepEvent"),
    selectorLabel  = cms.string("pfShyftSkim"),
)


process.p = cms.Path(
    process.patTriggerDefaultSequence *
    process.pfShyftSkim *
    process.kinFitTtSemiLepEvent *
    process.tprimeNtupleDumper
)

## configure output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents   = cms.untracked.PSet(SelectEvents = cms.vstring('p') ),                               
    fileName = cms.untracked.string('ttTest.root'),
    outputCommands = cms.untracked.vstring('drop *')
)
process.out.outputCommands += ['keep *_kinFitTtSemiLepEvent_*_*', 'keep *_pfShyftSkim_*_*', 'keep *_tprimeNtupleDumper_*_*']

## output path
process.outpath = cms.EndPath(process.out)
