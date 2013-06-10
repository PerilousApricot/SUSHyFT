import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('ignoreTrigger',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('muOrEle',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use muons (0) or electrons (1)")


options.register('useData',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use data (1) or MC (0)")



options.parseArguments()

print options

import sys

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'file:///uscms/home/pilot/data/Zprime8TeV/CMSSW_5_2_4/src/TopQuarkAnalysis/TopPairBSM/test/ttbsm_52x_data.root'
#'dcap:///pnfs/cms/WAX/11/store/user/pilot/SingleMu/SingleMu_Run2012A/82fd51e0af07726fb8b1875f5746f193/ttbsm_52x_data_1_1_7O8.root'
#'dcap:///pnfs/cms/WAX/11/store/user/pilot/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/WJetsToLNu_8TeV/8f2c5ea1c4172ee3e54a11c7e5d6a05d/ttbsm_52x_mc_1_1_JUZ.root'
)
)

payloadsData = [
    'Jec11_V3_L1FastJet_AK5PFchs.txt',
    'Jec11_V3_L2Relative_AK5PFchs.txt',
    'Jec11_V3_L3Absolute_AK5PFchs.txt',
    'Jec11_V3_L2L3Residual_AK5PFchs.txt',
    'Jec11_V3_Uncertainty_AK5PFchs.txt'
                ]

payloadsMC = [
    'Jec11_V3_L1FastJet_AK5PFchs.txt',
    'Jec11_V3_L2Relative_AK5PFchs.txt',
    'Jec11_V3_L3Absolute_AK5PFchs.txt',
    'Jec11_V3_Uncertainty_AK5PFchs.txt'
]

if options.useData :
    payloads = payloadsData
else :
    payloads = payloadsMC


## process.source = cms.Source("PoolSource",
##                             fileNames = cms.untracked.vstring(
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_10_1_5eL.root',
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_11_1_y36.root',
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_12_1_RFD.root'

## )
## )



from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if options.ignoreTrigger :
    process.hltSelection = cms.Sequence()
else :
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = ['HLT_Mu40_eta2p1_v1',
                                                                                                       'HLT_Mu40_eta2p1_v2',
                                                                                                       'HLT_Mu40_eta2p1_v3',
                                                                                                       'HLT_Mu40_eta2p1_v4',
                                                                                                       'HLT_Mu40_eta2p1_v5',
                                                                                                       'HLT_Mu40_eta2p1_v6',
                                                                                                       'HLT_Mu40_eta2p1_v7',
                                                                                                       'HLT_Mu40_eta2p1_v8',
                                                                                                       'HLT_Mu40_eta2p1_v9',
                                                                                                       ])
    process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  ['HLT_Ele45_CaloIdVT_TrkIdT_v1',
                                                                                                         'HLT_Ele45_CaloIdVT_TrkIdT_v2',
                                                                                                         'HLT_Ele45_CaloIdVT_TrkIdT_v3',
                                                                                                         'HLT_Ele52_CaloIdVT_TrkIdT_v1',
                                                                                                         'HLT_Ele52_CaloIdVT_TrkIdT_v2',
                                                                                                         'HLT_Ele65_CaloIdVT_TrkIdT_v1',
                                                                                                         'HLT_Ele25_WP80_PFMT40_v2'
                                                                                                         ])
    process.hltSelectionMu.throw = False
    process.hltSelectionEle.throw = False

    if options.muOrEle :
        process.hltSelection = cms.Sequence( ~process.hltSelectionMu * process.hltSelectionEle )
    else :
        process.hltSelection = cms.Sequence( process.hltSelectionMu )


## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.SHyFT.shyftPFSelection_cfi import shyftPFSelection as shyftPFSelectionInput



process.pfShyftProducer = cms.EDFilter('EDSHyFTPFSelector',
                                    shyftPFSelection = shyftPFSelectionInput.clone(
                                           jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                           jecPayloads = cms.vstring( payloads )
                                        )
                                    )

process.pfShyftProducerLoose = cms.EDFilter('EDSHyFTPFSelector',
                                            shyftPFSelection = shyftPFSelectionInput.clone(
                                                jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
                                                electronSrc = cms.InputTag('selectedPatElectronsLoosePFlow'),
                                                jecPayloads = cms.vstring( payloads ),
                                                removeLooseLep = cms.bool(True)
                                                )
                                            )

process.pfShyftProducerLoose.shyftPFSelection.cutsToIgnore.append('== 1 Tight Lepton')
process.pfShyftProducerLoose.shyftPFSelection.cutsToIgnore.append('0 other lepton')
process.pfShyftProducerLoose.shyftPFSelection.cutsToIgnore.append('>=1 Jets')
process.pfShyftProducerLoose.shyftPFSelection.muonIdPFTight.cutsToIgnore.append('PFIso')
process.pfShyftProducerLoose.shyftPFSelection.electronIdPFTight.cutsToIgnore.append('PFIso')


## std sequence to produce the kinematic fit for semi-leptonic events
process.load('TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi')

process.kinFitTtSemiLepEvent.jets = cms.InputTag("pfShyftProducer", "jets")
process.kinFitTtSemiLepEvent.mets = cms.InputTag("pfShyftProducer", "MET")
process.kinFitTtSemiLepEvent.leps = cms.InputTag("pfShyftProducer", "muons")

process.load("TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi")



process.pfShyftTupleJets = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "jets"),
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
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Pt"),
            quantity = cms.untracked.string("daughter(0).pt()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Eta"),
            quantity = cms.untracked.string("daughter(0).eta()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Phi"),
            quantity = cms.untracked.string("daughter(0).phi()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Mass"),
            quantity = cms.untracked.string("daughter(0).mass()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Pt"),
            quantity = cms.untracked.string("daughter(1).pt()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Eta"),
            quantity = cms.untracked.string("daughter(1).eta()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Phi"),
            quantity = cms.untracked.string("daughter(1).phi()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Mass"),
            quantity = cms.untracked.string("daughter(1).mass()")
            ),
        )  
    )

process.pfShyftTupleJetsLoose = process.pfShyftTupleJets.clone(
    src = cms.InputTag("pfShyftProducerLoose", "jets"),
    )



process.pfShyftTupleJetsLooseTopTag = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("goodPatJetsCATopTagPF"),
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
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("nSubjets"),
            quantity = cms.untracked.string("numberOfDaughters()")
            ),
        cms.PSet(
            tag = cms.untracked.string("minMass"),
            quantity = cms.untracked.string("? hasTagInfo('CATop') ? tagInfo('CATop').properties().minMass : 0.0")
            ),
        cms.PSet(
            tag = cms.untracked.string("topMass"),
            quantity = cms.untracked.string("? hasTagInfo('CATop') ? tagInfo('CATop').properties().topMass : 0.0")
            ),
	cms.PSet(
	    tag = cms.untracked.string("ssvhe"),
	    quantity = cms.untracked.string("bDiscriminator('combinedSecondaryVertexBJetTags')")
            ),
        )
    )


process.pfShyftTupleMuons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "muons"),
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
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
	cms.PSet(
            tag = cms.untracked.string("pfisoPU"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "max(0.0,  userIsolation('pat::PfNeutralHadronIso') + userIsolation('pat::PfGammaIso') - 0.5 * userIsolation('pat::TrackIso') )"
                                            )
            ),
        )  
    )

process.pfShyftTupleMuonsLoose = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerLoose", "muons"),
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
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPU"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "max(0.0,  userIsolation('pat::PfNeutralHadronIso') + userIsolation('pat::PfGammaIso') - 0.5 * userIsolation('pat::TrackIso') )"
                                            )
            ), 
        )
    )

process.pfShyftTupleMET = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "MET"),
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

process.pfShyftTupleMETLoose = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerLoose", "MET"),
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


process.pfShyftTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "electrons"),
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
            quantity = cms.untracked.string("userIsolation('PfAllParticleIso')")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )  
    )

process.pfShyftTupleElectronsLoose = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerLoose", "electrons"),
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
            quantity = cms.untracked.string("userIsolation('PfAllParticleIso')")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )  
    )

process.p1 = cms.Path(
    process.hltSelection*
    process.pfShyftProducerLoose *
    process.pfShyftTupleJetsLoose*
    process.pfShyftTupleJetsLooseTopTag*
    process.pfShyftTupleMuonsLoose*
    process.pfShyftTupleElectronsLoose*
    process.pfShyftTupleMETLoose
    )

process.p2 = cms.Path(
    process.hltSelection*
    process.pfShyftProducer*
    process.pfShyftTupleJets*
    process.pfShyftTupleMuons*
    process.pfShyftTupleElectrons*
    process.pfShyftTupleMET
    )


process.MessageLogger.cerr.FwkReport.reportEvery = 1000




process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyft_ultraslim.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p1', 'p2') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      #'keep *_pfShyftProducer_*_*',
                                                                      'keep double_*_rho_*',
                                                                      'keep *_pfShyftTuple*_*_*'
                                                                      #'keep *_kinFitTtSemiLepEvent_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
