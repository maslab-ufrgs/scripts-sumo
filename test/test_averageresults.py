'''
Created on May 6, 2013

@author: anderson
'''
import unittest
import sys, os
sys.path.append(os.path.join('..'))

import averageresults

class Test(unittest.TestCase):


    def test_full_trips_in_window(self):
        '''
        Uses the sample_tripinfo.xml file
        According to it, drivers data are:
        1st: id=aux69 depart=15 arrival=150 duration=135.00
        2nd: id=aux314 depart=64 arrival=181 duration=117.00
        3rd: id=aux422 depart=86 arrival=181 duration=95.00
        
        '''
        #gets all drivers
        ftrips = averageresults.full_trips_in_window(15, 181, 'sample_tripinfo_000.xml')
        self.assertEqual(['aux69', 'aux314', 'aux422'], ftrips)
        
        #gets first driver
        ftrips = averageresults.full_trips_in_window(15, 180, 'sample_tripinfo_000.xml')
        self.assertEqual(['aux69'], ftrips)
        
        #gets 2nd and 3rd driver
        ftrips = averageresults.full_trips_in_window(64, 181, 'sample_tripinfo_000.xml')
        self.assertEqual(['aux314', 'aux422'], ftrips) 
        
        #gets 3rd driver
        ftrips = averageresults.full_trips_in_window(86, 181, 'sample_tripinfo_000.xml')
        self.assertEqual(['aux422'], ftrips) 
        
        #gets no driver (finish is earlier than drivers' finish)
        ftrips = averageresults.full_trips_in_window(0, 149, 'sample_tripinfo_000.xml')
        self.assertEqual([], ftrips) 
        
        #gets no driver (start is later than drivers' start)
        ftrips = averageresults.full_trips_in_window(87, 181, 'sample_tripinfo_000.xml')
        self.assertEqual([], ftrips) 
        
    def test_averageresults(self):
        '''
        Uses the sample_tripinfo file
        
        '''
        #creates an option object, it is an instance from a new class
        options = type('', (), {})
        options.output = 'result.csv'
        options.begin = 64  #with these values of begin/end 
        options.end = 181   #2nd and 3rd vehicles will be averaged
        options.fields = 'duration'
        options.prefix = 'sample_tripinfo_'
        options.iterations = 1
        options.separator = ','
        
        averageresults.average_results(options)
        
        f = open('result.csv')
        fstring = f.read()
        
        estring = '#it,duration\n1,106.0\n'
        
        self.assertEqual(estring, fstring)
        
    def test_averageresults_without_timewindow(self):
        '''
        Uses the sample_tripinfo file
        
        '''
        #creates an option object, it is an instance from a new class
        options = type('', (), {})
        options.output = 'result-now.csv'
        options.fields = 'duration'
        options.prefix = 'sample_tripinfo_'
        options.iterations = 1
        options.separator = ','
        options.begin = 0
        options.end = 0
        
        averageresults.average_results(options)
        
        f = open('result-now.csv')
        fstring = f.read()
        
        estring = '#it,duration\n1,115.666666667\n'
        
        self.assertEqual(estring, fstring)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFullTripsInWindow']
    unittest.main()