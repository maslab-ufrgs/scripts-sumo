'''
Created on Jun 13, 2013

@author: anderson

Given a vehroute file (generated with SUMO's  --vehroute-output), 
writes a file with the number of vehicles that used each road network edge 
in a given time window for each iteration of a given experiment.

Generates a .csv file, one row per iteration.

Requires sumolib in python's PATH
 
'''
import sys
import sumolib
import xml.etree.ElementTree as ET
from optparse import OptionParser

def count(netfile, rprefix, numiter, ofile, firstiter=1, wbegin=0, wend=0, filldigits=0):
    
    if wend == 0:
        wend = sys.maxsize
        
    edgeids = [e.getID() for e in sumolib.net.readNet(netfile).getEdges()]
    
    #writes file header (x,edg1,edg2...)
    ofile = open(ofile,'w')
    ofile.write(','.join(['x'] + edgeids) + '\n')
    
    for i in range(firstiter, numiter+firstiter):
        sys.stdout.write( 'Iteration %d...' % i)
        linkusers = dict((e,0) for e in edgeids)
        
        fname = '%s%s.xml' % (rprefix, str(i).zfill(filldigits))
        
        rtree = ET.parse(fname)
        
        for veh in rtree.getroot():
            #print float(veh.get('depart')) >= wbegin and float(veh.get('arrival') <= wend
            try:                                                   
                if float(veh.get('depart')) >= wbegin and float(veh.get('arrival')) <= wend:
                    for e in veh[0].get('edges').split(' '):
                        #sys.stdout.write(e)
                        linkusers[e] += 1
            except ValueError:
                print 'Warning: %s has no depart or arrival in %s, skipping...' % (veh.get('id'), fname)  
                #print '' 
                    
        #writes the number of link users for each edge in the current iteration
        linearr = [i] + [linkusers[e] for e in edgeids]
        ofile.write(','.join([str(elem) for elem in linearr]) + '\n')
        sys.stdout.write( ' done.\n')            
    ofile.close()
    

if __name__ == '__main__':
    
    desc='''Given a vehroute file (generated with SUMO's  --vehroute-output), 
writes a file with the number of vehicles that used each road network edge 
in a given time window for each iteration of a given experiment.

Generates a .csv file, one row per iteration.

Requires sumolib in python's PATH
'''
    
    parser = OptionParser(description=desc)

    parser.add_option("-b", "--begin", type="int", default=0, help="begin of the time window")
    parser.add_option("-e", "--end", type="int", default=8530, help="end of the time window (0=unlimited; default=8530)")
    
    parser.add_option("-i", "--iterations", type="int", default=400, 
                         help="Number of iterations to be analysed")
    
    parser.add_option("--first-iter", type="int", default=1, 
                         help="Number of the first iteration to be analysed (usually 0 or 1; default=1)")
    
    parser.add_option("-r", "--routeinfo-prefix", type="string", default='routeinfo_',
        help="prefix to the .rou.xml files to be analysed")    
    
    parser.add_option("-n", "--netfile", type="string", default=None,
        help="The path to .net.xml file")
    parser.add_option("-o", "--output", type="string", default=None,
        help="The path to the output file")
                         
    parser.add_option("-z", "--zero-fill", type=int, default=0,
        help="perform a zero fill with the specified number of digits between the prefix and iteration number (for reading dua-generated files)"
    )                         
    
    #parser.add_option("-s", "--seed", type="int", help="random seed")
    
    (options, args) = parser.parse_args()
    
    count(
          options.netfile, options.routeinfo_prefix, 
          options.iterations, options.output, options.first_iter,
          options.begin, options.end, options.zero_fill
    )
    print 'Output file %s written.' % options.output
    