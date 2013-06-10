# template of stitching script for new (and also old) SHyFT workflow
#
# usage: python stsich.py yourConfigFile.cfg 
#

import ROOT, ConfigParser, re, sys

print sys.argv

config = ConfigParser.ConfigParser()
config.read([sys.argv[1]])


# ----------------------
# function definitions
# ----------------------

# returns list of histograms in the file (root directory)
# and list of folders (to deal with EB_plus, EB_minus, etc.)
def listDirsNames(tfile, rootdir):
    dirs=[]
    th1s=[]
    if rootdir!='':
        tdir = tfile.Get(rootdir)
        if tdir.IsZombie():
            #print 'no such filder in the root file: ', rootdir
            return dirs,th1s
        keylist = tdir.GetListOfKeys()
    else:
        keylist = tfile.GetListOfKeys()
    
    for key in keylist:
        if key.GetClassName()=='TH1F':
            th1s.append(key.GetName())
        elif key.GetClassName()=='TDirectoryFile':
            dirs.append(key.GetName())

    return dirs,th1s

# returns list of names to consider in stitching
def selectDirNames(names, hist_to_read, suffix):
    filtered = []
    #print 'search string: ',hist_to_read+suffix+'$'
    valid = re.compile(hist_to_read+suffix+'$')
    for n in names:
        if valid.search(n):
            filtered.append(n)
    return filtered

def getHist(tfile, root_dir, tdir, name):
    readname=''
    if root_dir!='':
        readname = root_dir + '/'

    if tdir=='':
        readname += name
    else:
        readname += tdir + '/' + name
    #print 'getting ',readname
    th1 = tfile.Get(readname)
    if th1.IsZombie():
        print 'no such histogram!'
        return None
    return th1

# get a clone of the histogram, considering its location
def getClone(tfile, root_dir, tdir, name):
    th1 = getHist(tfile, root_dir, tdir, name)
    cloned = th1.Clone()
    cloned.Sumw2()
    return cloned

# substitute the leading part of the name (Top, WJets, etc) by user-defined prefix
# will help to deal with multiple single top templates, for example
def recombineName(name,prefix,suffix):
    out = '_'
    l = name.split('_')
    l[0]=prefix
    if suffix!='':
        l.pop()
    return out.join(l)

# scale histogram using all information provided in the config
# sections that have 'Data' or 'QCD' in their names have special treatment - they are not rescaled
# in case of QCD it is needed to deal with externally produced templates
def getScaleHistogram(hclone, config, section):
    sf=1.0
    if 'Data' in section or 'QCD' in section:
    #if 'Data' in section:
        # special treatment for data (do nothing)
        pass
    else:
        xs = eval(config.get(section, 'xs'))
        #xs = config.getfloat(section, 'xs')
        #print 'xs ', xs
        globalSF = config.getfloat(section, 'globalSF')
        lum = config.getfloat(section, 'lum')
        n_gen = config.getfloat(section, 'n_gen')
        #print 'SF ',globalSF, ',lum ', lum, ',n_gen' , n_gen 
        sf*=xs*globalSF*lum/n_gen
    return sf

# extract template histogram if needed. normalize it to 1.0
def getTemplate(infile, config, section):
    # so far we need only one template per sample, we do not differentiate plus/minus etc.
    if config.has_option(section,'template_hist'):
        if config.has_option(section,'template_file'):
            # we have to open some external file
            extrafile = ROOT.TFile(config.get(section,'input_folder')+'/'+
                                   config.get(section,'template_file'),'READONLY')
            if extrafile.IsZombie():
                print 'No file ', config.get(section,'template_file'), ' in ', config.get(section,'input_folder')
                exit()  
            template = getClone(extrafile, '', '', config.get(section,'template_hist'))
            template.SetDirectory(infile.GetDirectory(''))
            extrafile.Close()
        else:
             # read the template from input_file
             template = getClone(infile, '', '', config.get(section,'template_hist')) 
        template.Scale(1.0/template.Integral())
        return template
    else:
        return None


# ------------
# main part 
# ------------

# loop over sections (samples)
for section in config.sections():
    print '========================='
    print 'Section: ',section
    print '========================='
    print config.items(section)
    
    infile = ROOT.TFile(config.get(section,'input_folder')+'/'+
                        config.get(section,'input_file'),'READONLY')
    if infile.IsZombie():
        print 'No file ', config.get(section,'input_file'), ' in ', config.get(section,'input_folder')
        exit()
    
    # open a subfolder in the root file if needed
    root_dir=''
    if config.has_option(section,'root_dir'):
        root_dir = config.get(section,'root_dir')
    
    (dirs,th1s) = listDirsNames(infile, root_dir)
    print dirs
    
    suffix=''
    if config.has_option(section,'suffix'):
        suffix = config.get(section,'suffix')
    
    prefix=section
    if config.has_option(section,'prefix'):
        prefix = config.get(section,'prefix')
    
    # add this to the output file names (like pfShyftAna in old format)
    outfile_suffix=''
    if config.has_option(section,'outfile_suffix'):
        outfile_suffix = config.get(section,'outfile_suffix')
    
    # if we want to use template shape
    template = getTemplate(infile, config, section)
    
    good_names = selectDirNames(th1s, config.get(section,'hist_to_read'), suffix)
    print good_names
    # loop over histograms, read them, scale, save to the output file
    dirs.insert(0,'') # also work with root_dir
    for d in dirs:
        # ==== do not go into subfolders for now ====
        if d!='': continue
        # ===========================================
        outfname = config.get(section,'output_folder') + '/' + 'stitched_' + root_dir + outfile_suffix + d + '.root'
        #print 'will open file: ',outfname
        outfile = ROOT.TFile(outfname, 'UPDATE')
        outdir = outfile.GetDirectory('')
        (existing_dirs,existing_names) = listDirsNames(outfile, '')

        for hname in good_names:
            hclone = getClone(infile, root_dir, d, hname)
            # save event counts for future reference
            ##print 'raw integral ', hclone.Integral()
            ##print 'raw entries ', hclone.GetEntries()
            # get the scale to use
            scale = getScaleHistogram(hclone, config, section)
            #print 'scale ', scale
            outhname = recombineName(hname, prefix, suffix)
                
            hclone.Scale(scale)
            ##print 'scaled integral ', hclone.Integral()
            # here we should be able to use templates if needed
            if template != None:
                new_clone = template.Clone()
                new_clone.Scale(hclone.Integral())
                hclone = new_clone
            
            if outhname in existing_names:
                if config.has_option(section,'prefix'):
                    # add new histogram to existing one
                    oldhist = getHist(outfile, '', '', outhname)
                    ##print 'integral before addition ', oldhist.Integral()
                    oldhist.Add(hclone)
                    ##print 'integral after addition ', oldhist.Integral()
                    oldhist.Write(oldhist.GetName(), ROOT.TH1F.kOverwrite)
                else:
                    print 'you seem to be running stitching more than once, clean the output folder!!!'
            else:
                # store this histogram in the output file
                hclone.SetName(outhname)
                hclone.SetDirectory(outdir)
                print 'saving with integral ', hclone.Integral()
                hclone.Write()

        outfile.Close()
    infile.Close()

#print config.getfloat(section, 'xs')
