#!/bin/python


from sys import argv


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--input', metavar='F', type='string', action='store',
                  default='shyftana_387_v1',
                  dest='input',
                  help='input file tag to be used')

parser.add_option('--mcDir', metavar='D1', type='string', action='store',
                  default='pfShyftAna',
                  dest='histdir',
                  help='TFileDirectory from where to get the hists for MC')

parser.add_option('--templateDir', metavar='D3', type='string', action='store',
                  default='pfShyftAnaMC',
                  dest='templatedir',
                  help='TFileDirectory from where to get the templates for MC')

parser.add_option('--outputLabel', metavar='L', type='string', action='store',
                  default='btagReweighted36pb_jes',
                  dest='outputLabel',
                  help='output label for the output root file')


parser.add_option('--variation', metavar='L', type='string', action='store',
                  default='central',
                  dest='variation',
                  help='variation. Options are (\'\', largerISRFSR, smallerISRFSR, matchingdown, matchingup, scaledown, scaleup')

parser.add_option('--tune', metavar='L', type='string', action='store',
                  default='D6T',
                  dest='tune',
                  help='PYTHIA tune. Options are (Z2, D6T)')



parser.add_option('--makePretagPlots', action='store_true',
                  default=False,
                  dest='makePretagPlots',
                  help='Plot everything with muon eta rather than secvtx mass')


parser.add_option('--lum', metavar='L', action='store',
                  default=35.9,
                  dest='lum',
                  help='Luminosity of the data')

(options, args) = parser.parse_args()

inFileEnd = options.input + '_simplesys'
tempstr   = options.histdir
outlabel  = options.outputLabel

histdir = tempstr+'/'
outfilestr = tempstr + '_' + outlabel
templatedir = options.templatedir + '/'

argv = []



if options.variation != 'central' :
    variation = options.variation + '_'
else :
    variation = ''

tune = options.tune

from ROOT import *
from array import *

from stitchFlavorHistory import *
from addSingleTops import *
from addSimple import *

# load up root
gROOT.Macro("rootlogon.C")

# ---------------------------------------------
# Get the files from whatever samples you want to stitch
# ---------------------------------------------
if options.variation != 'pu' : 
    print 'opening file ' + 'TTJets_' + tune + '_' + variation + '7TeV-madgraph-tauola_'+inFileEnd+'.root'
    f_ttbar = TFile('TTJets_' + tune + '_' + variation + '7TeV-madgraph-tauola_'+inFileEnd+'.root')
else :
    print 'opening file ' + 'TTJets_TuneD6T_7TeV-madgraph-tauola_'+inFileEnd+'.root'
    f_ttbar = TFile('TTJets_TuneD6T_7TeV-madgraph-tauola_'+inFileEnd+'.root')    
print 'opening file ' + 'TTJets_TuneD6T_7TeV-madgraph-tauola_'+options.input+'.root'
f_ttbar_central_all = TFile('TTJets_TuneD6T_7TeV-madgraph-tauola_'+options.input+'.root')

bmass = f_ttbar_central_all.Get( templatedir + 'bmass')
cmass = f_ttbar_central_all.Get( templatedir + 'cmass')
lfmass = f_ttbar_central_all.Get( templatedir + 'lfmass')

bmass.Scale(1.0/bmass.Integral())
cmass.Scale(1.0/cmass.Integral())
lfmass.Scale(1.0/lfmass.Integral())

templates = [bmass, cmass, lfmass]

if options.makePretagPlots is False :
    tagDists = [
        'muEta',
        'secvtxMass',
        'secvtxMass'
        ]
    wjetsTemplates = [
        None,
        templates,
        templates
        ]
else :
    tagDists = [
        'muEta',
        'muEta',
        'muEta'
        ]
    wjetsTemplates = [
        None,
        None,
        None
        ]


# ---------------------------------------------
# Assumed luminosity (pb-1)
# ---------------------------------------------
lum = options.lum

globalSF = 0.91 # From muon trigger efficiency

# ---------------------------------------------
# Leading order cross sections (pb)
# ---------------------------------------------
xs_ttbar =   157.5 * globalSF
xs_wjets = 24170.0 * globalSF # LO
xs_wtot  = 31314.0 * globalSF # NNLO
xs_zjets =  3048.0 * globalSF
xs_vqq   =    35.8 * globalSF
xs_qcd   = 79688.0 * globalSF
xs_st_t  =    20.93 * globalSF
xs_st_s  =     0.0 * globalSF # xs_singS  =     4.6 * 0.32442
xs_st_tW =    10.6 * globalSF


# ---------------------------------------------
# Relative "k" factors.
# There is an overall K-factor to get to the
# NLO (or NNLO) cross section,
# and then individual factors for each
# heavy flavor species, which can be different.
# ---------------------------------------------

k_wtot = xs_wtot / xs_wjets
s_wbb = 1.0
s_wcc = 1.0
s_wqq = 1.0


# ---------------------------------------------
# Number of generated events
# ---------------------------------------------
n_ttbar_central =  1306182
n_ttbar_ifsr_up =  1394010
n_ttbar_ifsr_down = 1221664
n_ttbar_matchingdown = 938005
n_ttbar_matchingup = 1036492
n_ttbar_scaledown = 1098971
n_ttbar_scaleup = 1153236
n_ttbar_pu = 1281237

if options.variation == 'central' :
    n_ttbar = n_ttbar_central
elif options.variation == 'largerISRFSR' :
    n_ttbar = n_ttbar_ifsr_up
elif options.variation == 'smallerISRFSR' :
    n_ttbar = n_ttbar_ifsr_down
elif options.variation == 'matchingup' :
    n_ttbar = n_ttbar_matchingup
elif options.variation == 'matchingdown' :
    n_ttbar = n_ttbar_matchingdown
elif options.variation == 'scaleup' :
    n_ttbar = n_ttbar_scaleup
elif options.variation == 'scaledown' :
    n_ttbar = n_ttbar_scaledown
elif options.variation == 'pu' :
    n_ttbar = n_ttbar_pu
else :
    print 'you did not specify a variation, using default'
    n_ttbar = n_ttbar_central

# ---------------------------------------------
# get the output file
# ---------------------------------------------
f_out = TFile('shyftPlots_stitched_' + outfilestr + '.root', 'RECREATE')

# ---------------------------------------------
# Template name
# ---------------------------------------------
#histnameTag = 'secvtxMass_'
#histnames0Tag = ['muEta']
#histnames0Tag = ['MET', 'hT', 'wMT', 'muEta']
#histnamesSing = ['nJets', 'nTags', 'm3']


# ---------------------------------------------
# maximum number of jets and tags
# ---------------------------------------------
maxJets = 6
maxTags = 3

# ---------------------------------------------
# ---------------------------------------------
#                   STEP 4 : Simple hists
# ---------------------------------------------
# ---------------------------------------------

quicksamples = []

quicksamples.append( ['Top_', f_ttbar, f_ttbar_central_all,  xs_ttbar, n_ttbar, False] )

allsimpleHists = []
for isample in range(0,len(quicksamples)) :
    simpleHists = []
    for ijet in range(1,maxJets) :
        for itag in range(0,maxTags) :
            if itag > ijet :
                continue
            if quicksamples[isample][0] is not 'Data_' :
                hist = addSimple( lum, histdir, templatedir, tagDists[itag]+'_'+str(ijet)+'j_'+str(itag)+'t', 1.0,
                                  quicksamples[isample])
            else :
                hist = addSimple( lum, histdirData, None, tagDists[itag]+'_'+str(ijet)+'j_'+str(itag)+'t', 1.0,
                                  quicksamples[isample])
            simpleHists.append(hist)
    allsimpleHists.append( simpleHists )


f_out.cd()
for histg in allsimpleHists :
    for hist in histg :
        hist.Write()

f_out.Close()
