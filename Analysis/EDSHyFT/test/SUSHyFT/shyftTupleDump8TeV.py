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

options.register('useLooseElectrons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add loose electron collection (1) or not (0)")

options.register('useLooseMuons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add loose muon collection (1) or not (0)")

options.register('useMETRes',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add shifted MET collection (1) or not (0)")

options.register('eleTriggerName',
                 'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "trigger to run for ele paths")

options.register('muTriggerName',
                 'HLT_Mu30_v*',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "trigger to run for muon paths")

options.register('runMuons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Run Muon paths")

options.register('runElectrons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add loose muon collection (1) or not (0)")

options.register('ignoreTrigger',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Ignore trigger bits (1) or not (0)")

options.register('minJets',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Minimum number of jets per event")


options.parseArguments()

print options
 ## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
 
inputCutsToIgnore = []
useData = True
if options.useData == 0 :
    useData = False
    #inputCutsToIgnore = ['Trigger']
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

# triggering's being done in the HLTfilter
inputCutsToIgnore = ['Trigger']
# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

process.load("Configuration.StandardSequences.MagneticField_cff")

import sys

if useData:
    inputFiles = [
            '/store/user/meloam/SingleMu/meloam_feb12_tlbsm53x2_Run2012C_24Aug2012_v1/20130212222033/00000/4463A7D0-9075-E211-95CC-003048F2E8C2.root'
        ]

else :
    inputFiles = [
            '/store/user/meloam/ZJetToMuMu_Pt-80to120_TuneZ2star_8TeV_pythia6/None/20130206162922/00000/407A66CB-E175-E211-BCF0-003048F316E8.root'
        ]

process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring( inputFiles )
)

if len(options.inputFiles) > 0 :
    process.source.fileNames = options.inputFiles


## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )

from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as shyftSelectionInput


if options.usePDFs: 
	process.load('Analysis.PdfWeights.pdfWeightProducer_cfi')

#____________________________________Trigger Filter________________________________________

from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if options.ignoreTrigger:
    process.hltSelectionMu = cms.Sequence()
    process.hltSelectionEle = cms.Sequence()
else :
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = ['HLT_IsoMu24_eta2p1_v*',
                                                                                                       'HLT_Mu40_eta2p1_v*',
                                                                                                       'HLT_PFMET_150_v*',
                                                                                                       'HLT_IsoMu17_eta2p1_DiCentralPFJet30_PFHT350_PFMHT40_v*'
                                                                                                       ])
    process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  ['HLT_Ele27_WP80_v*',
                                                                                                         'HLT_PFMET_150_v*'
                                                                                                         ])
    process.hltSelectionMu.throw = False
    process.hltSelectionEle.throw = False

process.pfShyftProducerMu = cms.EDFilter('EDSHyFTSelector',
        shyftSelection = shyftSelectionInput.clone(
            muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
            electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
            metSrc = cms.InputTag('patMETsPFlow'),
            jetSrc = cms.InputTag('goodPatJetsPFlow'),
            pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
            tauSrc = cms.InputTag('selectedPatTausPFlow'),
            ePlusJets = cms.bool( False ),
            muPlusJets = cms.bool( True ),
            matchByHand = cms.bool(False),
            muTrig = cms.string(options.muTriggerName),
            eleTrig = cms.string(options.eleTriggerName),
            jetPtMin = cms.double(10.0),##30
            minJets = cms.int32(options.minJets),
            metMin = cms.double(0.0),
            tauPtMin = cms.double(10.0),
            tauEtaMax = cms.double(3.0),
            muPtMin = cms.double(25.0),##35
            identifier = cms.string('PFMu'),
            cutsToIgnore=cms.vstring( inputCutsToIgnore ),
            useData = cms.bool(useData),
            jetSmear = cms.double(0.0),
            jecPayloads = cms.vstring( payloads )
            ),
            matchByHand = cms.bool(False),
        )
process.pfShyftProducerMuLoose = cms.EDFilter('EDSHyFTSelector',
                                              shyftSelection = shyftSelectionInput.clone(
                                                jetSrc = cms.InputTag('goodPatJetsPFlow'),
                                                muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
                                                electronSrc = cms.InputTag('selectedPatElectronsLoosePFlow'),
                                                tauSrc = cms.InputTag('selectedPatTausPFlow'),
                                                ePlusJets = cms.bool( False ),
                                                muPlusJets = cms.bool( True ),
                                                jetPtMin = cms.double(10.0),##30
                                                tauPtMin = cms.double(10.0),
                                                minJets = cms.int32(options.minJets),
                                                metMin = cms.double(0.0),
                                                muPtMin = cms.double(25.0),##35
                                                tauEtaMax = cms.double(3.0),
                                                matchByHand = cms.bool(False),
                                                identifier = cms.string('PFMuLoose'),
                                                cutsToIgnore=cms.vstring( ['Trigger','== 1 Tight Lepton','== 1 Tight Lepton, Mu Veto','== 1 Lepton'] ),
                                                useData = cms.bool(useData),
                                                jetSmear = cms.double(0.0),
                                                jecPayloads = cms.vstring( payloads ),
                                                removeLooseLep = cms.bool(True)
                                                ),
                                              matchByHand= cms.bool(False)
                                            )
#process.pfShyftProducerMuLoose.shyftSelection.muonIdTight.cutsToIgnore.append('PFIso')

process.pfShyftProducerEle = cms.EDFilter('EDSHyFTSelector',
                                    shyftSelection = shyftSelectionInput.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        tauSrc = cms.InputTag('selectedPatTausPFlow'),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        ePlusJets = cms.bool( True ),
        muPlusJets = cms.bool( False ),
        muTrig = cms.string(options.muTriggerName),
        eleTrig = cms.string(options.eleTriggerName),
        jetPtMin = cms.double(10.0),##30
        tauPtMin = cms.double(10.0),
        tauEtaMax = cms.double(3.0),
        eEtCut = cms.double(25.0),##35
        usePFIso = cms.bool(True),
        useVBTFDetIso  = cms.bool(False),
        useWP95Selection = cms.bool(False),
        useWP70Selection = cms.bool(True),
        matchByHand = cms.bool(False),
        electronIdTight = cms.PSet(
        version = cms.string('SPRING11'),
        MVA = cms.double(-0.01),
        MaxMissingHits = cms.int32(0),
        D0 = cms.double(0.02),
        electronIDused = cms.string('eidHyperTight1MC'),
        #electronIDused = cms.string('eidSuperTightMC'),
        ConversionRejection = cms.bool(False),
        PFIso = cms.double(0.1),
        cutsToIgnore = cms.vstring('MVA','MaxMissingHits', 'ConversionRejection'),
        ),
        minJets = cms.int32(options.minJets),
        metMin = cms.double(0.0),
        muPtMin = cms.double(25.0),#35
        identifier = cms.string('PFEle'),
        cutsToIgnore=cms.vstring( inputCutsToIgnore ),
        useData = cms.bool(useData),
        jetSmear = cms.double(0.0),
        jecPayloads = cms.vstring( payloads )
        ),
        matchByHand = cms.bool(False)
        )


process.pfShyftProducerEleLoose = process.pfShyftProducerEle.clone(
    shyftSelection = process.pfShyftProducerEle.shyftSelection.clone(
    useWP95Selection = cms.bool(True),# if CiC ID loose, then pf reliso<0.2 is applied
    useWP70Selection = cms.bool(False),
    )
    )

process.pfShyftProducerMetResEle090 = process.pfShyftProducerEle.clone(
    shyftSelection = process.pfShyftProducerEle.shyftSelection.clone(
    unclMetScale = cms.double( 0.90 ),
    jetSmear = cms.double(0.01),
    identifier = cms.string('PFMETRES090'),
    )
    )

process.pfShyftProducerMetResEle110 = process.pfShyftProducerEle.clone(
    shyftSelection = process.pfShyftProducerEle.shyftSelection.clone(
    unclMetScale = cms.double( 1.10 ),
    jetSmear = cms.double(0.01),
    identifier = cms.string('PFMETRES110'),
    )
    )

process.pfShyftProducerMetResMu090 = process.pfShyftProducerMu.clone(
    shyftSelection = process.pfShyftProducerMu.shyftSelection.clone(
    unclMetScale = cms.double( 0.90 ),
    jetSmear = cms.double(0.01),
    identifier = cms.string('PFMETRES090'),
    )
    )

process.pfShyftProducerMetResMu110 = process.pfShyftProducerMu.clone(
    shyftSelection = process.pfShyftProducerMu.shyftSelection.clone(
    unclMetScale = cms.double( 1.10 ),
    jetSmear = cms.double(0.01),
    identifier = cms.string('PFMETRES110'),
    )
    )
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
            quantity = cms.untracked.string("bDiscriminator('combinedSecondaryVertexBJetTags')")
            ),
        cms.PSet(
            tag = cms.untracked.string("secvtxMass"),
            quantity = cms.untracked.string("userFloat('secvtxMass')")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("tauJetPt"),
            quantity = cms.untracked.string("userFloat('tauJetPt')")
            ),
        cms.PSet(
            tag = cms.untracked.string("tauJetPhi"),
            quantity = cms.untracked.string("userFloat('tauJetPhi')")
            ),
        cms.PSet(
            tag = cms.untracked.string("tauJetEta"),
            quantity = cms.untracked.string("userFloat('tauJetEta')")
            ),
        cms.PSet(
            tag = cms.untracked.string("tauJetMass"),
            quantity = cms.untracked.string("userFloat('tauJetMass')")
            ),
        cms.PSet(
            tag = cms.untracked.string("byLooseCombinedIsolationDeltaBetaCorr3Hits"),
            quantity = cms.untracked.string("userFloat('byLooseCombinedIsolationDeltaBetaCorr3Hits')")
            ),
        cms.PSet(
            tag = cms.untracked.string("byMediumCombinedIsolationDeltaBetaCorr3Hits"),
            quantity = cms.untracked.string("userFloat('byMediumCombinedIsolationDeltaBetaCorr3Hits')")
            ),
        cms.PSet(
            tag = cms.untracked.string("byTightCombinedIsolationDeltaBetaCorr3Hits"),
            quantity = cms.untracked.string("userFloat('byTightCombinedIsolationDeltaBetaCorr3Hits')")
            ),
        cms.PSet(
            tag = cms.untracked.string("byLooseIsolationMVA2"),
            quantity = cms.untracked.string("userFloat('byLooseIsolationMVA2')")
            ),
        cms.PSet(
            tag = cms.untracked.string("byMediumIsolationMVA2"),
            quantity = cms.untracked.string("userFloat('byMediumIsolationMVA2')")
            ),
        cms.PSet(
            tag = cms.untracked.string("byTightIsolationMVA2"),
            quantity = cms.untracked.string("userFloat('byTightIsolationMVA2')")
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
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "userIsolation('pat::PfNeutralHadronIso') + " +
                                            "userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )  
    )

process.pfShyftTupleMuonsLoose = process.pfShyftTupleMuons.clone(
    src = cms.InputTag("pfShyftProducerMuLoose", "muons")
    )

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

process.pfShyftTupleMETMetResEle110 = process.pfShyftTupleMETEle.clone(
    src = cms.InputTag("pfShyftProducerMetResEle110", "MET"),
    )

process.pfShyftTupleMETMetResEle090 = process.pfShyftTupleMETEle.clone(
    src = cms.InputTag("pfShyftProducerMetResEle090", "MET"),
    )

process.pfShyftTupleMETMetResMu110 = process.pfShyftTupleMETMu.clone(
    src = cms.InputTag("pfShyftProducerMetResMu110", "MET"),
    )

process.pfShyftTupleMETMetResMu090 = process.pfShyftTupleMETMu.clone(
    src = cms.InputTag("pfShyftProducerMetResMu090", "MET"),
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
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "userIsolation('pat::PfNeutralHadronIso') + " +
                                            "userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )  
    )

process.pfShyftTupleElectronsLoose = process.pfShyftTupleElectrons.clone(
    src = cms.InputTag("pfShyftProducerEleLoose", "electrons"),
    )
#
#process.PUNtupleDumperSingleEle = cms.EDProducer("PileupReweightingPoducer",
#                                         FirstTime = cms.untracked.bool(True),
#                                         oneDReweighting = cms.untracked.bool(False),        
#                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
#                                         PileupDataFile = cms.untracked.string('dataPileupTruth_v2_finebin_160404-167913.root')
#)
#
#process.PUNtupleDumperEleHad = cms.EDProducer("PileupReweightingPoducer",
#                                         FirstTime = cms.untracked.bool(True),
#                                         oneDReweighting = cms.untracked.bool(False),        
#                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
#                                         PileupDataFile = cms.untracked.string('dataPileupTruth_v2_finebin_170826-173692.root')
#)
#
#process.PUNtupleDumperOld = cms.EDProducer("PUNtupleDumper",
#                                           PUscenario = cms.string("42X")
#                                           )

#if not options.useData:
    #process.p0 = cms.Path( process.PUNtupleDumperSingleEle + process.PUNtupleDumperEleHad + process.PUNtupleDumperOld )
#    process.p0 = cms.Path( )
#else:

process.p0 = cms.Path( process.patTriggerDefaultSequence )
    
process.p1 = cms.Path(
    process.hltSelectionMu*
    process.pfShyftProducerMu*
    process.pfShyftTupleJetsMu*
    process.pfShyftTupleMuons*
    process.pfShyftTupleMETMu
    #process.pfShyftTupleTausMu
    )

process.p2 = cms.Path(
    process.hltSelectionEle*
    process.pfShyftProducerEle*
    process.pfShyftTupleJetsEle*
    process.pfShyftTupleElectrons*
    process.pfShyftTupleMETEle
    #process.pfShyftTupleTausMu
    )


if options.usePDFs :
    process.p1 += process.pdfWeightProducer
    process.p2 += process.pdfWeightProducer

process.p3 = cms.Path()
process.p4 = cms.Path()
process.p5 = cms.Path()
process.p6 = cms.Path()

if options.useLooseElectrons:
    process.p3 = cms.Path(
        process.hltSelectionEle*
        process.pfShyftProducerEleLoose*
        process.pfShyftTupleJetsEleLoose*
        process.pfShyftTupleElectronsLoose*
        process.pfShyftTupleMETEleLoose
        #process.pfShyftTupleTausEleLoose
        )
if options.useLooseMuons :
    process.p4 = cms.Path(
        process.hltSelectionMu*
        process.pfShyftProducerMuLoose*
        process.pfShyftTupleJetsMuLoose*
        process.pfShyftTupleMuonsLoose*
        process.pfShyftTupleMETMuLoose
        #process.pfShyftTupleTausMuLoose
        )        

if options.useMETRes :
    process.p5 = cms.Path(
        process.hltSelectionEle*
        process.pfShyftProducerMetResEle090*
        process.pfShyftTupleMETMetResEle090*
        process.pfShyftProducerMetResEle110*
        process.pfShyftTupleMETMetResEle110)
    process.p6 = cms.Path(
        process.hltSelectionMu*
        process.pfShyftProducerMetResMu090*
        process.pfShyftTupleMETMetResMu090*
        process.pfShyftProducerMetResMu110*
        process.pfShyftTupleMETMetResMu110
        )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyftDump2.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p1','p2','p3','p4', 'p5', 'p6') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      #'keep *',
                                                                      #'keep *_*_pileupWeights_*',
                                                                      #'keep *_PUNtupleDumperSingleEle_*_*',
                                                                      #'keep *_PUNtupleDumperEleHad_*_*',
                                                                      #'keep *_PUNtupleDumperOld_*_*',
                                                                      'keep *_addPileupInfo_*_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_pdfWeightProducer_*_*',
                                                                      'keep PileupSummaryInfos_*_*_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*',
                                                                      'keep *_patTriggerEvent_*_*',
                                                                      'keep patTriggerPaths_patTrigger_*_*'
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

