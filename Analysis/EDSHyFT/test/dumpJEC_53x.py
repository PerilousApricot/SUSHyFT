import FWCore.ParameterSet.Config as cms

process = cms.Process("jectxt")

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(1)
        )

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('runData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "GT for data (1) or MC (0)")

options.parseArguments()
print options

GTData = ''
OutSuffix = ''

if options.runData==1:
	GTData = 'GR_P_V39_AN3::All'
        OutSuffix = 'Jec12_V3'
else: 
	GTData = 'MC_53_V15::All'
        OutSuffix = 'Jec12_V3_MC'

process.source = cms.Source("EmptySource")

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff import *

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string( GTData )

##-------------------- Import the JEC services -----------------------
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.readAK5PFchs = cms.EDAnalyzer('JetCorrectorDBReader', 
                                   payloadName    = cms.untracked.string('AK5PFchs'),
                                   printScreen    = cms.untracked.bool(False),
                                   createTextFile = cms.untracked.bool(True),
                                   globalTag      = cms.untracked.string(OutSuffix)
                                   )
process.p = cms.Path( process.readAK5PFchs )
