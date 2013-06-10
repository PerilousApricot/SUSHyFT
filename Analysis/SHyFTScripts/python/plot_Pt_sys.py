#!/bin/python



from ROOT import *
from array import *

gROOT.Macro("~/rootlogon.C")

gStyle.SetOptStat(000000)
f = TFile('TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v2.root')

leg = TLegend(0.6, 0.6, 0.84, 0.84)
leg.SetBorderSize(0)
leg.SetFillColor(0)

c1 = TCanvas('c1', 'c1')
#h_njets_1 = f.Get('pfRecoShyftAnaEleEEPt075/nJets')
h_njets_2 = f.Get('pfRecoShyftAna/nJets')
h_njets_3 = f.Get('pfRecoShyftAnaEleEEPt125/nJets')

h_njets_3.SetTitle("NJets, p_{T} > 25 GeV, |#eta| < 2.4;N_{JETS}")

h_njets_3.SetLineColor(4)
h_njets_2.SetLineColor(1)
#h_njets_1.SetLineColor(2)

leg.AddEntry(h_njets_3, 'Pt Up', 'l')
leg.AddEntry(h_njets_2, 'Pt Nominal', 'l')
#leg.AddEntry(h_njets_1, 'Pt Down', 'l')

h_njets_3.Draw('hist')
h_njets_2.Draw('hist same')
#h_njets_1.Draw('hist same')
leg.Draw()
c1.Print('pt_sys_njets_ele.png', 'png')
c1.Print('pt_sys_njets_ele.pdf', 'pdf')

c2 = TCanvas('c2', 'c2')
#h_jet1Pt_1 = f.Get('pfRecoShyftAnaEleEEPt075/jet1Pt')
h_jet1Pt_2 = f.Get('pfRecoShyftAna/jet1Pt')
h_jet1Pt_3 = f.Get('pfRecoShyftAnaEleEEPt125/jet1Pt')

#h_jet1Pt_1.Rebin(5)
h_jet1Pt_2.Rebin(5)
h_jet1Pt_3.Rebin(5)

h_jet1Pt_3.SetTitle("Jet 1 p_{T};p_{T} (GeV/c)")

h_jet1Pt_3.SetLineColor(4)
h_jet1Pt_2.SetLineColor(1)
#h_jet1Pt_1.SetLineColor(2)

h_jet1Pt_3.Draw('hist')
h_jet1Pt_2.Draw('hist same')
#h_jet1Pt_1.Draw('hist same')
leg.Draw()
c2.Print('pt_sys_jet1Pt_ele.png', 'png')
c2.Print('pt_sys_jet1Pt_ele.pdf', 'pdf')


c3 = TCanvas('c3', 'c3')
#h_jet2Pt_1 = f.Get('pfRecoShyftAnaEleEEPt075/jet2Pt')
h_jet2Pt_2 = f.Get('pfRecoShyftAna/jet2Pt')
h_jet2Pt_3 = f.Get('pfRecoShyftAnaEleEEPt125/jet2Pt')

#h_jet2Pt_1.Rebin(5)
h_jet2Pt_2.Rebin(5)
h_jet2Pt_3.Rebin(5)

h_jet2Pt_3.SetLineColor(4)
h_jet2Pt_2.SetLineColor(1)
#h_jet2Pt_1.SetLineColor(2)

h_jet2Pt_3.Draw('hist')
h_jet2Pt_2.Draw('hist same')
#h_jet2Pt_1.Draw('hist same')
leg.Draw()
c3.Print('pt_sys_jet2Pt_ele.png', 'png')
c3.Print('pt_sys_jet2Pt_ele.pdf', 'pdf')

lsc4 = TCanvas('c4', 'c4')
#h_jet3Pt_1 = f.Get('pfRecoShyftAnaEleEEPt075/jet3Pt')
h_jet3Pt_2 = f.Get('pfRecoShyftAna/jet3Pt')
h_jet3Pt_3 = f.Get('pfRecoShyftAnaEleEEPt125/jet3Pt')

#h_jet3Pt_1.Rebin(5)
h_jet3Pt_2.Rebin(5)
h_jet3Pt_3.Rebin(5)

h_jet3Pt_3.SetLineColor(4)
h_jet3Pt_2.SetLineColor(1)
#h_jet3Pt_1.SetLineColor(2)

h_jet3Pt_3.Draw('hist')
h_jet3Pt_2.Draw('hist same')
#h_jet3Pt_1.Draw('hist same')
leg.Draw()
c4.Print('pt_sys_jet3Pt_ele.png', 'png')
c4.Print('pt_sys_jet3Pt_ele.pdf', 'pdf')


c5 = TCanvas('c5', 'c5')
#h_metPt_1 = f.Get('pfRecoShyftAnaEleEEPt075/metPt')
h_metPt_2 = f.Get('pfRecoShyftAna/metPt')
h_metPt_3 = f.Get('pfRecoShyftAnaEleEEPt125/metPt')

#h_metPt_1.Rebin(5)
h_metPt_2.Rebin(5)
h_metPt_3.Rebin(5)

h_metPt_3.SetLineColor(4)
h_metPt_2.SetLineColor(1)
#h_metPt_1.SetLineColor(2)

h_metPt_3.Draw('hist')
h_metPt_2.Draw('hist same')
#h_metPt_1.Draw('hist same')
leg.Draw()
c5.Print('pt_sys_metPt_ele.png', 'png')
c5.Print('pt_sys_metPt_ele.pdf', 'pdf')

c5 = TCanvas('c6', 'c6')
#h_metPt_1 = f.Get('pfRecoShyftAnaEleEEPt075/metPt')
h_metPt_2 = f.Get('pfRecoShyftAna/ePt')
h_metPt_3 = f.Get('pfRecoShyftAnaEleEEPt125/ePt')

#h_metPt_1.Rebin(5)
h_metPt_2.Rebin(5)
h_metPt_3.Rebin(5)

h_metPt_3.SetLineColor(4)
h_metPt_2.SetLineColor(1)
#h_metPt_1.SetLineColor(2)

h_metPt_3.Draw('hist')
h_metPt_2.Draw('hist same')
#h_metPt_1.Draw('hist same')
leg.Draw()
c5.Print('pt_sys_ePt_ele.png', 'png')
c5.Print('pt_sys_ePt_ele.pdf', 'pdf')
