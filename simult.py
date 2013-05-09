'''
Makes all drivers have the same depart time.

Receives 3 args: the input.rou.xml file, the output.rou.xml file and the depart time

Last parameter is defaulted to 0.00 if omitted
'''

import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()
depart_time = sys.argv[3] if len(sys.argv) >= 4 else '0.00'

for element in root:
    element.set('depart', depart_time)
    
    
tree.write(sys.argv[2])
