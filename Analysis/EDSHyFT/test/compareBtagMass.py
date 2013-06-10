#! /usr/bin/env python

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

#files = ["shyft_386_mc.root"]
files = [
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_10_1_NYm.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_11_1_e8E.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_12_1_W3U.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_13_1_vTY.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_14_1_JXB.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_15_1_8Qg.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_16_1_Bmu.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_17_1_Kto.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_18_1_7pN.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_19_1_ryq.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_1_1_RWA.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_2_1_3wL.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_3_1_NHb.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_4_1_jAW.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_5_1_13H.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_6_1_ZWP.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_7_1_2sL.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_8_1_ZLD.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1_btagsys/da0889d1ba54331e2d04f67d29ced953/shyft_386_mc_9_1_644.root',
    
    ]
events = Events (files)
handle1  = Handle ("std::vector<pat::Jet>")
handle2  = Handle ("std::vector<pat::Jet>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label1 = ("selectedPatJetsPFlow")
label2 = ("selectedPatJets")

f = ROOT.TFile("analyzeMassShapes.root", "RECREATE")
f.cd()


secvtxMassB1 = ROOT.TH1F("secvtxMassB1","secvtxMassB, Unsmeared",   100, 0.0,  10.0 )
secvtxMassC1 = ROOT.TH1F("secvtxMassC1","secvtxMassC, Unsmeared",   100, 0.0,  10.0 )
secvtxMassP1 = ROOT.TH1F("secvtxMassP1","secvtxMassP, Unsmeared",   100, 0.0,  10.0 ) 

secvtxMassB2 = ROOT.TH1F("secvtxMassB2","secvtxMassB, Smeared",   100, 0.0,  10.0 )
secvtxMassC2 = ROOT.TH1F("secvtxMassC2","secvtxMassC, Smeared",   100, 0.0,  10.0 )
secvtxMassP2 = ROOT.TH1F("secvtxMassP2","secvtxMassP, Smeared",   100, 0.0,  10.0 ) 

secvtxMassB = [ secvtxMassB1, secvtxMassB2]
secvtxMassC = [ secvtxMassC1, secvtxMassC2]
secvtxMassP = [ secvtxMassP1, secvtxMassP2]

# loop over events
i = 0
for event in events:
    i = i + 1
    if i % 1000 == 0 :
        print i
    # use getByLabel, just like in cmsRun
    event.getByLabel (label1, handle1)
    event.getByLabel (label2, handle2)
    # get the product
    jets1 = handle1.product()
    jets2 = handle2.product()

    ijetcoll = -1
    for jetcoll in [jets1, jets2] :
        ijetcoll = ijetcoll + 1
        for jet in jetcoll :
            if jet.userFloat('secvtxMass') > 0.0 and jet.bDiscriminator('simpleSecondaryVertexHighEffBJetTags') :
                if abs(jet.partonFlavour()) == 5 :
                    secvtxMassB[ijetcoll].Fill( jet.userFloat('secvtxMass') )
                elif abs(jet.partonFlavour()) == 4 :
                    secvtxMassC[ijetcoll].Fill( jet.userFloat('secvtxMass') )
                else :
                    secvtxMassP[ijetcoll].Fill( jet.userFloat('secvtxMass') )

f.cd()

secvtxMassB1.Write()
secvtxMassC1.Write()
secvtxMassP1.Write()
secvtxMassB2.Write()
secvtxMassC2.Write()
secvtxMassP2.Write()

f.Close()
