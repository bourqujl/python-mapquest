.. python-mapquest documentation master file, created by
   sphinx-quickstart on Fri Jun 27 12:57:20 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python-MapQuest 0.1 Documentation
===========================================

**Python-MapQuest** is a python module for interacting with the MapQuest API. 

Versions
--------

* *Version 0.1*: Initial release, includes support for MapQuest geocoding service.

Tutorial
--------

Instances of the **MapQuest** class serve as the main interface to the MapQuest API. Simply initiate a new instance of the class with your MapQuest API key to begin.

Example::

    from mapquest import MapQuest

    mq = MapQuest('mapquest_api_key')

    location = '1555 Blake St,Denver,CO,80202'

    results = mq.geocode(location)

    # process results here

Classes
-------

.. toctree::
   :maxdepth: 2

.. currentmodule:: mapquest

.. autoclass:: MapQuest
   :members:


.. _responses-label:

Responses
---------

Python-MapQuest returns MapQuest API responses as python dictionaries.

Sample Geocoding Input::

    from mapquest import MapQuest

    latlng = [39.7505568, -104.9996268]

    mq = MapQuest('mapquest_developer_api')
    mq.reverse_geocode(latlng)

Sample Geocoding Response::
    
    {u'info': {u'copyright': {u'imageAltText': u'\xa9 2014 MapQuest, Inc.',
                              u'imageUrl': u'http://api.mqcdn.com/res/mqlogo.gif',
                              u'text': u'\xa9 2014 MapQuest, Inc.'},
               u'messages': [],
               u'statuscode': 0},
     u'options': {u'ignoreLatLngInput': False,
                  u'maxResults': -1,
                  u'thumbMaps': True},
     u'results': [{u'locations': [{u'adminArea1': u'US',
                                   u'adminArea1Type': u'Country',
                                   u'adminArea3': u'CO',
                                   u'adminArea3Type': u'State',
                                   u'adminArea4': u'Denver County',
                                   u'adminArea4Type': u'County',
                                   u'adminArea5': u'Denver',
                                   u'adminArea5Type': u'City',
                                   u'displayLatLng': {u'lat': 39.750521,
                                                      u'lng': -104.999724},
                                   u'dragPoint': False,
                                   u'geocodeQuality': u'ADDRESS',
                                   u'geocodeQualityCode': u'L1AAA',
                                   u'latLng': {u'lat': 39.750557,
                                               u'lng': -104.999627},
                                   u'linkId': 0,
                                   u'mapUrl': u'http://open.mapquestapi.com/staticmap/v4/getmap?key=Fmjtd|luur2lu1n0,r2=o5-9a7lgw&type=map&size=225,160&pois=purple-1,39.7505568,-104.9996268,0,0|&center=39.7505568,-104.9996268&zoom=15&rand=939318261',
                                   u'postalCode': u'80202',
                                   u'sideOfStreet': u'N',
                                   u'street': u'1555 Blake Street',
                                   u'type': u's'}],
                   u'providedLocation': {u'latLng': {u'lat': 39.750557,
                                                     u'lng': -104.999627}}}]}

For more information on the response fields, please reference the MapQuest API documentation at `http://open.mapquestapi.com/ <http://open.mapquestapi.com/>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

