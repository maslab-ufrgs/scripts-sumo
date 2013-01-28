'''
Created on 14/01/2013

@author: artavares
'''

import xml.etree.ElementTree as ET
from optparse import OptionParser

if __name__ == '__main__':
    optParser = OptionParser()
    
    optParser.add_option("-x", "--xml-file", dest='xmlfile',
                            help="the xml file to be converted (mandatory)")
    optParser.add_option("-o", "--output-file", dest='outfile',
                            help="the output file (mandatory)")
    optParser.add_option("-s", "--separator", default=" ", type='str',
                            help="the separator for the output file (default=whitespace")
    optParser.add_option("-t", "--total", default=0, type='int',
                            help="the total number of vehicles in the simulation [use if you need to normalize waiting/total, otherwise normalization will be waiting/(waiting+emitted)]")

    (options, args) = optParser.parse_args()
    
    sep = options.separator
    out = open(options.outfile,'w')
    xmltree = ET.parse(options.xmlfile)
    
    header = ['#time','loaded','emitted','running','waiting',
            'ended','meanWaitingTime','meanTravelTime','duration','wait/(wait+emit)']
    
    if options.total > 0:
        header += ['wait/tot']
    
    out.write(sep.join(header) + '\n')
    
    for element in xmltree.getroot():
        waiting = int(element.get('waiting'))
        waiting_over_wannadepart = float(waiting) / (waiting + int(element.get('emitted')))
        
        
        places = ['%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s']
        variables = (element.get('time'),
              element.get('loaded'),
              element.get('emitted'),
              element.get('running'),
              element.get('waiting'),
              element.get('ended'),
              element.get('meanWaitingTime'),
              element.get('meanTravelTime'),
              element.get('duration'),
              waiting_over_wannadepart
        )
        
        if options.total > 0:
            waiting_over_total =  float(waiting) / options.total
            places += ['%s']
            variables += (waiting_over_total,)
    
        
        out.write(sep.join(places + ['\n']) % variables)
        