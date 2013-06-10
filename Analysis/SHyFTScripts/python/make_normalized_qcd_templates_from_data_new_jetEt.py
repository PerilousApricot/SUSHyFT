#!/bin/python


# ===================================================
#             make_plots.py
#
#  Simple script to plot a stitched distribution
# ===================================================
# ===================================================


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFile', metavar='F', type='string', action='store',
                  default='Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root',
                  dest='inputFile',
                  help='input file tag to be used')

parser.add_option('--inputDirBkg', metavar='D', type='string', action='store',
                  default='pfShyftAnaLooseNoMETWithD0/',
                  dest='inputDirBkg',
                  help='input directory to be used for Background regions (A + B)')


parser.add_option('--inputDirSig', metavar='D', type='string', action='store',
                  default='pfShyftAnaNoMET/',
                  dest='inputDirSig',
                  help='input directory to be used for Signal regions (C + D)')


parser.add_option('--outlabel', metavar='L', type='string', action='store',
                  default='Mu_shyft_387_v2_shyftana_v9',
                  dest='outlabel',
                  help='label to append to plots')


parser.add_option('--taggedHist', metavar='H', type='string', action='store',
                  default='Data_secvtxMass',
                  dest='taggedHist',
                  help='tagged histogram to plot')


parser.add_option('--useD0VsIso', action='store_true',
                  default=False,
                  dest='useD0VsIso',
                  help='Use d0 versus isolation instead of met versus isolation')

(options, args) = parser.parse_args()

argv = []

from ROOT import *
from array import *

#gROOT.Macro("rootlogon.C")


from sys import argv

f = TFile(options.inputFile)

directorySig = options.inputDirSig
directoryBkg = options.inputDirBkg
if directorySig.find('pf') > -1 :
    label = 'pf'
elif directorySig.find('jpt') > -1 :
    label = 'jpt'



if options.useD0VsIso is False :
    ihist = 'Data_lepIsoVsMET_'
else :
    ihist = 'Data_lepIsoVsD0_'


histsSig = []
histsSig.append( [] )
histsSig.append( [] )
histsBkg = []
histsBkg.append( [] )
histsBkg.append( [] )

stacks = []
legs = []
bins = []
canvs = []

# First get the normalizations from ISO sidebands (ABCD)
maxTags = 2

print 'Getting normalization from sidebands for Sig'
for ijet in range(1,6):    
    h_0tag = f.Get( directorySig + ihist + str(ijet) +'j_0t' )
    h_1tag = f.Get( directorySig + ihist + str(ijet) +'j_1t' )
    if ijet > 1 :
        h_2tag = f.Get( directorySig + ihist + str(ijet) +'j_2t' )    
    h_1tag.SetName( ihist + str(ijet) + 'j_ge1t')
    if ijet > 1 :
        h_1tag.Add( h_2tag, 1.0)
    histsSig[0].append( h_0tag )
    histsSig[1].append( h_1tag )

print 'Getting normalization from sidebands for Bkg'
for ijet in range(1,6):    
    h_0tag = f.Get( directoryBkg + ihist + str(ijet) +'j_0t' )
    h_1tag = f.Get( directoryBkg + ihist + str(ijet) +'j_1t' )
    if ijet > 1:
        h_2tag = f.Get( directoryBkg + ihist + str(ijet) +'j_2t' )    
    h_1tag.SetName( ihist + str(ijet) + 'j_ge1t')
    if ijet > 1 :
        h_1tag.Add( h_2tag, 1.0)
    histsBkg[0].append( h_0tag )
    histsBkg[1].append( h_1tag )




preds = []
preds.append( [] )
preds.append( [] )

if options.useD0VsIso is True :

    # REGIONS:
    # A = nonisolated, high d0
    # B = nonisolated, low d0
    # C = isolated, high d0
    # D = isolated, low d0     <---- SIGNAL REGION
    for ijet in range(1,6) :
        for itag in [0,1] :
            bin_xmin = 1
            bin_ymin = 1
            bin_xmax = histsSig[itag][ijet-1].GetXaxis().FindBin(0.2)
            bin_ymax = histsSig[itag][ijet-1].GetYaxis().FindBin(1.0)
            bin_d0high = histsSig[itag][ijet-1].GetXaxis().FindBin(0.04)
            bin_d0low = histsSig[itag][ijet-1].GetXaxis().FindBin(0.02)
            bin_isohigh = histsSig[itag][ijet-1].GetYaxis().FindBin(0.20)
            bin_isolow = histsSig[itag][ijet-1].GetYaxis().FindBin(0.05)
            n_a = histsBkg[itag][ijet-1].Integral(bin_d0high, bin_xmax, bin_isohigh, bin_ymax)
            n_b = histsBkg[itag][ijet-1].Integral(bin_xmin, bin_d0low, bin_isohigh, bin_ymax )
            n_c = histsSig[itag][ijet-1].Integral(bin_d0high, bin_xmax, bin_ymin, bin_isolow)
            n_d = histsSig[itag][ijet-1].Integral(bin_xmin, bin_d0low, bin_ymin, bin_isolow)
            if n_a > 0 and n_b > 0 and n_c > 0 :
                n_pred = float( n_b ) * float( n_c ) / float( n_a )        
                dn_pred = n_pred * sqrt( 1/n_a + 1/n_b + 1/n_c)
            else :
                n_pred = 1.0
                dn_pred = 1.0
            print ' ijet = {0:3.0f}, itag = {1:3.0f}, na = {2:8.0f}, nb = {3:8.0f}, nc = {4:8.0f}, nd = {5:8.0f}, n_pred = {6:10.2f} +- {7:10.2f}'.format(
                ijet, itag, n_a, n_b, n_c, n_d, n_pred, dn_pred
                )
            preds[itag].append( n_pred )

else :
    

    # REGIONS:
    # A = nonisolated, low met
    # B = nonisolated, high met
    # C = isolated, low met
    # D = isolated, high met     <---- SIGNAL REGION
    for ijet in range(1,6) :
        for itag in [0,1] :
            n_a = histsBkg[itag][ijet-1].Integral(1,    8, 9, 41)
            n_b = histsBkg[itag][ijet-1].Integral(13,121, 9, 41)
            n_c = histsSig[itag][ijet-1].Integral( 1,    8, 1, 5)
            n_d = histsSig[itag][ijet-1].Integral( 13,121, 1, 5)
            if n_a > 0 and n_b > 0 and n_c > 0 :
                n_pred = float( n_b ) * float( n_c ) / float( n_a )            
                dn_pred = n_pred * sqrt( 1/n_a + 1/n_b + 1/n_c)
            else :
                n_pred = 1.0
                dn_pred = 1.0
            print ' ijet = {0:3.0f}, itag = {1:3.0f}, na = {2:8.0f}, nb = {3:8.0f}, nc = {4:8.0f}, nd = {5:8.0f}, n_pred = {6:10.2f} +- {7:10.2f}'.format(
                ijet, itag, n_a, n_b, n_c, n_d, n_pred, dn_pred
                )
            preds[itag].append( n_pred )





# Now make the scaled templates

maxTags = 2
untaghists = []
taghists = []
untaghists2d = []
taghists2d = []
untaghist = 'Data_lepIsoVsjetEt_'
taghist = options.taggedHist + '_'


for ijet in range(1,6):

    # get the 0-tag histogram (mu eta)
    h_0tag = f.Get( directoryBkg + untaghist + str(ijet) + 'j_0t' )
    # get the 1-tag and 2-tag histograms (secvtx mass)
    if options.taggedHist.find( 'secvtxMass' ) > -1 :
        h_1tag = f.Get( directoryBkg + taghist + str(ijet) +'j_1t_vs_iso' )
        if ijet >= 2 :
            h_2tag = f.Get( directoryBkg + taghist + str(ijet) +'j_2t_vs_iso' )
            h_1tag.Add( h_2tag )
        # first fill up the tagged histograms
        taghists2d.append( h_1tag )
        h_1tag_proj = h_1tag.ProjectionX( 'proj_' + taghist + str(ijet) + '_1t', 9, h_1tag.GetNbinsY()+1 )
        h_1tag_proj.SetMarkerStyle(20)
        taghists.append( h_1tag_proj )            
    else :
        h_1tag = f.Get( directoryBkg + taghist + str(ijet) +'j_1t' )    
        if ijet >= 2 :
            h_2tag = f.Get( directoryBkg + taghist + str(ijet) +'j_2t' )
            h_1tag.Add( h_2tag )        
        # first fill up the tagged histograms
        taghists2d.append( h_1tag )
        h_1tag_proj = h_1tag.ProjectionX( 'proj_Data_jetEt_' + str(ijet) + '_1t', 9, h_1tag.GetNbinsY()+1 )
        h_1tag_proj.SetMarkerStyle(20)
        taghists.append( h_1tag_proj )            


    untaghists2d.append( h_0tag )
    h_0tag_proj = h_0tag.ProjectionX( 'proj_Data_jetEt_' + str(ijet) + '_0t', 9, h_0tag.GetNbinsY()+1 )
    h_0tag_proj.SetMarkerStyle(20)
    untaghists.append( h_0tag_proj )


if options.taggedHist.find( 'secvtxMass' ) > -1 :
    taghists[2].Add( taghists[3] )
    taghists[2].Add( taghists[4] )
    taghists[3] = taghists[2].Clone()
    taghists[4] = taghists[2].Clone()
    taghists[3].SetName( 'proj_Data_secvtxMass_4_1t')
    taghists[4].SetName( 'proj_Data_secvtxMass_5_1t')

else :
    untaghists[2].Add( untaghists[3] )
    untaghists[2].Add( untaghists[4] )
    untaghists[3] = untaghists[2].Clone()
    untaghists[4] = untaghists[2].Clone()
    untaghists[3].SetName( 'proj_Data_jetEt_4_0t')
    untaghists[4].SetName( 'proj_Data_jetEt_5_0t')


if options.outlabel is not '' :
    fout = TFile(label + '_' + options.outlabel + '_normalized_qcd_templates.root', 'RECREATE')
else :
    fout = TFile(label + '_normalized_qcd_templates.root', 'RECREATE')    


# Now normalize the histograms to the prediction
for ijet in range(1,6) :
    untaghists[ijet-1].Sumw2()
    untaghists[ijet-1].Scale( preds[0][ijet-1] / untaghists[ijet-1].Integral() )    
    taghists[ijet-1].Sumw2()
    taghists[ijet-1].Scale( preds[1][ijet-1] / taghists[ijet-1].Integral() )


fout.cd()
for ijet in range(1,6):
    untaghists[ijet-1].Write()
    taghists[ijet-1].Write()
    

