import urllib2

import xml.etree.ElementTree as ET

from math import radians, cos, sin, asin, sqrt


class TrafficFeed(object):

    def __init__(self, url):
        self.feed_url = url
        self.xml = ET.fromstring(self.get_data(url)).find("channel")


    def get_data(self, url):
        """Make a request and return the response
        """
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()


    def items_within(self, distance, longitude, latitude):
        """Return traffic items with a certain distance

        Args:
            distance (int): The maximum distance in km.

        Returns:
            (list): A list of xml elements
        """
        results = []
        for item in self.xml.findall("item"):
            try:
                item_long = float(item.find("longitude").text)
                item_lat = float(item.find("latitude").text)
            except ValueError:
                pass
            diff = self.haversine(item_long,
                                  item_lat,
                                  longitude,
                                  latitude)
            if diff <= distance:
                results.append(item)
        return results


    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km
