#!/bin/python

# ===================================================
#             stitchFlavorHistory.py
# New and improved!
#
# Inputs:
#    idir : Input directory
#    histname : name of histogram to stitch
#    k_tot : any overall k-factor
#    pathNames: Looks like:
#    pathNames = [
#        ['VqqW_path1'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 1
#        ['VqqW_path2'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 2
#        ['VqqW_path3'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 3
#        ['WjetsW_path4'    , f_wjets ,n_wjets, xs_wjets ],# path 4
#        ['WjetsW_path5'    , f_wjets ,n_wjets, xs_wjets ],# path 5
#        ['WjetsW_path6'    , f_wjets ,n_wjets, xs_wjets ],# path 6
#        ['WjetsW_path11'   , f_wjets ,n_wjets, xs_wjets ],# path 11
#        ]
#    template : optional input template to use instead of just stitching
#               the hists together
#
# This will return a single histogram
#
# ===================================================

from ROOT import *
from array import *


def stitchFlavorHistory( label, lum, idir, histname, k_tot, pathNames, templates, suffixes, verbose=False ) :


    
    flavorSamples = []
    flavorSamples.append([])
    flavorSamples.append([])
    flavorSamples.append([])    
    totalN = 0.0
    for path in pathNames :
        name = path[0]
        ifile = path[1]
        nevt = path[2]
        xs = path[3]        

        # Grab the path's histogram for counts
        for suffix in suffixes :
            s = idir + name + '_' + histname + suffix
            if verbose:
                print 'Grabbing ' + s
            iflav = -1
            if suffix is '_b' or suffix is '_bb' or suffix is '_bc' or suffix is '_bq' :
                iflav = 0
            elif suffix is '_c' or suffix is '_cc' or suffix is '_cq' :
                iflav = 1
            elif suffix is '_q' or suffix is '_qq' :
                iflav = 2

                


            if iflav >= 0 :
                if templates is not None :
                    template = templates[iflav]
                    h1 = ifile.Get(s)
                    h2 = template.Clone()
                    h2.SetName( label[iflav] + histname )
                    h2.SetTitle( label[iflav] + histname )                        
                    h2.Scale( k_tot * xs * lum * h1.Integral() / nevt )
                    flavorSamples[iflav].append( h2 )
                    totalN = totalN + k_tot * xs * lum * h1.Integral() / nevt                    
                    if verbose :
                        print ' k_tot = {0:6.0f}, xs = {1:6.2f}, lum = {2:6.2f}, int = {3:6.2f}, nevt = {4:6.0f}, Norm = {5:6.2f}, hnorm = {6:6.2f} '.format(
                            k_tot, xs, lum, h1.Integral(), nevt,
                            k_tot * xs * lum * h1.Integral() / nevt,
                            h2.Integral()
                            )
                else : # template is None
                    h = ifile.Get(s).Clone()
                    h.SetName( label[iflav] + histname )
                    h.SetTitle( label[iflav] + histname )                        
                    h.Scale( k_tot * xs * lum / nevt )
                    flavorSamples[iflav].append( h )
                    totalN = totalN + k_tot * xs * lum * h.Integral() / nevt                    
                    if verbose :
                        print ' k_tot = {0:6.0f}, xs = {1:6.2f}, lum = {2:6.2f}, int = {3:6.2f}, nevt = {4:6.0f}, Norm = {5:6.2f}, hnorm = {6:6.2f} '.format(
                            k_tot, xs, lum, h.Integral(), nevt,
                            k_tot * xs * lum * h.Integral() / nevt,
                            h.Integral()
                            )                    

    if len(flavorSamples) < 1 :
        print 'Huge problem! No paths!'
        return None
    else :
        if verbose :
            print 'Total number = ' + str(totalN)
        toret = []
        for iflav in range (0, 3):
            if verbose :
                print 'Processing iflav = ' + str(iflav)
            iret = flavorSamples[iflav][0]
            if verbose: 
                print 'Adding normalization ' + str(flavorSamples[iflav][0].Integral())            
            for ipath in range(1,len(flavorSamples[iflav])):
                if verbose: 
                    print 'Adding normalization ' + str(flavorSamples[iflav][ipath].Integral())
                iret.Add( flavorSamples[iflav][ipath])        
            toret.append( iret )
        return toret
