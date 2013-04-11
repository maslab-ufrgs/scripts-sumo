'''
Created on 08/04/2013

@author: Gabriel Ramos
'''
import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser
from igraph import *

def getGraph():
    g = Graph()
    g.add_vertices(["A1","B1","A","B","C","D","E","F","G","H","I","J","K","L","M","L1","M1"])
    g.add_edges([("A1","A"),("A","A1"),("B1","B"),("B","B1"),("A","B"),("B","A"),("A","C"),("C","A"),("A","D"),("D","A"),
                 ("B","D"),("D","B"),("B","E"),("E","B"),("C","D"),("D","C"),("C","F"),("F","C"),("C","G"),("G","C"),
                 ("D","E"),("E","D"),("D","G"),("G","D"),("D","H"),("H","D"),("E","H"),("H","E"),("F","G"),("G","F"),
                 ("F","I"),("I","F"),("G","J"),("J","G"),("G","H"),("H","G"),("H","K"),("K","H"),("I","L"),("L","I"),
                 ("I","J"),("J","I"),("J","K"),("K","J"),("J","L"),("L","J"),("J","M"),("M","J"),("K","M"),("M","K"),
                 ("L","L1"),("L1","L"),("M","M1"),("M1","M")]);
    g.es["name"] = ["A1A","AA1","B1B","BB1","AB","BA","AC","CA","AD","DA","BD","DB","BE","EB",
                    "CD","DC","CF","FC","CG","GC","DE","ED","DG","GD","DH","HD","EH","HE",
                    "FG","GF","FI","IF","GJ","JG","GH","HG","HK","KH","IL","LI","IJ","JI",
                    "JK","KJ","JL","LJ","JM","MJ","KM","MK","LL1","L1L","MM1","M1M"];
    return g

def calc_Betweenness(in_file, out_file, separator, topological, OD, routes):
    infile = ET.parse('ortuzar.rou.xml')
    table = {}
    
    #initialize table with edges 
    g = getGraph()
    for edge in g.es["name"]:
        table[edge] = [1, 0, 0]
    
    #count the number of times each edge appears in a route/OD pair
    for vehicle in infile.getroot():
        route = vehicle[0].get('edges').split(' ')
        for element in range(len(route)):
            edge = route[element]
            sumOD = 1 if element in [0,len(route)-1] else 0 
            #if edge not in table:
            #    table[edge] = [1, 1, sumOD]
            #else:
            table[edge] = [1, table[edge][1]+1, table[edge][2]+sumOD]
    
    #calculate betweenness
    wlR = [1]*len(g.es["name"])
    wlOD = [1]*len(g.es["name"])
    for e in range(len(g.es["name"])):
        edge = g.es["name"][e]
        if edge in table:
            wlR[e] = table[edge][0] + table[edge][1]
            wlOD[e] = table[edge][0] + table[edge][2]
    bR = g.edge_betweenness(weights=wlR)
    bOD = g.edge_betweenness(weights=wlOD)
    
    #update table with betweenness values
    for e in range(len(g.es["name"])):
        edge = g.es["name"][e]
        if edge in table:
            table[edge][1] = bR[e]
            table[edge][2] = bOD[e]
    
    #generate the output file(s)
    if routes:
        outR = open(out_file + '.routes.csv', 'w')
        outR.write('#Edge' + separator + 'Betweenness\n')
    if OD:
        outOD = open(out_file + '.OD.csv', 'w')
        outOD.write('#Edge' + separator + 'Betweenness\n')
    
    #print values to files
    for element in table:
        if routes:
            outR.write(element + separator + str(table[element][1]) + '\n')
        if OD:
            outOD.write(element + separator + str(table[element][2]) + '\n')
    
    if routes:
        outR.close()
    if OD:
        outOD.close()
    
if __name__ == '__main__':
    optParser = OptionParser()
    
    optParser.add_option("-r", "--routes-file", dest='routesfile',
                            help="the routes file to which the betweenness should be calculated (mandatory)")
    optParser.add_option("-c", "--output-csv", default="out", dest='csvfile',
                            help="the output CSV file, without extension (default=out)")
    optParser.add_option("-s", "--separator", default=" ", type='str',
                            help="the separator for the output file (default=whitespace)")
    optParser.add_option("-T", "--topological", default=False, action="store_true",
                            help="topological analysis (no weights)")
    optParser.add_option("-O", "--OD", default=False, action="store_true",
                            help="OD pairs analysis")
    optParser.add_option("-R", "--routes", default=False, action="store_true",
                            help="routes analysis")
    
    (options, args) = optParser.parse_args()
    
    if options.routesfile == None:
        print "The routes file must be informed"
        sys.exit()
    
    if options.topological == False and options.OD == False and options.routes == False:
        print "Specify at least one type of analysis (topological, OD pairs, routes)"
        sys.exit()
        
    calc_Betweenness(options.routesfile, options.csvfile, options.separator, options.topological, options.OD, options.routes)