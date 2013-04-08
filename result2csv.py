'''
Created on 14/01/2013

@author: artavares
'''

import xml.etree.ElementTree as ET
from optparse import OptionParser

def generate_csv(inxml_file, outcsv_file, fields, separator):
    sep = separator.decode('string-escape')
    out = open(outcsv_file,'w')
    xmltree = ET.parse(inxml_file)
    
    
    fields = fields.split(',') if fields else []
    
    header = list(fields)
    if len(header) > 0:
        header[0] = "#" + header[0]
        out.write(sep.join(header) + '\n')
    
    for element in xmltree.getroot():
        places = ['%s' for f in fields]
        variables = [element.get(f) for f in fields]
        
        out.write(sep.join(places + ['\n']) % tuple(variables))
     
    out.close()
    print "File '%s' written." % options.outfile     
    
if __name__ == '__main__':
    optParser = OptionParser()
    
    optParser.add_option("-x", "--xml-file", dest='xmlfile',
                            help="the xml file to be converted (mandatory)")
    optParser.add_option("-o", "--output-file", dest='outfile',
                            help="the output file (mandatory)")
    optParser.add_option("-s", "--separator", default=" ", type='str',
                            help="the separator for the output file (default=whitespace)")
    optParser.add_option("-t", "--total", default=0, type='int',
                            help="the total number of vehicles in the simulation [use if you need to normalize waiting/total]")
    optParser.add_option("-f", "--fields", default=None, type='str',
                            help="the fields you want to output in the .csv file (field1,field2,field3,...).")

    (options, args) = optParser.parse_args()
    
    generate_csv(options.xmlfile, options.outfile, options.fields, options.separator)