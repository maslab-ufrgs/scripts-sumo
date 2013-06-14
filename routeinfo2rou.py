'''
Created on Jun 13, 2013

@author: anderson

Reads a routeinfo.xml result file (generated with --routeinfo.edges) and writes a .rou.xml file 
with the trips contained in it.

Useful when the trips were generated on-the-fly so that you don't have an original .rou.xml file
such as in TraCI-generated trips.

'''
import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser

def convert(rinfofile,roufile, wbegin=0, wend=0):
    
    if wend == 0:
        wend = sys.maxsize
        
    #writes file header (x,edg1,edg2...)
    rinfotree = ET.parse(rinfofile)
    
    drivers = []       
    for vdata in rinfotree.getroot():
        #print float(veh.get('depart')) >= wbegin and float(veh.get('arrival') <= wend
        try:                                                   
            if float(vdata.get('depart')) >= wbegin and float(vdata.get('arrival')) <= wend:
                drivers.append({
                    'id':vdata.get('id'), 
                    'depart': float(vdata.get('depart')), 
                    'route': vdata[0].get('edges')
                })
        except ValueError:
            print 'Warning: %s has no depart or arrival, skipping...' % (vdata.get('id'))  
            #print '' 
                
    #sorts drivers by their depart
    sdrivers = sorted(drivers, key=lambda x: x['depart'])
    
    ofile = open(roufile,'w')
    ofile.write('<routes>\n')       
    for d in sdrivers:
        ofile.write('\t<vehicle depart="%.2f" id="%s" >\n' % (d['depart'], d['id']))
        ofile.write('\t\t<route edges="%s" />\n' % d['route'])
        ofile.write('\t</vehicle>\n')
    ofile.write('</routes>\n')     
    ofile.close()
        
    

if __name__ == '__main__':
    
    desc="""Reads a routeinfo.xml result file (generated with --routeinfo.edges) and writes a .rou.xml file 
with the trips contained in it.

Useful when the trips were generated on-the-fly so that you don't have an original .rou.xml file
such as in TraCI-generated trips.

One can specify a time window to reconstruct only the trips that occurred there"""
    
    parser = OptionParser(description=desc)
    parser.add_option("-b", "--begin", type="int", default=0, help="begin of the time window")
    parser.add_option("-e", "--end", type="int", default=0, help="end of the time window; default=0 (unlimited)")
    
    parser.add_option("-r", "--routeinfo", type="string", 
        help="path to the routeinfo file from which the trips will be reconstructed")    

    parser.add_option("-o", "--output", type="string", default=None,
        help="The path to the output .rou.xml file where the reconstructed trips will be written")
                         
    #parser.add_option("-s", "--seed", type="int", help="random seed")
    
    (options, args) = parser.parse_args()
    
    convert(
          options.routeinfo, options.output, options.begin, options.end
    )
    print 'Output file %s written.' % options.output
    