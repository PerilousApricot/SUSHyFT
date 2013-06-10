#########Description of options:###################
#
# When running over data, use either of the trigger options, ele or mu depending on PD type
# When running over MC, either use both the trigger switches "on" or both of them "off"
# option "triggerName" is not used, but is kept as an option for SHyFTSelector
#
###################################################
import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('usePDFs',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('useData',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use data (1) or MC (0)")

options.register('useMuTrigs',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use muon triggers (1) or not (0)")

options.register('useEleTrigs',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use electron triggers (1) or not (0)")

options.register('useLooseElectrons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add loose electron collection (1) or not (0)")

options.register('triggerName',
                 'HLT_Ele27_WP80_v8',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "trigger to run")

options.register('useLooseMuons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add loose muon collection (1) or not (0)")


options.parseArguments()

print options

#ignore trigger in SHyft Selector
inputCutsToIgnore = ['Trigger']

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

useData = True
if options.useData == 0 :
    useData = False
    #inputCutsToIgnore.append('Trigger')
    process.GlobalTag.globaltag = 'START53_V7F::All'
    payloads = [
        'Jec12_V3_MC_L1FastJet_AK5PFchs.txt',
        'Jec12_V3_MC_L2Relative_AK5PFchs.txt',
        'Jec12_V3_MC_L3Absolute_AK5PFchs.txt',
        'Jec12_V3_MC_L2L3Residual_AK5PFchs.txt',
        'Jec12_V3_MC_Uncertainty_AK5PFchs.txt',
        ]
else:
    process.GlobalTag.globaltag = 'GR_P_V40_AN1::All'
    payloads = [
        'Jec12_V3_L1FastJet_AK5PFchs.txt',
        'Jec12_V3_L2Relative_AK5PFchs.txt',
        'Jec12_V3_L3Absolute_AK5PFchs.txt',
        'Jec12_V3_L2L3Residual_AK5PFchs.txt',
        'Jec12_V3_Uncertainty_AK5PFchs.txt',
        ]


process.load("Configuration.StandardSequences.MagneticField_cff")
# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

import sys

if useData :
    jetSmear = 0.0
    inputFiles = [
        'dcap:///pnfs/cms/WAX/11/store/results/B2G/SingleElectron/StoreResults-Run2012A-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/SingleElectron/USER/StoreResults-Run2012A-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/0000/FE2F7667-4728-E211-8F95-002618FDA263.root',
        ]

else :
    jetSmear = 0.1
    inputFiles = [
        'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/meloam/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2/c04f3b4fa74c8266c913b71e0c74901d/tlbsm_53x_v2_mc_725_1_opY.root'
        ]

from HLTrigger.HLTfilters.hltHighLevel_cfi import *

eleStop = 'HLT_Ele25_CaloIdVT_CaloIsoVL_TrkIdVL_TrkIsoT_TriCentralPFNoPUJet'

if options.useMuTrigs == 0 and options.useEleTrigs == 0 :
    process.hltSelectionMu = cms.Sequence()
    process.hltSelectionEle = cms.Sequence()
else :
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = ['HLT_Mu40_eta2p1_v*',
                                                                                                       ])
    if options.useLooseElectrons==1:
	process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  [eleStop+'30_v*',
                                                                                                             eleStop+'45_35_25_v*',   
                                                                                                             eleStop+'50_40_30_v*',            
                                                                                                            ])
    else:
    	process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  ['HLT_Ele27_WP80_v*', #PD:SingleElectron
                                                                                                         ])
    process.hltSelectionMu.throw = False
    process.hltSelectionEle.throw = False

    
    if options.useMuTrigs == 0 and options.useEleTrigs == 1 :
        process.hltSelectionMu =  cms.Sequence()
    elif options.useMuTrigs == 1 and options.useEleTrigs == 0 :
        process.hltSelectionEle =  cms.Sequence()

    
process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring( inputFiles )
)

if len(options.inputFiles) > 0 :
    process.source.fileNames = options.inputFiles



## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as shyftSelectionInput


if options.usePDFs: 
	process.load('Analysis.PdfWeights.pdfWeightProducer_cfi')


process.pfShyftProducerMu = cms.EDFilter('EDSHyFTSelector',
                                         shyftSelection = shyftSelectionInput.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        ePlusJets = cms.bool( False ),
        muPlusJets = cms.bool( True ),
        muTrig = cms.string(options.triggerName),
        eleTrig = cms.string(options.triggerName),
        useNoPFIso = cms.bool(False),
        eEt = cms.double( 30.0 ), ##
        useNoID  = cms.bool(False), # use eMVA > 0.5
        eRelIso = cms.double( 0.1 ), 
        muPtMin = cms.double( 40.0 ),##
        useMuonTightID = cms.bool(True), #default off
        muRelIso = cms.double( 0.12 ),            
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(1),
        identifier = cms.string('PFMu'),
        cutsToIgnore=cms.vstring( inputCutsToIgnore ),
        useData = cms.bool(useData),
        jetSmear = cms.double(jetSmear),
        jecPayloads = cms.vstring( payloads )
        ),                                         
        matchByHand = cms.bool(False),
        useData = cms.bool(useData)                              
                                         )

# mu+jets with loose muons
process.pfShyftProducerMuLoose = process.pfShyftProducerMu.clone()
process.pfShyftProducerMuLoose.shyftSelection.muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose')
process.pfShyftProducerMuLoose.shyftSelection.electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose')
process.pfShyftProducerMuLoose.shyftSelection.useNoPFIso = cms.bool(True)
process.pfShyftProducerMuLoose.shyftSelection.muRelIso = cms.double( 20.0 ) # to be sure again
#process.pfShyftProducerMuLoose.shyftSelection.muEtaMax = cms.double( 2.1 ) #2.5
process.pfShyftProducerMuLoose.shyftSelection.useMuonTightID = cms.bool(True)
process.pfShyftProducerMuLoose.shyftSelection.identifier = cms.string('PFMuLoose')

# e+jets
process.pfShyftProducerEle = process.pfShyftProducerMu.clone()
process.pfShyftProducerEle.shyftSelection.ePlusJets = cms.bool( True )
process.pfShyftProducerEle.shyftSelection.muPlusJets = cms.bool( False )
process.pfShyftProducerMuLoose.shyftSelection.identifier = cms.string('PFEle')

# e+jets with loose electron
process.pfShyftProducerEleLoose = process.pfShyftProducerMu.clone()
process.pfShyftProducerEle.shyftSelection.ePlusJets = cms.bool( True )
process.pfShyftProducerEle.shyftSelection.muPlusJets = cms.bool( False )
process.pfShyftProducerEleLoose.shyftSelection.muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose')
process.pfShyftProducerEleLoose.shyftSelection.electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose')
process.pfShyftProducerEleLoose.shyftSelection.useNoPFIso = cms.bool(True)
process.pfShyftProducerEleLoose.shyftSelection.eRelIso = cms.double( 20.0 ) # to be sure again
process.pfShyftProducerEleLoose.shyftSelection.useNoID  = cms.bool(True) #no eMVA > 0.5 cut

# now get the edm trees:
# ====================

# get the jet trees
process.pfShyftTupleJetsMu = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerMu", "jets"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ),
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("ssvhe"),
            quantity = cms.untracked.string("bDiscriminator('simpleSecondaryVertexHighEffBJetTags')")
            ),
        cms.PSet(
            tag = cms.untracked.string("secvtxMass"),
            quantity = cms.untracked.string("userFloat('secvtxMass')")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        )  
    )



if not options.useData :
    process.pfShyftTupleJetsMu.variables.append(
        cms.PSet(
            tag = cms.untracked.string("flavor"),
            quantity = cms.untracked.string("partonFlavour()")
            )
        )
    process.pfShyftTupleJetsMu.variables.append(
        cms.PSet(
            tag = cms.untracked.string("genJetPt"),
            quantity = cms.untracked.string("? userInt('matched') ? genJet().pt : -10")
            )
    )

process.pfShyftTupleJetsMuLoose = process.pfShyftTupleJetsMu.clone(
    src = cms.InputTag("pfShyftProducerMuLoose", "jets"),
    )

process.pfShyftTupleJetsEle = process.pfShyftTupleJetsMu.clone(
    src = cms.InputTag("pfShyftProducerEle", "jets"),
    )

process.pfShyftTupleJetsEleLoose = process.pfShyftTupleJetsMu.clone(
    src = cms.InputTag("pfShyftProducerEleLoose", "jets"),
    )

# get the muon trees
process.pfShyftTupleMuons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerMu", "muons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("chIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')" )
            ),
         cms.PSet(
            tag = cms.untracked.string("nhIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')")                          
            ),
        cms.PSet(
            tag = cms.untracked.string("phIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')")                                  
            ),
         cms.PSet(
            tag = cms.untracked.string("puIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfPUChargedHadronIso')" )
            ),
        )  
    )

process.pfShyftTupleMuonsLoose = process.pfShyftTupleMuons.clone(
    src = cms.InputTag("pfShyftProducerMuLoose", "muons")
    )

process.pfShyftTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerEle", "electrons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("eMVA"),
            quantity = cms.untracked.string("electronID('mvaTrigV0')")
            ),
        cms.PSet(
            tag = cms.untracked.string("chIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')" )
            ),
         cms.PSet(
            tag = cms.untracked.string("nhIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')")                          
            ),
        cms.PSet(
            tag = cms.untracked.string("phIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')")                                  
            ),
         cms.PSet(
            tag = cms.untracked.string("puIso"),
            quantity = cms.untracked.string("userIsolation('pat::PfPUChargedHadronIso')" )
            ),
          cms.PSet(
            tag = cms.untracked.string("AEff"),
            quantity = cms.untracked.string("userFloat('AEff')" )
            ),
        )  
    )

process.pfShyftTupleElectronsLoose = process.pfShyftTupleElectrons.clone(
    src = cms.InputTag("pfShyftProducerEleLoose", "electrons"),
    )


# get the MET trees
process.pfShyftTupleMETMu = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerMu", "MET"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            )
        )  
    )

process.pfShyftTupleMETMuLoose = process.pfShyftTupleMETMu.clone(
    src = cms.InputTag("pfShyftProducerMuLoose", "MET")
    )

process.pfShyftTupleMETEle = process.pfShyftTupleMETMu.clone(
    src = cms.InputTag("pfShyftProducerEle", "MET"),
    )

process.pfShyftTupleMETEleLoose = process.pfShyftTupleMETEle.clone(
    src = cms.InputTag("pfShyftProducerEleLoose", "MET"),
    )


## pileup
process.PUNtupleDumper = cms.EDProducer("PileupReweightingPoducer",
                                        FirstTime = cms.untracked.bool(False),
                                        oneDReweighting = cms.untracked.bool(True),
                                        PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                        PileupDataFile = cms.untracked.string('PUData_finebin_dist.root')
                                        )

## configure output module
if not options.useData:
    process.p0 = cms.Path( process.PUNtupleDumper )
else:
    process.p0 = cms.Path( process.patTriggerDefaultSequence )
    
process.p1 = cms.Path(
    process.hltSelectionMu*
    process.pfShyftProducerMu*
    process.pfShyftTupleJetsMu*
    process.pfShyftTupleMuons*
    process.pfShyftTupleMETMu
    )

process.p2 = cms.Path(
    process.hltSelectionEle*
    process.pfShyftProducerEle*
    process.pfShyftTupleJetsEle*
    process.pfShyftTupleElectrons*
    process.pfShyftTupleMETEle
    )


if options.usePDFs :
    process.p1 += process.pdfWeightProducer
    process.p2 += process.pdfWeightProducer

process.p3 = cms.Path()
process.p4 = cms.Path() 
if options.useLooseElectrons:
    process.p3 = cms.Path(
        process.hltSelectionEle*
        process.pfShyftProducerEleLoose*
        process.pfShyftTupleJetsEleLoose*
        process.pfShyftTupleElectronsLoose*
        process.pfShyftTupleMETEleLoose
        )
if options.useLooseMuons :
    process.p4 = cms.Path(
        process.hltSelectionMu*
        process.pfShyftProducerMuLoose*
        process.pfShyftTupleJetsMuLoose*
        process.pfShyftTupleMuonsLoose*
        process.pfShyftTupleMETMuLoose
        )
        


process.MessageLogger.cerr.FwkReport.reportEvery = 1000


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyftDump.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p1','p2','p3','p4') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                     ##  #'keep *_pfShyftProducer_*_*',
                                                                      'keep *_*_pileupWeights_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_kt6PFJets_rho_*',
                                                                      'keep *_pdfWeightProducer_*_*',
                                                                      'keep PileupSummaryInfos_*_*_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*',
                                                                      #'keep *_patTriggerEvent_*_*',
                                                                      #'keep patTriggerPaths_patTrigger_*_*',
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")

if options.useData:
    #suppress the L1 trigger error messages
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000
    process.MessageLogger.suppressWarning.append('patTrigger')
    process.MessageLogger.cerr.FwkJob.limit=1
    process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit =
                                                           cms.untracked.int32(0) )

