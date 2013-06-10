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

options.register('triggerName',
                 'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "trigger to run")


options.parseArguments()

print options

inputCutsToIgnore = []
useData = True
if options.useData == 0 :
    useData = False
    inputCutsToIgnore.append('Trigger')
else:
    ## Geometry and Detector Conditions (needed for a few patTuple production steps)
    process.load("Configuration.StandardSequences.Geometry_cff")
    process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
    process.GlobalTag.globaltag = 'GR_R_42_V12::All'
    process.load("Configuration.StandardSequences.MagneticField_cff")
    
    # run the trigger on the fly
    process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

import sys

if useData:
    inputFiles = [
        #'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/dstrom/SingleElectron/SingleElectron_Run2011A-PromptReco/f8e845a0332c56398831da6c30999af1/ttbsm_42x_data_9_1_PZg.root'
        #'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/SingleMu/ttbsm_v9_Run2011A-PromptReco-v4/f8e845a0332c56398831da6c30999af1/ttbsm_42x_data_326_1_ZF4.root'
        ]

else :
    inputFiles = [
        '/store/user/b2g12006/bazterra/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_1001_1_eOl.root',
        #'dcap:///pnfs/cms/WAX/11//store/user/lpctlbsm/srappocc/TTJets_TuneZ2_7TeV-madgraph-tauola/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_9_1_7Fg.root'
        ]

process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring( inputFiles )
)

if len(options.inputFiles) > 0 :
    process.source.fileNames = options.inputFiles


payloads = [
    'Jec12_V1_L1FastJet_AK5PFchs.txt',
    'Jec12_V1_L2Relative_AK5PFchs.txt',
    'Jec12_V1_L3Absolute_AK5PFchs.txt',
    'Jec12_V1_L2L3Residual_AK5PFchs.txt',
    'Jec12_V1_Uncertainty_AK5PFchs.txt'
]

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
        jetPtMin = cms.double(10.0),##30
        minJets = cms.int32(1),
        metMin = cms.double(0.0),
        muPtMin = cms.double(25.0),##35
        identifier = cms.string('PFMu'),
        cutsToIgnore=cms.vstring( inputCutsToIgnore ),
        useData = cms.bool(useData),
        jetSmear = cms.double(0.0),
        jecPayloads = cms.vstring( payloads )
        )
        )
process.pfShyftProducerMuLoose = cms.EDFilter('EDSHyFTSelector',
                                              shyftSelection = shyftSelectionInput.clone(
                                                jetSrc = cms.InputTag('goodPatJetsPFlow'),
                                                muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
                                                electronSrc = cms.InputTag('selectedPatElectronsLoosePFlow'),
                                                ePlusJets = cms.bool( False ),
                                                muPlusJets = cms.bool( True ),
                                                jetPtMin = cms.double(10.0),##30
                                                minJets = cms.int32(1),
                                                metMin = cms.double(0.0),
                                                muPtMin = cms.double(25.0),##35
                                                identifier = cms.string('PFMuLoose'),
                                                cutsToIgnore=cms.vstring( ['Trigger','== 1 Tight Lepton','== 1 Tight Lepton, Mu Veto','== 1 Lepton'] ),
                                                useData = cms.bool(useData),
                                                jetSmear = cms.double(0.0),
                                                jecPayloads = cms.vstring( payloads ),
                                                removeLooseLep = cms.bool(True)
                                                )
                                            )
process.pfShyftProducerMuLoose.shyftSelection.muonIdTight.cutsToIgnore.append('PFIso')

process.pfShyftProducerEle = cms.EDFilter('EDSHyFTSelector',
                                    shyftSelection = shyftSelectionInput.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        ePlusJets = cms.bool( True ),
        muPlusJets = cms.bool( False ),
        muTrig = cms.string(options.triggerName),
        eleTrig = cms.string(options.triggerName),
        jetPtMin = cms.double(10.0),##30
        eEtCut = cms.double(25.0),##35
        usePFIso = cms.bool(True),
        useVBTFDetIso  = cms.bool(False),
        useWP95Selection = cms.bool(False),
        useWP70Selection = cms.bool(True),

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

        minJets = cms.int32(1),
        metMin = cms.double(0.0),
        muPtMin = cms.double(25.0),#35
        identifier = cms.string('PFEle'),
        cutsToIgnore=cms.vstring( inputCutsToIgnore ),
        useData = cms.bool(useData),
        jetSmear = cms.double(0.0),
        jecPayloads = cms.vstring( payloads )
        )
        )


process.pfShyftProducerEleLoose = process.pfShyftProducerEle.clone(
    shyftSelection = process.pfShyftProducerEle.shyftSelection.clone(
    useWP95Selection = cms.bool(True),# if CiC ID loose, then pf reliso<0.2 is applied
    useWP70Selection = cms.bool(False),
    )
    )

process.pfShyftProducerMetRes090 = process.pfShyftProducerEle.clone(
    shyftSelection = process.pfShyftProducerEle.shyftSelection.clone(
    unclMetScale = cms.double( 0.90 ),
    jetSmear = cms.double(0.01),
    identifier = cms.string('PFMETRES090'),
    )
    )

process.pfShyftProducerMetRes110 = process.pfShyftProducerEle.clone(
    shyftSelection = process.pfShyftProducerEle.shyftSelection.clone(
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

process.pfShyftTupleMETMetRes110 = process.pfShyftTupleMETEle.clone(
    src = cms.InputTag("pfShyftProducerMetRes110", "MET"),
    )

process.pfShyftTupleMETMetRes090 = process.pfShyftTupleMETEle.clone(
    src = cms.InputTag("pfShyftProducerMetRes090", "MET"),
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

process.PUNtupleDumperSingleEle = cms.EDProducer("PileupReweightingPoducer",
                                         FirstTime = cms.untracked.bool(True),
                                         oneDReweighting = cms.untracked.bool(False),        
                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                         PileupDataFile = cms.untracked.string('dataPileupTruth_v2_finebin_160404-167913.root')
)

process.PUNtupleDumperEleHad = cms.EDProducer("PileupReweightingPoducer",
                                         FirstTime = cms.untracked.bool(True),
                                         oneDReweighting = cms.untracked.bool(False),        
                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                         PileupDataFile = cms.untracked.string('dataPileupTruth_v2_finebin_170826-173692.root')
)

process.PUNtupleDumperOld = cms.EDProducer("PUNtupleDumper",
                                           PUscenario = cms.string("42X")
                                           )

if not options.useData:
    process.p0 = cms.Path( process.PUNtupleDumperSingleEle + process.PUNtupleDumperEleHad + process.PUNtupleDumperOld )
else:
    process.p0 = cms.Path( process.patTriggerDefaultSequence )
    
process.p1 = cms.Path(
    process.pfShyftProducerMu*
    process.pfShyftTupleJetsMu*
    process.pfShyftTupleMuons*
    process.pfShyftTupleMETMu
    )

process.p2 = cms.Path(
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
process.p5 = cms.Path()

if options.useLooseElectrons:
    process.p3 = cms.Path(
        process.pfShyftProducerEleLoose*
        process.pfShyftTupleJetsEleLoose*
        process.pfShyftTupleElectronsLoose*
        process.pfShyftTupleMETEleLoose
        )
if options.useLooseMuons :
    process.p4 = cms.Path(
        process.pfShyftProducerMuLoose*
        process.pfShyftTupleJetsMuLoose*
        process.pfShyftTupleMuonsLoose*
        process.pfShyftTupleMETMuLoose
        )        

if options.useMETRes :
    process.p5 = cms.Path(
        process.pfShyftProducerMetRes090*
        process.pfShyftTupleMETMetRes090*
        process.pfShyftProducerMetRes110*
        process.pfShyftTupleMETMetRes110
        )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyftDump.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p1','p2','p3','p4', 'p5') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      #'keep *_*_pileupWeights_*',
                                                                      'keep *_PUNtupleDumperSingleEle_*_*',
                                                                      'keep *_PUNtupleDumperEleHad_*_*',
                                                                      'keep *_PUNtupleDumperOld_*_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_pdfWeightProducer_*_*',
                                                                      'keep PileupSummaryInfos_*_*_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*'
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

