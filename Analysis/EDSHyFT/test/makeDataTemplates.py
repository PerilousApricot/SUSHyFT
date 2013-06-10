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
handle1  = Handle ("std::vector<pat::Muon>")
handle2  = Handle ("std::vector<pat::Jet>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label1 = ("selectedPatMuonsPFlowLoose")
label2 = ("selectedPatJetsPFlowLoose")

f = ROOT.TFile("analyzeMassShapes.root", "RECREATE")
f.cd()

secvtxMass = ROOT.TH1F( 'secvtxMass', 'Secondary Vertex Mass', 100, 0., 10. )

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
    muons = handle1.product()
    jets = handle2.product()
    pairs = []

    # find the muon/jet pairs
    for muon in muons :
        if muon.pt() > 15. and fabs(muon.eta()) < 2.4 :
            for jet in jets :
                if jet.pt() > 25. and fabs(jet.eta()) < 2.4 :
                    if deltaR( muon, jet ) < 0.5 :
                        pairs.append( [muon, jet] )
                        break
    # Now make a dijet selection
    if len(pairs) != 2 :
        continue
    if deltaR( pairs[0][1], pairs[1][1] ) < 3.14159 :
        continue
    # Now require that there be a tag on the "away" side
    if pairs[0][1].bDiscriminator('simpleSecondaryVertexHighEffBJetTags') < 2.34 :
        continue
    # Finally check the vertex mass of the tags
    if pairs[1][1].bDiscriminator('simpleSecondaryVertexHighEffBJetTags') < 2.34 :
        secvtxMass.Fill( pairs[1][1].userFloat('secvtxMass') )
    
f.cd()
secvtxMass.Write()

f.Close()
