
# SHyFT configuration
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")


options.parseArguments()

print options

import sys

# Set to true for running on data
useData = options.useData

if options.useData == False :
    # Make sure to NOT apply L2L3Residual to MC
    corrections = ['L2Relative', 'L3Absolute']
    # global tag for 384 MC
    process.GlobalTag.globaltag = cms.string('START38_V14::All')
else :
    # Make sure to apply L2L3Residual to data
    corrections = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    # global tag for 386 data
    process.GlobalTag.globaltag = cms.string('GR_R_38X_V15::All')



process.load('Configuration.StandardSequences.Services_cff')
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
 smearedPFJets = cms.PSet(
   initialSeed = cms.untracked.uint32(183694527)
 )
)


# require HLT_Mu9 trigger
from HLTrigger.HLTfilters.hltHighLevel_cfi import *


process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Mu9", "HLT_Mu15*"])


process.step1.throw = False

# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

 
# get the 7 TeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *



# require physics declared
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process )
process.patTriggerEvent.processName = cms.string( options.hltProcess )
process.patTrigger.processName = cms.string( options.hltProcess )


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24.0), 
                                           maxd0 = cms.double(2) 
                                           )

# Now add the two PF sequences, one for the tight leptons, the other for the loose.
# For both, do the fastjet area calculation for possible pileup subtraction correction. 

from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfix) 


# turn to false when running on data
if useData :
    removeMCMatching(process, ['All'])



process.smearedPFJets = cms.EDProducer("SmearedPFJetProducer",
  src = cms.InputTag("pfJetsPFlow"),
  MeanEta = cms.double(0.0),
  StdDevEta = cms.double(0.1),
  MeanPhi = cms.double(0.0),
  StdDevPhi = cms.double(0.1),
)



switchJetCollection( process,
                     jetCollection=cms.InputTag('smearedPFJets'),
                     jetCorrLabel=('AK5PF', cms.vstring(corrections) ),
                     doJTA        = True,
                     doBTagging   = True,
                     doType1MET   = True,
                     genJetCollection=cms.InputTag("ak5GenJets"),
                     doJetID      = True                     
                     )




# Selection
process.selectedPatJetsPFlow.cut = cms.string('pt > 25 & abs(eta) < 2.4')
process.selectedPatJets.cut = cms.string('pt > 25 & abs(eta) < 2.4')

process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD" + postfix)
    )
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD")
    )


process.selectedPatMuonsPFlow.cut = cms.string("pt > 10")
process.patMuonsPFlow.usePV = False
process.patMuonsPFlow.embedTrack = True

process.selectedPatElectronsPFlow.cut = cms.string("pt > 10")
process.patElectronsPFlow.usePV = False
process.patElectronsPFlow.embedTrack = True





process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')

process.patJets.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJets.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patTausPFlow.isoDeposits = cms.PSet()

process.patJetsPFlow.embedCaloTowers = False
process.patJetsPFlow.embedPFCandidates = False

process.patJets.embedCaloTowers = False
process.patJets.embedPFCandidates = False


# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

if useData :
    readFiles.extend( [
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A82F71C-57EA-DF11-80A2-E0CB4E55365F.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A78BF54-84EA-DF11-A0CD-485B39800BCA.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A77B760-B9E9-DF11-B2F8-90E6BA442F2B.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A777C9D-02EA-DF11-B982-90E6BA0D09E2.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A69BA60-0FEA-DF11-9879-90E6BA442F3B.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A292691-A8EA-DF11-908E-E0CB4E29C4D5.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A1C4CCB-0FEA-DF11-9642-001EC9D8D08D.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/08E0BEAD-EEE9-DF11-80B2-90E6BA442EEE.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/083FAA15-28EA-DF11-96C1-90E6BA442EF2.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/06F1A9FA-36EC-DF11-AE50-001EC9D8D08D.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/06CC3F83-08EA-DF11-A05B-E0CB4E29C4CA.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/06A53695-A8EA-DF11-BAE4-485B39800C2B.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0683478B-0FEA-DF11-9729-00261834B575.root',
        '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/066D7924-0FEA-DF11-8ED7-E0CB4E55367A.root'
        ] );
else : 
    readFiles.extend( [
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E8B2CA4D-42E7-DF11-988C-90E6BA442F16.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E847D402-12E7-DF11-97C5-003048D4EF1D.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/6EE559BE-11E7-DF11-B575-00145E5513C1.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/DC4963A1-E0E5-DF11-807E-00D0680BF898.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/D8F33E3F-58E5-DF11-9FCC-0026B9548CB5.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B2D39D4C-63E6-DF11-8CFA-003048CEB070.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B28EE7AE-48E5-DF11-9F45-001F29651428.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/9C7AD216-ACE5-DF11-BE50-001517255D36.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/788BCB6C-ACE5-DF11-A13C-90E6BA442F1F.root',

        ] );

    
process.source.fileNames = readFiles


# let it run

#print
#print "============== Warning =============="
#print "technical trigger filter:    DISABLED"
#print "physics declare bit filter:  DISABLED"
#print "primary vertex filter:       DISABLED"

process.patseq = cms.Sequence(
    process.step1*
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.smearedPFJets*
    process.patDefaultSequence
)

if not useData :
    process.patseq.remove( process.scrapingVeto )
    process.patseq.remove( process.primaryVertexFilter )
    process.patseq.remove( process.HBHENoiseFilter )    


process.p1 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p1')


# rename output file
if useData :
    process.out.fileName = cms.untracked.string('shyft_386.root')
else :
    process.out.fileName = cms.untracked.string('shyft_386_mc.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# process all the events
process.maxEvents.input = 1000
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.patEventContent_cff import patExtraAodEventContent
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerEventContent

process.out.outputCommands = [
    'keep *_flavorHistoryFilter_*_*',
    'keep *_prunedGenParticles_*_*',
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_patMETs*_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_offlinePrimaryVertices_*_*',
    'drop patPFParticles_*_*_*',
    'drop *_MEtoEDMConverter_*_*'
    ]


if useData :
    process.out.outputCommands.append( 'keep LumiSummary_lumiProducer_*_*' )
