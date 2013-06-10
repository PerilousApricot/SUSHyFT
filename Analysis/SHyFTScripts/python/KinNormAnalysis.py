

from kinnorm import KinNorm



class KinNormAnalysis :

    def __init__(self, inputTextFile) :

        # This will hold a mapping like "Data--->0, Total--->1, Top--->2", etc.
        # It's used to hold the indices for the various types
        self.speciesIndex = dict( {} )
        self.species = dict( {} )
        
        intext = open(inputTextFile)

        lines = intext.readlines()

        # Looping over lines
        for line in lines:
            # here's the title line. Get a map of the headers and indices
            if line[0] == '#' :
                head = line.split('&')
                for iihead in range(0,len(head)) :
                    ihead = head[iihead]
                    ihead2 = ihead.rstrip().rstrip('\\\\').strip()
                    if ihead2 != '#' :
                        self.speciesIndex[iihead-1] = ihead2 # Don't count the #
                for ispecies in range(0,len(self.speciesIndex)) :
                    self.species[ self.speciesIndex[ispecies] ] = KinNorm()
            # These are actual lines with numbers in them
            else :
                # Split up the columns.
                #   The first is the jet/tag bin and lepton type.
                #   The remaining are the counts per species for that jet/tag bin and lepton type.
                items = line.split('&')
                firsttag = True
                muEleIndex = 0
                lepStr = 'Muon'
                for iitem in range(0,len(items)) :
                    item = items[iitem]
                    tok = item.rstrip().rstrip('\\\\').strip()
                    # Figure out the jet/tag/lepton bin
                    if firsttag:
                        parsed = tok.split()
                        njets = int(parsed[0])
                        ntags = int(parsed[2])
                        lepStr = parsed[4]
                        firsttag = False
                    # Upload the normalizations to the arrays
                    else :
                        self.species[ self.speciesIndex[iitem-1] ].set( njets, ntags, lepStr, float(tok) )

    def dump(self):
        for ispecies in self.species.items():
            print ispecies[0]
            ispecies[1].dump()

    def add(self, f1, f2, rename=None) :
        if rename is None:
            self.species[ f1 ].add( self.species[f2] )
            del self.species[f2]
        else :
            self.species[ rename ] = self.species[f1]
            self.species[ rename ].add( self.species[f2] )
            del self.species[f1]
            del self.species[f2]

    def get(self, ikey, ijet, itag, lepStr ) :
        return self.species[ikey].get( ijet, itag, lepStr )
