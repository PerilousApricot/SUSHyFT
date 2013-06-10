#!/bin/python



from ROOT import *
from array import *

gROOT.Macro("~/rootlogon.C")

gStyle.SetOptStat(000000)
f = TFile('TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v1.root')

leg = TLegend(0.6, 0.6, 0.84, 0.84)
leg.SetBorderSize(0)
leg.SetFillColor(0)

c1 = TCanvas('c1', 'c1')
h_njets_1 = f.Get('pfRecoShyftAnaMETRES090/nJets')
h_njets_2 = f.Get('pfRecoShyftAna/nJets')
h_njets_3 = f.Get('pfRecoShyftAnaMETRES110/nJets')

h_njets_3.SetTitle("NJets, p_{T} > 25 GeV, |#eta| < 2.4;N_{JETS}")

h_njets_3.SetLineColor(4)
h_njets_2.SetLineColor(1)
h_njets_1.SetLineColor(2)

leg.AddEntry(h_njets_3, '0.9', 'l')
leg.AddEntry(h_njets_2, '1.0', 'l')
leg.AddEntry(h_njets_1, '1.1', 'l')

h_njets_3.Draw('hist')
h_njets_2.Draw('hist same')
h_njets_1.Draw('hist same')
leg.Draw()
c1.Print('unclmet_sys_njets_ele.png', 'png')
c1.Print('unclmet_sys_njets_ele.pdf', 'pdf')


c5 = TCanvas('c5', 'c5')
h_metPt_1 = f.Get('pfRecoShyftAnaMETRES090/metPt')
h_metPt_2 = f.Get('pfRecoShyftAna/metPt')
h_metPt_3 = f.Get('pfRecoShyftAnaMETRES110/metPt')

h_metPt_1.Rebin(5)
h_metPt_2.Rebin(5)
h_metPt_3.Rebin(5)

h_metPt_3.SetLineColor(4)
h_metPt_2.SetLineColor(1)
h_metPt_1.SetLineColor(2)

h_metPt_3.Draw('hist')
h_metPt_2.Draw('hist same')
h_metPt_1.Draw('hist same')
leg.Draw()
c5.Print('unclmet_sys_metPt_ele.png', 'png')
c5.Print('unclmet_sys_metPt_ele.pdf', 'pdf')
