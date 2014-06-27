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

from __future__ import unicode_literals
from __future__ import absolute_import

__version__ = '0.1'

#<----------------------------------------------------------------------------->

import json

try: 
    from urllib.parse import urlencode, unquote
except ImportError: 
    from urllib import urlencode, unquote

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

try:
    from urllib.parse import urlunparse
except ImportError:
    from urlparse import urlunparse

#<----------------------------------------------------------------------------->

MAPQUEST_API_URLS = {
    'netloc': {
        'licensed': 'www.mapquestapi.com',
        'open': 'open.mapquestapi.com',
    },
    'path': {
        'geocode': '/geocoding/v1/address',
        'reverse_geocode': '/geocoding/v1/reverse',
        'batch_geocode': '/geocoding/v1/batch',
    },
}

#<----------------------------------------------------------------------------->

class MapQuest(object):
    """
    Toplevel class for interacting with the MapQuest developer API.
    
    :param str key: MapQuest developer API key.
    :param str data: Specifies which MapQuest data to use. Options are either 'open' or 'licensed'.
    :param bool ssl: Specifies whether to use Secure Socket Layer (SSL) when fetching data from the MapQuest API (i.e. http vs https).
    :param int timeout: Specifies how long the http request should wait (in seconds) for a response before timing out.
    :param dict headers: Allows for the modification of the http request headers (i.e. specify a custom User-Agent).

    Usage::

        from mapquest import MapQuest
        mq = MapQuest('mapquest_api_key')

    Methods:
    """

    def __init__(self, key, data='open', ssl=False, timeout=60, headers={}):
        super(MapQuest, self).__init__()
        
        # mapquest api key
        self.key = unquote(key) if '%' in key else key

        # mapquest data, options [open, licensed]
        self.data = 'licensed' if data == 'licensed' else 'open'
        
        # optional request parameters
        self.timeout = timeout
        self.headers = headers
        self.ssl = ssl

    #<------------------------------------------------------------------------->

    def _fetch(self, type, query):

        # build the url attributes
        scheme = 'https' if self.ssl else 'http'
        netloc = MAPQUEST_API_URLS['netloc'][self.data]
        path = MAPQUEST_API_URLS['path'][type]

        # convert query dictionary to a url encoded string
        query = urlencode(query)

        # build the url
        url = urlunparse((scheme, netloc, path, '', query, ''))

        # build the request object
        request = Request(url, headers=self.headers)
        
        # fetch the response
        response = urlopen(request, timeout=self.timeout)

        return response

    #<------------------------------------------------------------------------->

    def _geocode(self, type, location, limit=-1, thumbnails=True, bounding_box=[]):

        # build the json query
        json_query = {}

        # build the options dictionary
        options = {}

        if limit != -1:
            options['maxResults'] = limit

        if not thumbnails:
            options['thumbMaps'] = thumbnails
        
        if bounding_box:
            
            if isinstance(bounding_box, str):
                bounding_box = [float(i) for i in bounding_box.split(',')]

            bbox = {
                'ul': {
                    'lat': bounding_box[0],
                    'lng': bounding_box[1],
                },
                'lr': {
                    'lat': bounding_box[2],
                    'lng': bounding_box[3],
                }
            }

            options['boundingBox'] = bbox

        # add the options dictionary to the json query if present
        if options:
            json_query['options'] = options

        # build the location dictionary
        if type == 'reverse_geocode':

            if isinstance(location, str):
                location = [float(i) for i in location.split(',')]
            
            loc = {
                'latLng': {
                    'lat': location[0],
                    'lng': location[1],
                }
            }

            json_query['location'] = loc

        elif type == 'batch_geocode':
            locations = [{'street': loc} if isinstance(loc, str) else loc for loc in location]
            json_query['locations'] = locations

        else:

            if isinstance(location, str):
                location = {'street': location}

            json_query['location'] = location

        # build the key, value pairs for the query
        query = (
            ('key', self.key),
            ('inFormat', 'json'),
            ('outFormat', 'json'),
            ('json', json.dumps(json_query)),
        )
        
        # fetch the results from mapquest and convert them to a python dictionary
        response = self._fetch(type, query)
        response = json.loads(response.read().decode('utf-8'))

        return response

    #<------------------------------------------------------------------------->

    def geocode(self, location, limit=-1, thumbnails=True, bounding_box=[]):
        """
        Fetchs geocode data for a specified address. Useful for finding the 
        relative latitude and longitude of an address.

        :param location: The address the geocoder should look up.
        :type location: str or dict 
        :param int limit: Limits the number of results returned by the geocoder service. Specify -1 for unlimited results.
        :param bool thumbnails: Specifies whether the geocoder service should return a URL to a map thumbnail image in the results for the location being geocoded.
        :param bounding_box: Moves any locations within the bounding box to the top of the results list when ambiguous results are returned (i.e. the provided address coresponds to multiple locations). See Bounding Boxes for more info.
        :type bounding_box: list or tuple

        The **location** may be specified as either a string or dictionary as follows::

            location = '1555 Blake St,Denver,CO,80202'

            location = {
                'street': '1555 Blake St',
                'city': 'Denver',
                'state': 'CO',
                'postalCode': '80202'
            }

        :returns: :ref:`MapQuest Geocode Response <responses-label>`
        """

        return self._geocode('geocode', location, limit, thumbnails, bounding_box)

    #<------------------------------------------------------------------------->

    def reverse_geocode(self, location, limit=-1, thumbnails=True, bounding_box=[]):
        """
        Fetchs geocode data for a specified latitude and longitude.Useful for 
        finding the relative address of a latitude and longitude.

        :param location: The latitude and longitude the geocoder should look up.
        :type location: str, list, or tuple 
        :param int limit: Limits the number of results returned by the geocoder service. Specify -1 for unlimited results.
        :param bool thumbnails: Specifies whether the geocoder service should return a URL to a map thumbnail image in the results for the location being geocoded.
        :param bounding_box: Moves any locations within the bounding box to the top of the results list when ambiguous results are returned (i.e. the provided address coresponds to multiple locations). See Bounding Boxes for more info.
        :type bounding_box: list or tuple

        The **location** may be specified as either a string or list as follows::

            location = '39.7505568,-104.9996268'

            location = [39.7505568,-104.9996268]

        :returns: :ref:`MapQuest Geocode Response <responses-label>`
        """

        return self._geocode('reverse_geocode', location, limit, thumbnails, bounding_box)

    #<------------------------------------------------------------------------->

    def batch_geocode(self, locations, limit=-1, thumbnails=True, bounding_box=[]):
        """
        Fetchs the geocode data for multiple addresses. Useful for finding the 
        relative latitude and longitude of multiple addresses.

        :param locations: A list of addresses the geocoder should look up.
        :type locations: list or tuple 
        :param int limit: Limits the number of results returned by the geocoder service per address. Specify -1 for unlimited results.
        :param bool thumbnails: Specifies whether the geocoder service should return a URL to a map thumbnail image in the results for the location being geocoded.
        :param bounding_box: Moves any locations within the bounding box to the top of the results list. See Bounding Boxes for more info.
        :type bounding_box: list or tuple

        **Locations** may be specified as either a list of strings or a list of dictionaries as follows::

            locations = [
                '1555 Blake St,Denver,CO,80202',
                '2590 Pearl St,Boulder,CO,80302'
            ]

            locations = [
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

        :returns: :ref:`MapQuest Geocode Response <responses-label>`
        """

        return self._geocode('batch_geocode', locations, limit, thumbnails, bounding_box)

