import FWCore.ParameterSet.Config as cms

process = cms.Process("myprocess")

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(1)
        )

process.source = cms.Source("EmptySource")


process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


from JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff import *


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string( 'GR_R_42_V23::All' )
##-------------------- Import the JEC services -----------------------
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.readAK5PFchs = cms.EDAnalyzer('JetCorrectorDBReader', 
                                   payloadName    = cms.untracked.string('AK5PFchs'),
                                   printScreen    = cms.untracked.bool(False),
                                   createTextFile = cms.untracked.bool(True),
                                   globalTag      = cms.untracked.string('Jec12_V1')
                                   )
process.p = cms.Path( process.readAK5PFchs )
