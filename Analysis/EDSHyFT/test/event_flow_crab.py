import re
import sys
import os.path

def event_flow_crab(files, tokens) :

    p = re.compile(r'\W+')

    for s in tokens:
        #    print 'Looking at string ' + s

        nvisit = 0
        npass = 0
        nfail = 0
        nerror = 0
        for file in files :
            #print 'Opening file ' + file
            infile = open(file, 'r')
    
            for line in infile :
                if ( line.find(s) >= 0 ) :
                    #                print 'found! line = ',line
                    #                print p.split(line)
                    nvisit += int(p.split(line)[3])
                    npass  += int(p.split(line)[4])
                    nfail  += int(p.split(line)[5])
                    nerror += int(p.split(line)[6])
                    break
            infile.close()
        print '%20s' % (s),' : visited %10d' % nvisit,', pass %10d' % npass,', fail %10d' % nfail

