#!/bin/python

from ROOT import *
from array import *

from sys import argv

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFile', metavar='F', type='string', action='store',
                  default='TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v9.root',
                  dest='inputFile',
                  help='input file to be used')

parser.add_option('--inputDir', metavar='D', type='string', action='store',
                  default='pfShyftAnaMC',
                  dest='inputDir',
                  help='input dir to be used')

parser.add_option('--prepend', metavar='P', type='string', action='store',
                  default='Top',
                  dest='prepend',
                  help='string with which to prepend the histograms')

parser.add_option('--variable', metavar='V', type='string', action='store',
                  default='muEta',
                  dest='variable',
                  help='variable to plot')

parser.add_option('--doFlavorHistory', metavar='F', action='store_true',
                  default=False,
                  dest='doFlavorHistory',
                  help='Check all the flavor history paths')

parser.add_option('--minJets', metavar='m', type='int', action='store',
                  default=1,
                  dest='minJets',
                  help='Min Jets')

parser.add_option('--maxJets', metavar='m', type='int', action='store',
                  default=6,
                  dest='maxJets',
                  help='Max Jets')


parser.add_option('--minTags', metavar='m', type='int', action='store',
                  default=0,
                  dest='minTags',
                  help='Min Tags')

parser.add_option('--maxTags', metavar='m', type='int', action='store',
                  default=3,
                  dest='maxTags',
                  help='Max Tags')


(options, args) = parser.parse_args()

argv = []

#gROOT.Macro("rootlogon.C")


f = TFile(options.inputFile)

nJets = f.Get( options.inputDir + '/nJets')

print 'Njets: ',
for ibin in range(2, nJets.GetNbinsX()):
    print '{0:12.0f}'.format( ibin-1 ),
print ''
print 'Nevt : ',
for ibin in range(2, nJets.GetNbinsX()) :
    print '{0:12.0f}'.format( nJets.GetBinContent(ibin) ),
print ''

maxJets = 6

allTags = [0,1,2]
sums = [0]*maxJets

if options.doFlavorHistory is False : 

    for itag in range(options.minTags, options.maxTags ) :
        print str(allTags[itag]) + 't   : ',
        for ijet in range(options.minJets, options.maxJets ):
            s = options.inputDir + '/' + options.prepend + '_' + options.variable + '_' + str(ijet) + 'j_' + str(itag) + 't'
            h = f.Get( s )
            if h is not None:
                print '{0:12.2f}'.format( h.Integral() ),
                sums[ijet] += h.Integral()
            else :
                print '{0:12s}'.format( '' ),            
        print ''

    print 'Sum  : ',
    for ijet in range(1, maxJets) :
        print '{0:12.2f}'.format( sums[ijet] ),
    print ''

else :
    for path in range(1,12) :
        for itag in range(options.minTags, options.maxTags ) :
            print '{0:2.0f},{1:1.0f}t: '.format( path, itag ),
            for ijet in range(options.minJets, options.maxJets ):
                s = options.inputDir + '/' + options.prepend + '_path' + str(path) + '_' + options.variable + '_' + str(ijet) + 'j_' + str(itag) + 't'
                h = f.Get( s )
                if h is not None:
                    print '{0:12.2f}'.format( h.Integral() ),
                    sums[ijet] += h.Integral()
                else :
                    print '{0:12s}'.format( '' ),            
            print ''


    print 'Sum  : ',
    for ijet in range(1, maxJets) :
        print '{0:12.2f}'.format( sums[ijet] ),
    print ''
