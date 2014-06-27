# -*- coding: utf-8 -*-
#
# Copyright 2014 Joshua Bourquin
#
# This file is part of python-mapquest.
#
# python-mapquest is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# python-mapquest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-mapquest.  If not, see <http://www.gnu.org/licenses/>.

#<----------------------------------------------------------------------------->

import sys
import argparse
import unittest

from mapquest import MapQuest
from pprint import pprint

#<----------------------------------------------------------------------------->

API_KEY = ''

#<----------------------------------------------------------------------------->

class TestMapQuest(unittest.TestCase):

    def setUp(self):
        self.mq = MapQuest(API_KEY)

    #<------------------------------------------------------------------------->

    def test_geocode(self):

        # test the string query format
        address = '1555 Blake St,Denver,CO,80202'
        address_results = self.mq.geocode(address)
        address_results_count = len(address_results['results'][0]['locations'])

        print('\nGeocode Query:\n{}\n\nGeocode Results:'.format(address))
        pprint(address_results)

        # test the dictionary query format
        address_dict = {
            'street': '1555 Blake St',
            'city': 'Denver',
            'state': 'CO',
            'postalCode': '80202'
        }
        address_dict_results = self.mq.geocode(address_dict)
        address_dict_results_count = len(address_dict_results['results'][0]['locations'])

        print('\nGeocode Query:\n{}\n\nGeocode Results:'.format(address_dict))
        pprint(address_dict_results)

        self.assertEqual(address_results_count, address_dict_results_count)

    #<------------------------------------------------------------------------->

    def test_reverse_geocode(self):
        
        # test the string query format
        latlng = '39.7505568,-104.9996268'
        latlng_results = self.mq.reverse_geocode(latlng)
        latlng_results_count = len(latlng_results['results'][0]['locations'])

        print('\nReverse Geocode Query:\n{}\n\nReverse Geocode Results:'.format(latlng))
        pprint(latlng_results)

        # test the list/tuple query format
        latlng_list = [39.7505568,-104.9996268]
        latlng_list_results = self.mq.reverse_geocode(latlng_list)
        latlng_list_results_count = len(latlng_list_results['results'][0]['locations'])

        print('\nReverse Geocode Query:\n{}\n\nReverse Geocode Results:'.format(latlng_list))
        pprint(latlng_list_results)

        self.assertEqual(latlng_results_count, latlng_list_results_count)

    def test_batch_geocode(self):
        
        # test the string list query format
        addresses = [
            '1555 Blake St,Denver,CO,80202',
            '2590 Pearl St,Boulder,CO,80302'
        ]
        addresses_results = self.mq.batch_geocode(addresses)
        addresses_results_count = len(addresses_results['results'])

        print('\nBatch Geocode Query:\n{}\n\nBatch Geocode Results:'.format(addresses))
        pprint(addresses_results)

        # test the dictionary list query format
        addresses_dict = [
            {
                'street': '1555 Blake St',
                'city': 'Denver',
                'state': 'CO',
                'postalCode': '80202'
            },
            {
                'street': '2590 Pearl St',
                'city': 'Boulder',
                'state': 'CO',
                'postalCode': '80302'
            }
        ]
        addresses_dict_results = self.mq.batch_geocode(addresses_dict)
        addresses_dict_results_count = len(addresses_dict_results['results'])

        print('\nBatch Geocode Query:\n{}\n\nBatch Geocode Results:'.format(addresses_dict))
        pprint(addresses_dict_results)

        self.assertEqual(addresses_results_count, addresses_dict_results_count)

    def test_geocode_options(self):

        # specify the location
        location = 'Red Lion, DE'
        
        # specify the bounding box
        box = [39.715056,-75.811158,39.5098,-75.491781]
        
        # fetch the results
        results = self.mq.geocode(location, limit=1, thumbnails=False, bounding_box=box)

        print('\nGeocode Options Query:\n{}\n\nGeocode Options Bounding Box:\n{}\n\nGeocode Options Results:'.format(location, box))
        pprint(results)

        self.assertEqual(results['options']['thumbMaps'], False)
        self.assertEqual(len(results['results'][0]['locations']), 1)

#<----------------------------------------------------------------------------->

if __name__ == '__main__':
    
    # Parse the command line for a MapQuest Api key
    parser = argparse.ArgumentParser()
    parser.add_argument('key')
    parser.add_argument('unittest_args', nargs='*')
    
    args = parser.parse_args()

    # Update the golbal api key
    API_KEY = args.key

    # Remove the key argument from the command line options 
    sys.argv[1:] = args.unittest_args

    # Run the unittests
    unittest.main()
