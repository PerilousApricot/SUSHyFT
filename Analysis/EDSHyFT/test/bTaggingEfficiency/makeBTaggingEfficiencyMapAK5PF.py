#!/usr/bin/env python

import os, sys
from ROOT import gROOT, TFile, TH2D
from array import array

gROOT.SetBatch(1)

#----------------------------------------------------------------------------------
# Configurable parameters

datasets = [
  # Background
  [
    '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/jpilot-TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10-fe5dcf8cf2a24180bf030f68a7d97dda/USER', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'
  ],
  [
    '/TT_8TeV-mcatnlo/galank-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/TT_CT10_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/bazterra-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 240., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/agarabed-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/dsperka-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 240., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/mmhl-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/mmhl-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/WW_TuneZ2star_8TeV_pythia6_tauola/mmhl-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/WZ_TuneZ2star_8TeV_pythia6_tauola/bcalvert-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/ZZ_TuneZ2star_8TeV_pythia6_tauola/mmhl-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/TTWJets_8TeV-madgraph/mgabusi-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/TTZJets_8TeV-madgraph_v2/mgabusi-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-20to30_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-30to50_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-80to120_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 140., 180., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 140., 180., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 140., 180., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 550., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 550., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 550., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 600., 700., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 600., 700., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 600., 700., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-600to800_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-800to1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 950., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 950., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 950., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 20., 40., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 20., 40., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 20., 40., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_20_30_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_80_170_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_170_250_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_250_350_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_350_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_20_30_BCtoE_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_30_80_BCtoE_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/QCD_Pt_350_BCtoE_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/GJets_HT-200To400_8TeV-madgraph/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/GJets_HT-400ToInf_8TeV-madgraph/cjenkins-GJets_HT-400ToInf_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 450.,1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 250., 300., 350., 450.,1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 250., 300., 400., 500., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  # Signal
  # BprimeBprimeToBHBHinc
  [
    '/BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-850_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-850_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-900_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-900_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-950_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-950_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-1000_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-1000_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 550., 700., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-1100_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-1100_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-1200_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-1200_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-1300_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-1300_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-1400_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-1400_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-1500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-1500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  # BprimeBprimeToBHBZinc
  [
    '/BprimeBprimeToBHBZinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_A-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-850_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-850_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-900_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-900_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-950_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-950_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-1000_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-1000_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 550., 700., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-1100_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-1100_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-1200_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-1200_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-1300_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-1300_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-1400_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-1400_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBZinc_M-1500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-1500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  # BprimeBprimeToBHTWinc
  [
    '/BprimeBprimeToBHTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-900_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-900_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBHTWinc_M-1500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-1500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  # BprimeBprimeToBZBZinc
  [
    '/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-900_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-900_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-950_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-950_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-1100_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-1100_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-1200_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-1200_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZBZinc_M-1500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-1500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  # BprimeBprimeToBZTWinc
  [
    '/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_A-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_A-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-900_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-900_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-950_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-950_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-1000_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1000_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 550., 700., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-1100_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1100_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-1200_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1200_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-1300_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1300_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-1400_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1400_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-1500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  # BprimeBprimeToTWTWinc
  [
    '/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_B-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_B-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-850_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-850_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-900_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-900_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-950_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-950_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 600., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-1000_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-1000_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 550., 700., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-1100_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-1100_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-1200_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-1200_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-1300_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-1300_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-1400_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-1400_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-1500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-1500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 500., 600., 700., 800., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'AK5PF_CSVM'
  ]
]

pathToInputFiles = 'CRAB_Jobs'
inputFileSubdirectory = 'bTaggingEffAnalyzerAK5PF'
outputFileSuffix = 'bTaggingEfficiencyMap'

#----------------------------------------------------------------------------------

def produceEfficiencyMaps(dataset, inputPath, subdirectory, suffix):

  inputFilename = os.path.join(inputPath, dataset[0].lstrip('/').replace('/','__') + '.root')
  inputFile = TFile(inputFilename, 'READ')

  outputFilename = dataset[0].split('/')[1] + '_' + dataset[2] + '_' + suffix + '.root'
  outputFile = TFile(outputFilename, 'RECREATE')

  for partonFlavor in ['b', 'c', 'udsg']:

    denominatorHisto = subdirectory + '/h2_BTaggingEff_Denom_' + partonFlavor
    numeratorHisto = subdirectory + '/h2_BTaggingEff_Num_' + partonFlavor

    denominatorIn = inputFile.Get(denominatorHisto)
    numeratorIn = inputFile.Get(numeratorHisto)

    xShift = denominatorIn.GetXaxis().GetBinWidth(1)/2.
    yShift = denominatorIn.GetYaxis().GetBinWidth(1)/2.

    binsX = array('d', dataset[1][partonFlavor][0])
    binsY = array('d', dataset[1][partonFlavor][1])

    denominatorOut = TH2D('denominator_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
    numeratorOut   = TH2D('numerator_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
    efficiencyOut  = TH2D('efficiency_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)

    # loop over all bins
    for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
      for j in range(1,denominatorOut.GetYaxis().GetNbins()+1):

        binXMin = denominatorIn.GetXaxis().FindBin(denominatorOut.GetXaxis().GetBinLowEdge(i)+xShift)
        binXMax = denominatorIn.GetXaxis().FindBin(denominatorOut.GetXaxis().GetBinUpEdge(i)-xShift)
        binYMinPos = denominatorIn.GetYaxis().FindBin(denominatorOut.GetYaxis().GetBinLowEdge(j)+yShift)
        binYMaxPos = denominatorIn.GetYaxis().FindBin(denominatorOut.GetYaxis().GetBinUpEdge(j)-yShift)
        binYMinNeg = denominatorIn.GetYaxis().FindBin(-denominatorOut.GetYaxis().GetBinUpEdge(j)+yShift)
        binYMaxNeg = denominatorIn.GetYaxis().FindBin(-denominatorOut.GetYaxis().GetBinLowEdge(j)-yShift)

        denominator = denominatorIn.Integral(binXMin,binXMax,binYMinPos,binYMaxPos)
        denominator = denominator + denominatorIn.Integral(binXMin,binXMax,binYMinNeg,binYMaxNeg)
        numerator = numeratorIn.Integral(binXMin,binXMax,binYMinPos,binYMaxPos)
        numerator = numerator + numeratorIn.Integral(binXMin,binXMax,binYMinNeg,binYMaxNeg)

        if(i==denominatorOut.GetXaxis().GetNbins()): # also add overflow to the last bin in jet pT
          denominator = denominator + denominatorIn.Integral(binXMax+1,denominatorIn.GetXaxis().GetNbins()+1,binYMinPos,binYMaxPos)
          denominator = denominator + denominatorIn.Integral(binXMax+1,denominatorIn.GetXaxis().GetNbins()+1,binYMinNeg,binYMaxNeg)
          numerator = numerator + numeratorIn.Integral(binXMax+1,numeratorIn.GetXaxis().GetNbins()+1,binYMinPos,binYMaxPos)
          numerator = numerator + numeratorIn.Integral(binXMax+1,numeratorIn.GetXaxis().GetNbins()+1,binYMinNeg,binYMaxNeg)

        denominatorOut.SetBinContent(i,j,denominator)
        numeratorOut.SetBinContent(i,j,numerator)
        if(denominator>0.): efficiencyOut.SetBinContent(i,j,numerator/denominator)

    # check if there are any bins with 0 or 100% efficiency
    for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
      for j in range(1,denominatorOut.GetYaxis().GetNbins()+1):

        efficiency = efficiencyOut.GetBinContent(i,j)
        if(efficiency==0. or efficiency==1.):
          print 'Warning! Bin(%i,%i) for %s jets has a b-tagging efficiency of %.3f'%(i,j,partonFlavor,efficiency)

    # set efficiencies in overflow bins
    for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
      efficiencyOut.SetBinContent(i, denominatorOut.GetYaxis().GetNbins()+1, efficiencyOut.GetBinContent(i, denominatorOut.GetYaxis().GetNbins()))

    for j in range(1,denominatorOut.GetYaxis().GetNbins()+2):
      efficiencyOut.SetBinContent(denominatorOut.GetXaxis().GetNbins()+1, j, efficiencyOut.GetBinContent(denominatorOut.GetXaxis().GetNbins(), j))

    outputFile.cd()

    denominatorOut.Write()
    numeratorOut.Write()
    efficiencyOut.Write()

  outputFile.Close()

  print '-------------------------------------------------------------------------------------------'
  print 'b-tagging efficiency map for'
  print dataset[0]
  print 'successfully created and stored in %s'%outputFilename
  print ''


def main():

  for dataset in datasets:
    produceEfficiencyMaps(dataset, pathToInputFiles, inputFileSubdirectory, outputFileSuffix)

if __name__ == "__main__":
  main()
