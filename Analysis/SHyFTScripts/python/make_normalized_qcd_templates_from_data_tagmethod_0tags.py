#!/bin/python


from ROOT import *
from array import *

gROOT.Macro("rootlogon.C")


from sys import argv

f = TFile('data_anashyft_15pb_v1.root')
label = 'jpt'

# First get normalization from MET vs ISO
normdirectory = label + 'ShyftAnaLooseNoMETWithD0/'
norms = []
normhist = 'Data_muisoVsMET_'

for ijet in range(1,6):
    h_0tag = f.Get( normdirectory + normhist + str(ijet) +'j_0t' )
    n_a = h_0tag.Integral(1, 2, 5, 20)
    n_b = h_0tag.Integral(3,20, 5, 20)
    n_c = h_0tag.Integral(1, 2, 1, 1)
    n_d = h_0tag.Integral(3,20, 1, 1)
    n_pred = float( n_b ) * float( n_c ) / float( n_a )
    if n_a > 0 and n_b > 0 and n_c > 0 :
        dn_pred = n_pred * sqrt( 1/n_a + 1/n_b + 1/n_c)
    else :
        n_pred = 1.0
        dn_pred = 1.0
    print ' ijet = {0:3.0f}, na = {1:8.0f}, nb = {2:8.0f}, nc = {3:8.0f}, nd = {4:8.0f}, n_pred = {5:6.2f} +- {6:6.2f}'.format(
        ijet, n_a, n_b, n_c, n_d, n_pred, dn_pred
        )
    norms.append( n_pred )
    

# Shape for muon eta will come from the
# high-MET, iso > 0.2 region.
# Normalization will come from the
# MET vs ISO plane. Here we just make the
# templates. 
directory = label + 'ShyftAnaLooseWithD0/'
ihist = 'Data_muisoVsMuEta_'


hists = []
projs = []

stacks = []
legs = []
bins = []
canvs = []

# First get the normalizations from the MET vs ISO sidebands (ABCD)
maxTags = 2

for ijet in range(1,6):
    h_0tag = f.Get( directory + ihist + str(ijet) +'j_0t' )
    h_0tag.SetName('mueta_vs_iso_' + str(ijet) + 'jets')
    hists.append( h_0tag )
    c = TCanvas('c_' + str(ijet), 'c_' + str(ijet))
    h_0tag.Draw('box')
    canvs.append(c)
    c.Print( label + '_0tag_mueta_vs_iso_jet_' + str(ijet) + '.png', 'png')
    c.Print( label + '_0tag_mueta_vs_iso_jet_' + str(ijet) + '.pdf', 'pdf')
    h_0tag_proj = h_0tag.ProjectionX( 'proj_Data_muEta_QCD_' + str(ijet) + '_0t', 2, h_0tag.GetNbinsX() )
    projs.append( h_0tag_proj )


projs[2].Add( projs[3] )
projs[2].Add( projs[4] )
projs[3] = projs[2].Clone()
projs[4] = projs[2].Clone()

projs[3].SetName( 'proj_Data_muEta_QCD_4_0t')
projs[4].SetName( 'proj_Data_muEta_QCD_5_0t')

fout = TFile(label + '_0tag_scaled_qcd_templates.root', 'RECREATE')

ijet = 0
for iproj in range(0,len(projs)):
    proj = projs[iproj]
    ijet = ijet + 1
    proj.Sumw2()
    proj.Scale( norms[iproj] / proj.Integral() )
    c2 = TCanvas('c2_' + str(ijet), 'c2_' + str(ijet))
    proj.SetMarkerStyle(20)
    proj.Draw('e')
    c2.Print( label + '_0tag_mueta_qcd_jet_' + str(ijet) + '.png', 'png')
    c2.Print( label + '_0tag_mueta_qcd_jet_' + str(ijet) + '.pdf', 'pdf')
    canvs.append(c2)
    fout.cd()
    proj.Write()

