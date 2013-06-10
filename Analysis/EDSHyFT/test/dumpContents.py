#!/bin/python


from ROOT import *
from array import *

gROOT.Macro("rootlogon.C")


f = TFile('shyftStudies.root')

directories = [
    'pfShyftAna/',
		
    'pfShyftAnaReweightedBTag076/',	
    'pfShyftAnaReweightedBTag082/',
    'pfShyftAnaReweightedNominal/',
    'pfShyftAnaReweightedBTag094/',	
    'pfShyftAnaReweightedBTag100/',	
    'pfShyftAnaReweightedUnity/',
    'pfShyftAnaReweightedLFTag074/',	
    'pfShyftAnaReweightedLFTag080/',
    'pfShyftAnaReweightedNominal/',
    'pfShyftAnaReweightedLFTag094/',	
    'pfShyftAnaReweightedLFTag100/',
    'pfShyftAnaReweightedUnity/'
    ]

sample = 'Top_'
hists = [
    'hT_4j_0t',
    'secvtxMass_4j_1t',
    'secvtxMass_4j_2t',
    ]

for directory in directories :
    integralsum = 0
    print directory
    for ihist in hists :
        h = f.Get( directory + sample + ihist )
        print '{0:30s} : {1:6.2f}'.format( ihist, h.Integral() )
        integralsum = integralsum + h.Integral()
    print '{0:30s} : {1:6.2f}'.format( 'Total', integralsum )    
