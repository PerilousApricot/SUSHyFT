#!/bin/python

from ROOT import *
from array import *

def addSimple( lum, idir, templatedir, histname, k_tot, sample, verbose = False ) :
    prepend = sample[0]
    ifile = sample[1]
    templatefile = sample[2]
    xs = sample[3]
    nevt = sample[4]
    sampleIsData = sample[5]

    if templatedir is not None and sampleIsData is False :
        h = templatefile.Get( templatedir + prepend + histname ).Clone()
        h2 = ifile.Get( idir + prepend + histname ).Clone()
    else :
        h = ifile.Get( idir + prepend + histname ).Clone()

    h.SetName( prepend + histname )
    h.SetTitle( prepend + histname )    
    if sampleIsData is False :
        h.Scale( k_tot * xs * lum * h2.Integral() / (nevt * h.Integral() ) )
    return h
