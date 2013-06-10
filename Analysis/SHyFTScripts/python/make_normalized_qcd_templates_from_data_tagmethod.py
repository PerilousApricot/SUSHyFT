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

f = TFile('data_15invpb_anashyft_v2.root')

directory = 'pfShyftAnaLooseNoMETWithD0/'
label = 'pf'

ihist = 'Data_muisoVsMET_'


hists = []


stacks = []
legs = []
bins = []
canvs = []

# First get the normalizations from the MET vs ISO sidebands (ABCD)
maxTags = 2

for ijet in range(1,6):
    h_1tag = f.Get( directory + ihist + str(ijet) + 'j_1t' ).Clone()
    h_2tag = f.Get( directory + ihist + str(ijet) + 'j_2t' )    
    h_1tag.SetName( ihist + str(ijet) + 'j_ge1t')
    h_1tag.Add( h_2tag, 1.0)
    hists.append( h_1tag )


#hists[2].Add( hists[3] )
#hists[2].Add( hists[4] )

# REGIONS:
# A = nonisolated, low met
# B = nonisolated, high met
# C = isolated, low met
# D = isolated, high met     <---- SIGNAL REGION

for ijet in range(1,6) :
    c = TCanvas('c_' + str(ijet), 'c_' + str(ijet))
    hists[ijet-1].Draw('box')
    canvs.append(c)
    c.Print( label + '_tag_met_vs_iso_jet_' + str(ijet) + '.png', 'png')
    c.Print( label + '_tag_met_vs_iso_jet_' + str(ijet) + '.pdf', 'pdf')

signalRegion = hists[2].Clone()
signalRegion.SetName('met_vs_iso_3jets')
signalRegion.Add( hists[3] )
signalRegion.Add( hists[4] )
signalRegion.SetTitle('Muon Isolation vs MET, >=3 Jets;MET (GeV/c^{2});Relative Isolation')





preds = []

for ijet in range(1,6) :    
    n_a = hists[ijet-1].Integral(1, 2, 5, 20)
    n_b = hists[ijet-1].Integral(3,20, 5, 20)
    n_c = hists[ijet-1].Integral(1, 2, 1, 1)
    n_d = hists[ijet-1].Integral(3,20, 1, 1)
    n_pred = float( n_b ) * float( n_c ) / float( n_a )
    if n_a > 0 and n_b > 0 and n_c > 0 :
        dn_pred = n_pred * sqrt( 1/n_a + 1/n_b + 1/n_c)
    else :
        dn_pred = 1.0
    print ' ijet = {0:3.0f}, na = {1:4.0f}, nb = {2:4.0f}, nc = {3:4.0f}, nd = {4:4.0f}, n_pred = {5:6.2f} +- {6:6.2f}'.format(
        ijet, n_a, n_b, n_c, n_d, n_pred, dn_pred
        )
    preds.append( n_pred )





# Now make the scaled templates

maxTags = 2
taghists = []
taghists2d = []
taghist = 'Data_secvtxMass_'

for ijet in range(1,6):

    h_1tag = f.Get( directory + taghist + str(ijet) +'j_1t_vs_iso' )
    if ijet >= 2 :
        h_2tag = f.Get( directory + taghist + str(ijet) +'j_2t_vs_iso' )
        h_1tag.Add( h_2tag )

    taghists2d.append( h_1tag )
#    hs = THStack('stack_' + taghist + str(ijet), 'stack_' + taghist + str(ijet))
    h_1tag_proj = h_1tag.ProjectionX( 'proj_' + taghist + str(ijet) + '_1t', 2, h_1tag.GetNbinsX() )
    h_1tag_proj.SetMarkerStyle(20)
    taghists.append( h_1tag_proj )



taghists[2].Add( taghists[3] )
taghists[2].Add( taghists[4] )
taghists[3] = taghists[2].Clone()
taghists[4] = taghists[2].Clone()

taghists[3].SetName( 'proj_Data_secvtxMass_4_1t')
taghists[4].SetName( 'proj_Data_secvtxMass_5_1t')

fout = TFile(label + '_normalized_qcd_templates.root', 'RECREATE')

for ijet in range(1,6) :
    c = TCanvas('c_' + str(ijet), 'c_' + str(ijet))
    taghists[ijet-1].Sumw2()
    taghists[ijet-1].Scale( preds[ijet-1] / taghists[ijet-1].Integral() )
    taghists[ijet-1].Draw('e')
    c.Print( label + '_qcd_normalized_templates_tagmethod_' + str(ijet) + '.png', 'png')
    c.Print( label + '_qcd_normalized_templates_tagmethod_' + str(ijet) + '.pdf', 'pdf')    
    canvs.append(c)



c2d = TCanvas('c2d', 'c2d')
signalRegion.Draw('box')
l = TLine()
l.SetLineWidth(3)
l.SetLineColor(2)

l.DrawLine( 20., 0.00, 20., 0.05 )
l.DrawLine( 20., 0.2, 20., 1.0 )
l.DrawLine( 0., 0.05, 20., 0.05)
l.DrawLine( 0., 0.2, 20., 0.2)
l.DrawLine( 20., 0.05, 200., 0.05 )
l.DrawLine( 20., 0.2, 200., 0.2 )

t = TLatex()
t.SetTextColor(2)
t.DrawLatex( 10., 0.5, 'A')
t.DrawLatex( 60., 0.5, 'B')
t.DrawLatex( 10., 0.0, 'C')
t.DrawLatex( 60., 0.0, 'D')

c2d.Print(label + '_pretty_tag_met_vs_iso_jet_3.png', 'png')
c2d.Print(label + '_pretty_tag_met_vs_iso_jet_3.pdf', 'pdf')

fout.cd()
for ijet in range(1,6):
    taghists[ijet-1].Write()
    


