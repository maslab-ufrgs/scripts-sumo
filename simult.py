'''
Makes all drivers have the same depart time.

Receives 3 args: the input.rou.xml file, the output.rou.xml file and the depart time

'''

import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()

for element in root:
    element.set('depart',sys.argv[3] or '0.00')
    
    
tree.write(sys.argv[2])
