import itertools

class EffInfo :
    def __init__(self, index, eff, flavor) :
        self.index = index
        self.eff = eff
        self.flavor =flavor
    def __lt__(self, other ) :
        return self.index < other.index
    def __gt__(self, other ) :
        return self.index > other.index
    def printIt(self) :
        print ' [{0:2.0f} : {1:5.2f}, {2:1.0f}] '.format(
            self.index, self.eff, self.flavor ),


class EffInfoCombinations :
    """Helper class to generate probabilities to tag k out of N jets with different probabilities"""
    def __init__(self, k , verbose=False) :
        self.k = k
        self.xtot = set( self.k )
        self.ik = 0
        self.efftot = 0.0
        self.verbose = verbose

    def multiplies(self, a ) :
        efftot = 1.0
        for ia in a :
            efftot = efftot * ia.eff
        return efftot

    def oneminusmultiplies(self, a ) :
        efftot = 1.0
        for ia in a :
            efftot = efftot * (1 - ia.eff)
        return efftot

    def pTag(self, ijet) :
        """Method to call to get the probabiltiy to tag 'ijet' jets"""
        if self.verbose :
            print '-------------- njets = ' + str(ijet) + '----------------'
        a = itertools.combinations(self.k, ijet)
        iefftot = 0.0
        for ia in a :
            xa = set(ia)
            xb = self.xtot.difference(ia)
            eff1 = self.multiplies(xa)
            eff2 = self.oneminusmultiplies(xb)
            iefftot = iefftot + (eff1 * eff2)

            if self.verbose:
                for ixa in xa :
                    ixa.printIt()
                for ixb in xb :
                    ixb.printIt()
                print ', eff1 = {0:6.2f}, eff2 = {1:6.2f}'.format( eff1, eff2 )
        if self.verbose :
            print '------ Probability to tag {0:3.0f} jets = {1:6.4f}'.format( ijet, iefftot )
        return iefftot
