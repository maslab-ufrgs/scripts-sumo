'''
Created on 08/04/2013

@author: artavares

'''

#>>.rou.xml
#<<edg num_trips

#<vehicle id="aux0" depart="2">
#    <route edges="18to17 17to14 14to12 12to20 20to19 19to5 5to6" />
#</vehicle>

import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser

class CountUsage(object):
    
    def __init__(self, routefile):
        self.routes =  ET.parse(routefile)
        self.usage = {}
        
    def count_usage(self):
        
        for vehicle in self.routes.getroot():
            route = vehicle[0].get('edges').split(' ')
            
            for edge in route:
                #increments the num. of times the edge appears in a route
                self.usage[edge] = self.usage[edge] + 1 if edge in self.usage else 1
                
    def output_usage(self, outstream, separator = ' '):
        sep = separator.decode('string-escape')
        
        #sort the usage array in decreasing order
        ordered_keys = sorted(self.usage, key=lambda x: (self.usage[x], x), reverse=True)
        
        for k in ordered_keys:
            outstream.write(sep.join(['%s','%s\n']) % (k, self.usage[k]) )
            

if __name__ == '__main__':
    optParser = OptionParser()
    optParser.add_option("-r", "--route-file", dest='routefile',
                            help="the input .rou.xml file") 
    #optParser.add_option("-o", "--output-file", dest='outfile',
    #                        help="the output file (mandatory)")
    optParser.add_option("-s", "--separator", default=" ", type='str',
                            help="the separator for the output (default=whitespace)")
    
    (options, args) = optParser.parse_args(sys.argv)
    
    counter = CountUsage(options.routefile)
    counter.count_usage()
    counter.output_usage(sys.stdout, options.separator)
    
        
        
        
        
            
            
