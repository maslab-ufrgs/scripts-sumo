'''
Created on 08/04/2013

@authors: Cristiano Galafassi, Gabriel Ramos, Rodrigo Batista
'''
import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser
from igraph import *
import sumolib
import sys, getopt
debug = True

def printdebug(arr):
    for a in arr:
        print a

def writefile(names, bet, out_file, separator):
    #Generate the output file
    out = open(out_file, 'w')
    out.write('#Edge' + separator + 'Betweenness\n')
    
    #Print values to file
    if len(names) != len(bet):
        print "ERRO - Betweenness length differs from names length!"
    else:
        for i in range(0,len(names)-1):
            out.write(str(names[i]) + separator + str(bet[i]) + '\n')
    
    #Close file
    out.close()

def calc_Betweenness(network_file, routes_file, out_file, separator, topological, OD, routes, weighted):
    
    #Load the network file
    roadnetwork = sumolib.net.readNet(network_file)
    roadnetwork_edges = roadnetwork.getEdges()
    roadnetwork_nodes = roadnetwork.getNodes()
    
    #Initialize some variables
    nodes = []
    node_names = []
    edges = []
    edge_weights = []    
    edge_names = []
    
    #Read edges from the network file
    for e in roadnetwork_edges:
        edges += [(e.getFromNode().getID(), e.getToNode().getID())]
        edge_names += [e.getID()]
        
        if weighted:
            #If edge does not have any lanes, put constant weight
            if e.getLaneNumber()==0:
                edge_weights += [1]
            else:
                edge_weights += [e.getLength() / e.getLaneNumber()]
        else:
            edge_weights += [1]
            
    #Read nodes from the network file
    for n in roadnetwork_nodes:
        nodes += [n]
        node_names += [n.getID()]
    
    if debug:
        print "NODES:"
        printdebug(nodes)
        printdebug(node_names)
        print "EDGES:"
        printdebug(edges)
        printdebug(edge_names)
        printdebug(edge_weights)

    #Load igraph graph structure
    g = Graph(directed = True)
    for n in nodes:
        g.add_vertex(n.getID())
    
    g.add_edges(edges)
    g.es["name"] = edge_names
    g.es["weight"] = edge_weights

    if debug:
        print "EDGES IGRAPH"
        printdebug(g.get_edgelist())
        print "EDGES IGRAPH NAMES"
        printdebug(g.es["name"])
        #Print betweenness edge information        
        print "edge - betweenness"
        #If --weighted is false, then is weight=1 otherwise wieght=length/lanesnumber
        print g.edge_betweenness(directed=True, cutoff=None, weights=g.es["weight"])
    
    if topological:
        bT = g.edge_betweenness(directed=True, cutoff=None, weights=g.es["weight"])
    
    if OD or routes:
        infile = ET.parse(routes_file)
        table = {}
        
        #initialize table with edges 
        for edge in g.es["name"]:
            table[edge] = [1, 0, 0]
        
        #count the number of times each edge appears in a route/OD pair
        for vehicle in infile.getroot():
            route = vehicle[0].get('edges').split(' ')
            for element in range(len(route)):
                edge = route[element]
                sumOD = 1 if element in [0,len(route)-1] else 0 
                table[edge] = [1, table[edge][1]+1, table[edge][2]+sumOD]
        
        #calculate betweenness
        wlR = [1]*len(g.es["name"])
        wlOD = [1]*len(g.es["name"])
        for e in range(len(g.es["name"])):
            edge = g.es["name"][e]
            if edge in table:
                wlR[e] = table[edge][0] + table[edge][1]
                wlOD[e] = table[edge][0] + table[edge][2]
        bR = g.edge_betweenness(directed=True, cutoff=None, weights=wlR)
        bOD = g.edge_betweenness(directed=True, cutoff=None, weights=wlOD)
        
    #Print topological betweenness
    out = out_file+'.topological.csv'
    if topological:
        writefile(g.es["name"], bT, out, separator)
    
    if OD:
        writefile(g.es["name"], bOD, out_file+'.od.csv', separator)
    
    if routes:
        writefile(g.es["name"], bR, out_file+'.routes.csv', separator)
    

    
if __name__ == '__main__':
    optParser = OptionParser()
    
    optParser.add_option("-n", "--network-file", dest='networkfile',
                            help="sumo network file (mandatory)")
    optParser.add_option("-r", "--routes-file", dest='routesfile',
                            help="the routes file to which the betweenness should be calculated")
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
    optParser.add_option("-W", "--weighted", default=False, action="store_true",
                            help="Weighted: Length / LaneNumber. Else 1 ")
    
    
    (options, args) = optParser.parse_args()
    
    if options.networkfile == None:
        print "The network file must be informed"
        sys.exit() 

    if (options.OD or options.routes) and options.routesfile == None:
        print "The routes file must be informed"
        sys.exit()
    
    if not options.topological and  not options.OD and not options.routes:
        print "Specify at least one type of analysis (topological, OD pairs, routes)"
        sys.exit()
    
    
    calc_Betweenness(options.networkfile, options.routesfile, options.csvfile, options.separator, options.topological, options.OD, options.routes, options.weighted)
