#!/bin/python

from ROOT import *
from array import *

def weightHisto( label, tempDir, histname, sample, color, verbose) :
    ifile = sample[0]
    xs    = sample[1]
    nevt  = sample[2]
    lumi  = sample[3]
    hist  = ifile.Get( tempDir +"/"+ histname ).Clone()
    if verbose:
        print 'file: {0:<20}, histo:{1:<20}, integral:{2:<5.3f}, xs:{3:<5.2f}, lumi:{4:<5.2f}, nevt:{5:<5.2f}, weight:{6:<2.3f}'.format(
            ifile.GetName(),    
            tempDir +"/"+ histname,
            hist.Integral(), xs, lumi, nevt, xs * lumi /nevt
            )
    hist.Sumw2()    
    hist.Scale( xs * lumi /nevt)
    hist.SetName( label+histname )
    hist.SetTitle( label+histname )
    if histname != 'Data_':
        hist.SetFillColor(color)
    if verbose:    
        print 'newName: {0:<5}, newIntegral: {1:5.2f}'.format(label+histname, hist.Integral() )  
    return hist
