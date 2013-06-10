#!/bin/python

class KinNorm:
    """A class to keep track of the normalization for kinematic distributions"""


    # Max number of jets and tags
    maxJets = 5
    maxTags = 2
    def __init__(self) :

        # This stores the jet-tag bins for muons
        self.muonJetTagBins     = [ ]
        self.electronJetTagBins = [ ]
        # This stores the lepton type
        self.leptonType=''
        # Initialize the jet-tag bins.
        # Use indexing such that ijet=0 is "0 jets", etc
        for ijet in xrange(self.maxJets+1) :
            self.muonJetTagBins.append([])
            self.electronJetTagBins.append([])
            for itag in xrange( self.maxTags+1) :
                self.muonJetTagBins[ijet].append(0.0)
                self.electronJetTagBins[ijet].append(0.0)
        return None

    # Set a value corresponding to lepton type "lepton", jet/tag bin ijet,itag, with value "val"
    def set(self, ijet, itag, lepton, val) :
        if lepton == 'Muons' or lepton == 'Mu' :            
            self.muonJetTagBins[ijet][itag]=val
        elif lepton == 'Electrons' or lepton == 'Ele' or lepton == 'El' :
            self.electronJetTagBins[ijet][itag]=val

    # Get a value corresponding to lepton type "lepton", jet/tag bin ijet,itag
    def get(self, ijet, itag, lepton) :
        if lepton == 'Muons' or lepton == 'Mu' :            
            return self.muonJetTagBins[ijet][itag]
        elif lepton == 'Electrons' or lepton == 'Ele' or lepton == 'El' :
            return self.electronJetTagBins[ijet][itag]

    def add(self, other) :
        for ijet in xrange(self.maxJets+1):
            for itag in xrange(self.maxTags+1):
                self.muonJetTagBins[ijet][itag] += other.muonJetTagBins[ijet][itag]
                self.electronJetTagBins[ijet][itag] += other.electronJetTagBins[ijet][itag]

    def dump(self):
        print '---------Muons-------------'
        print '{0:8s}'.format(''),
        for itag in xrange(self.maxTags+1):
            print '{0:7.0f}t'.format( itag ),
        print ''
        for ijet in xrange(self.maxJets+1):
            print '{0:7.0f}j'.format( ijet ),
            for itag in xrange(self.maxTags+1):
                print '{0:8.2f}'.format( self.get(ijet,itag,'Muons')),
            print ''
        print '---------Electrons---------'
        print '{0:8s}'.format(''),
        for itag in xrange(self.maxTags+1):
            print '{0:7.0f}t'.format( itag ),
        print ''
        for ijet in xrange(self.maxJets+1):
            print '{0:7.0f}j'.format( ijet ),
            for itag in xrange(self.maxTags+1):
                print '{0:8.2f}'.format( self.get(ijet,itag,'Electrons')),
            print ''
