#!/bin/python

from ROOT import *
from array import *

def addSingleTops( label, lum, idir, templatedir, histname, k_tot, singleTopSamples, verbose = False ) :
    singleTops = []

    for singleTopSample in singleTopSamples :
        prepend = singleTopSample[0]
        ifile = singleTopSample[1]
        xs = singleTopSample[2]
        nevt = singleTopSample[3]
        templateHist = ifile.Get( templatedir + prepend + histname ).Clone()        
        hist = ifile.Get( idir + prepend + histname ).Clone()
        templateHist.Scale( k_tot * xs * lum * hist.Integral() / ( nevt * templateHist.Integral() ) )
        singleTops.append( templateHist )

    singleTop = singleTops[0]
    for isingleTop in range(1, len(singleTops) ):
        singleTop.Add( singleTops[isingleTop] )

    singleTop.SetName( label + histname )
    singleTop.SetTitle( label + histname )    
    return singleTop
