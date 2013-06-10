#! /usr/bin/env python


from optparse import OptionParser


parser = OptionParser()


# Option to just print out the pre-fit numbers
parser.add_option('--doMC', action='store_true',
                  default=False,
                  dest='doMC',
                  help='use MC')



(options, args) = parser.parse_args()

argv = []


import ROOT
import sys
from DataFormats.FWLite import Events, Handle

if options.doMC :
    files = [
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_10_1_ejB.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_11_1_rzB.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_12_1_HJd.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_13_1_DUs.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_14_1_9yj.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_15_1_GWC.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_16_1_wMP.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_17_1_b2E.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_18_1_sOT.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_19_1_RBT.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_1_1_KqE.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_20_1_801.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_21_1_D91.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_22_1_nNs.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_23_1_kMl.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_24_1_j4z.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_25_1_yFo.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_26_1_NFU.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_27_1_H2Y.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_28_1_N5E.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_29_1_MhK.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_2_1_PhR.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_30_1_lBF.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_31_1_2ew.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_32_1_MUB.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_33_1_sa2.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_34_1_Z7c.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_35_1_PmE.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_36_1_jLu.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_37_1_eg6.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_38_1_huP.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_39_1_0rs.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_3_1_YcY.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_40_1_mv2.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_41_1_wpS.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_42_1_I7K.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_43_1_pjx.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_44_1_ptI.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_45_1_ry5.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_46_1_WnC.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_47_1_zHT.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_48_1_SQc.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_49_1_9it.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_4_1_Flk.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_50_1_oUN.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_51_1_iGj.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_5_1_idD.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_6_1_IiF.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_7_1_Ku5.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_8_1_pmM.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_singlemuonInJet_387_v2/res/muonInJet_9_1_4Wy.root'

        ]
else :
    files = [
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_10_1_nE5.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_1_1_xKZ.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_2_1_5KI.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_3_1_RMe.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_4_1_p0T.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_5_1_HVI.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_6_1_2v6.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_7_1_XoF.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_8_1_S9s.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_9_1_1JL.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_1_1_qZV.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_2_1_JFY.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_3_1_y0P.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_4_1_9GO.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_5_1_dsU.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_1_1_WTq.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_2_1_mKs.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_3_1_loE.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_4_1_XkB.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_5_1_Gkh.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_6_1_nES.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_7_1_ZVt.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_8_1_4mi.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_9_1_xkV.root',


        ]

    
events = Events (files)
secvtxMassH  = Handle ("std::vector<float>")

jetPtH  = Handle("std::vector<float>")
jetEtaH = Handle("std::vector<float>")
jetPhiH = Handle("std::vector<float>")

muonPtH  = Handle("std::vector<float>")
muonEtaH = Handle("std::vector<float>")
muonPhiH = Handle("std::vector<float>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label1 = ("jetsDump", "jetSecvtxMass")

jetPtLabel  = ("jetsDump", "jetPt")
jetEtaLabel = ("jetsDump", "jetEta")
jetPhiLabel = ("jetsDump", "jetPhi")

muonPtLabel  = ("muonsDump", "muonPt")
muonEtaLabel = ("muonsDump", "muonEta")
muonPhiLabel = ("muonsDump", "muonPhi")


if options.doMC :
    f = ROOT.TFile("plotSingleMuonInJetMC.root", "RECREATE")
else :
    f = ROOT.TFile("plotSingleMuonInJetData.root", "RECREATE")
f.cd()


secvtxMass = ROOT.TH1F("secvtxMass","secvtxMass",   100, 0.0,  10.0 )


# loop over events
i = 0
for event in events:
    i = i + 1
    if i % 1000 == 0 :
        print i

    index_jet = 0

    event.getByLabel (muonPtLabel,  muonPtH)
    event.getByLabel (muonEtaLabel, muonEtaH)
    event.getByLabel (muonPhiLabel, muonPhiH)

    muPt  = muonPtH.product()[0]
    muEta = muonEtaH.product()[0]
    muPhi = muonPhiH.product()[0]

    muP = ROOT.TVector3()
    muP.SetPtEtaPhi( muPt, muEta, muPhi )


    event.getByLabel (jetPtLabel,  jetPtH)
    event.getByLabel (jetEtaLabel, jetEtaH)
    event.getByLabel (jetPhiLabel, jetPhiH)

    
    jetsPt  = jetPtH.product()
    jetsEta = jetEtaH.product()
    jetsPhi = jetPhiH.product()

    theJet = -1

    if len(jetsPt) != 2:
        continue

    for ijet in range(0, len(jetsPt)) :
        jetP = ROOT.TVector3()
        jetP.SetPtEtaPhi( jetsPt[ijet], jetsEta[ijet], jetsPhi[ijet])
        if jetP.DeltaR( muP ) < 0.5 :
            theJet = 1 - ijet
            break

    if theJet == -1 :
        continue
    
    # use getByLabel, just like in cmsRun
    event.getByLabel (label1, secvtxMassH)

    # get the product
    mass =secvtxMassH.product()[theJet]
    secvtxMass.Fill( mass )



f.cd()

secvtxMass.Write()

f.Close()
