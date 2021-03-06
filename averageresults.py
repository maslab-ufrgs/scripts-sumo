'''
Created on 24/03/2013

@author: artavares

This scripts writes a .csv file with the average values of user-selected fields 
from a sequence of SUMO output files.

Example: duaIterate.py generated 100 tripinfo files: tripinfo_000.xml to 
tripinfo_099.xml, and the user wants to know the average travel time of each iteration
 
'''

import xml.etree.ElementTree as ET
import sys
import os
import csv
from optparse import OptionParser
import collections

def average_results(options):
    '''
    Averages the results of the given attributes of a xml file.
    
    The options object is configured according to parse_args()
    
    '''
    
    if not options.iterations:
        print 'parameter -i/--iterations required.'
        exit()
    
    #data = collections.defaultdict(dict)
    #print options
    sep = options.separator.decode('string-escape')
    
    #opens output file and writes header
    outfile = open(options.output, 'w')
    fields = options.fields.split(',')
    
    #adds the first column (iteration) to the fields
    fields = ['it'] + fields
    outfile.write('#' + sep.join(fields) + '\n')
    
    for i in range(options.iterations):
        sys.stdout.write('Generating averages for iteration %d' % (i + 1) )
        
        tripinfo_file = '%s%s.xml' % (options.prefix, str(i).zfill(3))
        #parses the i-th tripinfo file
        tree = ET.parse(tripinfo_file)
        
        #initializes average data and sets the iteration number
        data = {f:0 for f in fields}
        data['it'] = i + 1
        
        ftrips = full_trips_in_window(options.begin, options.end, tripinfo_file)
        print ': %d full trips in window (%d,%d)' % (len(ftrips),  options.begin, options.end)
        #traverses the xml file, averaging the values of the fields
        parsed_elements = 0
        for element in tree.getroot():
            
            #skips vehicles who haven't completed trips within the time window
            if element.get('id') not in ftrips:
                continue
            
            #print element.attrib
            for f in fields[1:]:
                #print type(data[f]), type(element.get(f)), type(parsed_elements)
                data[f] = new_average(data[f], element.get(f), parsed_elements)
            
            parsed_elements += 1
            
        #writes one line in the output
        places = ['%s' for f in fields]
        variables = [data[f] for f in fields]
        
        outfile.write((sep.join(places) + '\n') % tuple(variables))
        
    print "Output file '%s' written." % options.output

def new_average(old_avg, new_value, stepnum):
    #if old_avg == {}:
    #    return new_value
    #old_avg = float(old_avg)
    #print new_value, old_avg, stepnum
    return ( (float(new_value) - float(old_avg)) / (stepnum + 1)) + old_avg


def full_trips_in_window(begin, finish, tripinfo_file):
    '''
    Returns a list with the ID of the drivers that
    made a full trip between begin and finish
    
    '''
    if finish == 0:
        finish = sys.maxint
    
    rinfo_tree = ET.parse(tripinfo_file)
    
    fulltrips = []
    
    #handles edge case:
    if finish == 0:
        finish = sys.maxint
    
    for vdata in rinfo_tree.getroot():
        try:
            if float(vdata.get('depart')) >= begin and float(vdata.get('arrival')) <= finish:
                fulltrips.append(vdata.get('id'))
        except ValueError:
            print 'Warning: %s has no depart or arrival in %s, skipping...' % (vdata.get('id'), tripinfo_file)
    
    return fulltrips 


def parse_args():
    
    parser = OptionParser()
            
    parser.add_option(
        '-o', '--output', type=str, default='avgresults.csv',
        help = 'output file'
    )
    
    parser.add_option(
        '-b', '--begin',
        help='the start time of the time window',
        type=int, default=0
    )
    
    parser.add_option(
        '-e', '--end',
        help='the end time of the time window, 0=unlimited',
        type=int, default=0
    )
    
    parser.add_option(
        "-f", "--fields", default=None, type='str',
        help="the fields you want to output in the .csv file (field1,field2,field3,...)."
    )
    
    parser.add_option(
        '-p', '--prefix',
        help='the prefix for the SUMO result files: [prefix]i.xml, where i is the iteration',
        type=str, default=None
    )
    
    parser.add_option(
        '-i', '--iterations',
        help='the number of iterations to be read from inputs',
        type=int
    )
    
    parser.add_option(
        '-s', '--separator',
        help='the separator for the output file',
        type=str, default=','
    )
    
    return parser.parse_args(sys.argv)



if __name__ == '__main__':
    (options, args) = parse_args()
    average_results(options)

