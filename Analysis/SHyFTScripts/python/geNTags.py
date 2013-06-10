#!/bin/python

from ROOT import *
from array import *


def geNTags( hists, N ) :
    if N is 1 :
        hists_geNTags = hists[6::3] + hists[7::3]
    elif N is 2:
        hists_geNTags = hists[7::3]

    isum = 0.0
    for ihist in hists_geNTags :
        isum = isum + ihist.Integral()

    return isum

