import re
import sys
import os.path

def event_flow_selectors(files, tokens, labels ) :

    p = re.compile(r'\s+')
    q = re.compile(r':')

    niterations = len(labels)

    sum_all={}
    
    for s in tokens:
        sum_events = []
        for iiter in range(0,niterations) :
            sum_events.append (0)
        #print len(files), tokens, labels
        for file in files :
            infile = open(file, 'r')
            iteration = 0
            for line in infile :
                #print 's = ', s
                if ( line.find(s) >= 0 ) :
                    #print 'found! line = ',line 
                    i1 = p.split(line)
                    #print 'il = ',  i1
                    #if s in i1:    #<-------------------
                    dead1 = i1.pop( 0 )
                    index = i1.pop( 0 )
                    dead2 = i1.pop( 0 )
                    num = i1.pop( len(i1) - 2)
                    newstring = i1.pop(0)
                    for cattok in i1 :
                        newstring += ' ' + cattok
                    #print ' New match string ' + newstring
                    #print ' Number = ' + str(num)
                    sum_events[iteration] += int(num)
                    iteration += 1
                    if iteration == niterations :
                        break
            infile.close()

        print '-------------'
        print '%s' %s
        print '-------------'
        if s not in sum_all: sum_all[s]={}
        for iteration in range(0,niterations) :
            print '%25s' % labels[iteration],' : %10d' % sum_events[iteration]
            sum_all[s][labels[iteration]]=sum_events[iteration]

    return sum_all
            
                    #print ' The rest = ' + str( line.find( i2, len(line) -1, 0 ) )
                    
#                    for i in ii :
#                        nowhite = re.sub("\s+", "", i)
#                        print nowhite
#                    ii = q.split(line)
#                    for i in ii :
#                        nowhite = re.sub("\s+", "", i)
#                        print nowhite
                    #nvisit[iteration] += int(p.split(line)[3])
                    #npass[iteration]  += int(p.split(line)[4])
                    #nfail[iteration]  += int(p.split(line)[5])
                    #nerror[iteration] += int(p.split(line)[6])
                    #iteration += 1
#            infile.close()
            #for iteration in range(0,niterations):
            #    print '%18s%2d' % (s), iteration,' : visited %10d' % nvisit,', pass %10d' % npass,', fail %10d' % nfail

