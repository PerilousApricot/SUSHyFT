
from KinNormAnalysis import KinNormAnalysis

from ROOT import TFile
from string import Template

class SummedKinHist :
    def __init__(self, name,title,
                 iminJets, imaxJets, iminTags, imaxTags,
                 nexpTextFile,
                 ifile, idir, ipre, ivar, ilepstr,
                 ikey) :
        self.name = name
        self.title = title
        self.minJets=iminJets
        self.maxJets=imaxJets
        self.minTags=iminTags
        self.maxTags=imaxTags
        self.nexpMap = KinNormAnalysis(nexpTextFile)
        self.nexpMap.add( 'Wbx', 'Wcx', 'Wjets')
        self.nexpMap.add( 'Wjets', 'Wqq' )
        
        self.file = ifile
        self.dir = idir
        self.pre = ipre
        self.var = ivar
        self.lepstr = ilepstr
        self.key = ikey
        self.f = TFile(ifile)
        self.sT = Template('${dir}/${pre}_${var}_${nj}j_${nt}t')

    def getHist(self):
        return self.hist

    def getNorm(self):
        return self.hist.Integral()
    

class SummedKinMCHist(SummedKinHist) : 
    def form(self) :        
        hists = []
        for ijet in range(self.minJets,self.maxJets) :
            for itag in range(self.minTags,self.maxTags) :
                if itag > ijet :
                    continue
                regions = []
                for idir in self.dir:
                    s = self.sT.substitute( dir=idir, pre=self.pre, var=self.var, nj=ijet, nt=itag)
                    print 'Getting ' + s + ' from ' + self.file + ' with input normalization ',
                    hj = self.f.Get( s ).Clone()
                    print hj.Integral()
                    regions.append( hj )
                hi = regions[0]
                for j in range(1,len(regions)):
                    hi.Add(regions[j])
                nexp = self.nexpMap.get( self.key, ijet, itag, self.lepstr)
                if hi.Integral() > 0 :
                    hi.Scale(nexp/hi.Integral())
                hists.append(hi)
        self.hist = hists[0]
        self.hist.SetName(self.name)
        self.hist.SetTitle(self.title)
        for i in range(1,len(hists)):
            self.hist.Add( hists[i] )
        print 'Added histogram with nevents = ' + str(self.hist.Integral())

class SummedKinQCDHist(SummedKinHist) : 
    def form(self) :
        sT1 = Template('${dir1}/${pre}_${var}_${nj}j_${nt}t')
        sT2 = Template('${dir2}/${pre}_${var}_${nj}j_${nt}t')        
        hists = []
        for ijet in range(self.minJets,self.maxJets) :
            for itag in range(self.minTags,self.maxTags) :
                if itag > ijet :
                    continue
                regions = []
                for idir in self.dir:                
                    s1 = sT1.substitute( dir1=idir[0], pre=self.pre, var=self.var, nj=ijet, nt=itag)
                    s2 = sT2.substitute( dir2=idir[1], pre=self.pre, var=self.var, nj=ijet, nt=itag)
                    print 'Getting ' + s1 + ' from ' + self.file + ' with input normalization ',
                    hi1 = self.f.Get( s1 ).Clone()
                    print hi1.Integral()
                    print 'Getting ' + s2 + ' from ' + self.file + ' with input normalization ',
                    hi2 = self.f.Get( s2 ).Clone()
                    print hi2.Integral()
                    hi1.Add( hi2, -1.0 )
                    print 'Summing, we get ' + str( hi1.Integral() )
                    nexp = self.nexpMap.get( self.key, ijet, itag, self.lepstr)
                    if hi1.Integral() > 0 :
                        hi1.Scale(nexp/hi1.Integral())
                    hists.append(hi1)
        self.hist = hists[0]
        self.hist.SetName(self.name)
        self.hist.SetTitle(self.title)
        for i in range(1,len(hists)):
            self.hist.Add( hists[i] )

class SummedKinDataHist(SummedKinHist) : 
    def form(self) :
        hists = []
        for ijet in range(self.minJets,self.maxJets) :
            for itag in range(self.minTags,self.maxTags) :
                if itag > ijet :
                    continue                
                regions = []
                for idir in self.dir:
                    s = self.sT.substitute( dir=idir, pre=self.pre, var=self.var, nj=ijet, nt=itag)
                    print 'Getting ' + s
                    hj = self.f.Get( s ).Clone()
                    regions.append( hj )
                hi = regions[0]
                for j in range(1,len(regions)):
                    hi.Add(regions[j])
                hists.append(hi)
        self.hist = hists[0]
        self.hist.SetName(self.name)
        self.hist.SetTitle(self.title)
        for i in range(1,len(hists)):
            self.hist.Add( hists[i] )
            
