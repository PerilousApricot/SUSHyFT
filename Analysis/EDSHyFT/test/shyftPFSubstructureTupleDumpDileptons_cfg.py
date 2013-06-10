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
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_116_1_AOE.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_117_1_X0u.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_118_1_oH9.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_119_1_WkG.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_11_1_Lgw.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_120_1_dbd.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_121_1_kcS.root',
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
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = [
        'HLT_IsoMu15_v5',
        'HLT_IsoMu24_v2',
        'HLT_IsoMu24_v4',
        'HLT_IsoMu24_v5',
        'HLT_IsoMu24_v7',
        'HLT_IsoMu24_v8',
        'HLT_IsoMu24_v9',
        ])
    process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  [
        'HLT_Ele45_CaloIdVT_TrkIdT_v1',
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
                                           jetSrc = cms.InputTag('goodPatJetsPFlow'),
                                           muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
                                           removeLooseLep = cms.bool(True),
                                           jecPayloads = cms.vstring( payloads )
                                        )
                                    )

process.pfShyftProducerPrunedCA8 = cms.EDFilter('EDSHyFTPFSelector',
                                            shyftPFSelection = shyftPFSelectionInput.clone(
                                                jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                jecPayloads = cms.vstring( payloads )
                                                )
                                            )

process.pfShyftProducer.shyftPFSelection.cutsToIgnore.append('== 1 Tight Lepton')
process.pfShyftProducer.shyftPFSelection.cutsToIgnore.append('0 other lepton')
process.pfShyftProducer.shyftPFSelection.cutsToIgnore.append('>=1 Jets')

process.pfShyftProducerPrunedCA8.shyftPFSelection.cutsToIgnore.append('== 1 Tight Lepton')
process.pfShyftProducerPrunedCA8.shyftPFSelection.cutsToIgnore.append('0 other lepton')
process.pfShyftProducerPrunedCA8.shyftPFSelection.cutsToIgnore.append('>=1 Jets')


process.pfShyftTupleJetsPrunedCA8 = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerPrunedCA8", "jets"),
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
            tag = cms.untracked.string("tche"),
            quantity = cms.untracked.string("bDiscriminator('trackCountingHighEffBJetTags')")
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
            quantity = cms.untracked.string("bDiscriminator('simpleSecondaryVertexHighEffBJetTags')")
            ),
        cms.PSet(
            tag = cms.untracked.string("tche"),
            quantity = cms.untracked.string("bDiscriminator('trackCountingHighEffBJetTags')")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            )
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
        )  
    )


process.p1 = cms.Path(
    process.hltSelection*
    process.pfShyftProducerPrunedCA8 *
    process.pfShyftTupleJetsPrunedCA8
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
                                                                       'keep *_addPileupInfo_*_*',
                                                                       #'keep *_pfShyftProducer_*_*',
                                                                       'keep double_*_rho_*',
                                                                       'keep *_pfShyftTuple*_*_*'
                                                                       #'keep *_kinFitTtSemiLepEvent_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
