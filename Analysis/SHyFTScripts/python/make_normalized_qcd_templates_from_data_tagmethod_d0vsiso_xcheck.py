#!/bin/python


# ===================================================
#             make_plots.py
#
#  Simple script to plot a stitched distribution
# ===================================================
# ===================================================

from ROOT import *
from array import *

gROOT.Macro("rootlogon.C")


from sys import argv

f = TFile('data_anashyft_15pb_v1.root')

directory = 'pfShyftAnaLooseNoMET/'
label = 'pf'

ihist = 'Data_muisoVsD0_'


hists = []


stacks = []
legs = []
bins = []
canvs = []

# First get the normalizations from the MET vs ISO sidebands (ABCD)
maxTags = 2

for ijet in range(1,6):

    h_all = f.Get( directory + ihist + str(ijet) + 'j' )
    h_0tag = f.Get( directory + ihist + str(ijet) +'j_0t' )
    h_1tag = h_all.Clone()
    h_1tag.SetName( ihist + str(ijet) + 'j_ge1t')
    h_1tag.Add( h_0tag, -1.0)
    hists.append( h_1tag )


#hists[2].Add( hists[3] )
#hists[2].Add( hists[4] )

# REGIONS:
# A = nonisolated, high d0
# B = nonisolated, low d0
# C = isolated, high d0
# D = isolated, low d0     <---- SIGNAL REGION



preds = []

for ijet in range(1,6) :
    bin_xmin = 1
    bin_ymin = 1
    bin_xmax = hists[ijet-1].GetXaxis().FindBin(0.2)
    bin_ymax = hists[ijet-1].GetYaxis().FindBin(1.0)
    bin_d0high = hists[ijet-1].GetXaxis().FindBin(0.04)
    bin_d0low = hists[ijet-1].GetXaxis().FindBin(0.02)
    bin_isohigh = hists[ijet-1].GetYaxis().FindBin(0.20)
    bin_isolow = hists[ijet-1].GetYaxis().FindBin(0.05)
    n_a = hists[ijet-1].Integral(bin_d0high, bin_xmax, bin_isohigh, bin_ymax)
    n_b = hists[ijet-1].Integral(bin_xmin, bin_d0low, bin_isohigh, bin_ymax )
    n_c = hists[ijet-1].Integral(bin_d0high, bin_xmax, bin_ymin, bin_isolow)
    n_d = hists[ijet-1].Integral(bin_xmin, bin_d0low, bin_ymin, bin_isolow)
    n_pred = float( n_b ) * float( n_c ) / float( n_a )
    if n_a > 0 and n_b > 0 and n_c > 0 :
        dn_pred = n_pred * sqrt( 1/n_a + 1/n_b + 1/n_c)
    else :
        dn_pred = 1.0
    print ' ijet = {0:3.0f}, na = {1:4.0f}, nb = {2:4.0f}, nc = {3:4.0f}, nd = {4:4.0f}, n_pred = {5:6.2f} +- {6:6.2f}'.format(
        ijet, n_a, n_b, n_c, n_d, n_pred, dn_pred
        )
    preds.append( n_pred )
    c = TCanvas('c_' + str(ijet), 'c_' + str(ijet))
    hists[ijet-1].Draw('box')

    l = TLine()
    l.SetLineWidth(3)
    l.SetLineColor(2)

    l.DrawLine( 0.00, 0.05, 0.02, 0.05 )
    l.DrawLine( 0.02, 0.00, 0.02, 0.05 )
    l.DrawLine( 0.00, 0.20, 0.02, 0.20 )
    l.DrawLine( 0.02, 0.20, 0.02, 1.00 )
    l.DrawLine( 0.04, 0.00, 0.04, 0.05 )
    l.DrawLine( 0.04, 0.05, 0.2,  0.05 )
    l.DrawLine( 0.04, 0.20, 0.2,  0.20 )
    l.DrawLine( 0.04, 0.20, 0.04, 1.00 )

    canvs.append(c)
    c.Print( label + '_tag_d0_vs_iso_jet_' + str(ijet) + '.png', 'png')
    c.Print( label + '_tag_d0_vs_iso_jet_' + str(ijet) + '.pdf', 'pdf')

