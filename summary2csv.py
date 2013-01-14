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
    optParser.add_option("-s", "--separator", default=" ",
                            help="the separator for the output file (default=whitespace")

    (options, args) = optParser.parse_args()
    
    sep = options.separator
    out = open(options.outfile,'w')
    xmltree = ET.parse(options.xmlfile)
    
    out.write(sep.join(
            ['#time','loaded','emitted','running','waiting',
            'ended','meanWaitingTime','meanTravelTime','duration']
        ) + '\n'
    )
    for element in xmltree.getroot():
        print element.get('duration')
        out.write('%s %s %s %s %s %s %s %s %s\n' % ( 
                  element.get('time'),
                  element.get('loaded'),
                  element.get('emitted'),
                  element.get('running'),
                  element.get('waiting'),
                  element.get('ended'),
                  element.get('meanWaitingTime'),
                  element.get('meanTravelTime'),
                  element.get('duration')
        ))
        