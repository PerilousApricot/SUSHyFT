#!/bin/python

from ROOT import *
from array import *

def addHistos( label, tempDir, histname, Samples, color, verbose) :
    histos = []

    for iSample in Samples :
        prepend = iSample[0]
        ifile = iSample[1]
        xs = iSample[2]
        nevt = iSample[3]
        lumi = iSample[4]
        #print tempDir +"/"+  prepend + histname
        hist = ifile.Get( tempDir +"/"+  prepend + histname ).Clone()
        if verbose:
            print 'file: {0:<20}, histo:{1:<20}, integral:{2:<5.3f}, xs:{3:<5.2f}, lumi:{4:<5.2f}, nevt:{5:<5.2f}, weight:{6:<2.3f}'.format(
                ifile.GetName(),    
                tempDir +"/"+  prepend + histname,
                hist.Integral(), xs, lumi, nevt, xs * lumi /nevt
                )
        hist.Sumw2()    
        hist.Scale( xs * lumi /nevt)
        histos.append( hist )
    histo = histos[0]
    for ihisto in range(0, len(histos) ):
        #print len(histos)
        histo.Add( histos[ihisto] )              
        histo.SetName( label+histname )
        histo.SetTitle( label+histname )
        histo.SetFillColor( color)
    if verbose:    
        print 'newName: {0:<5}, newIntegral: {1:5.2f}'.format(label+histname, histo.Integral() )   
    return histo
