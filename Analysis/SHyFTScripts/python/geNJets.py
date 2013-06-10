#!/bin/python

from ROOT import *
from array import *


def geNJets( hists, N ) :
    if N is 3 :
        hists_geNJets = hists[6::3] + hists[7::3]
    elif N is 4:
        hists_geNJets = hists[9::3] + hists[10::3]

    isum = 0.0
    for ihist in hists_geNJets :
        isum = isum + ihist.Integral()

    return isum

