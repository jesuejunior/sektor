# encoding: utf-8
from math import radians, cos, sin, asin, sqrt

from db import DB


class Position:
    def __init__(self, time, lat, lon, speed, distance=0, oil=False):
        self.lat = lat
        self.lon = lon
        self.speed = int(speed)
        self.distance = distance
        self.time = time
        self.oil = oil

    @staticmethod
    def distance(coordinates1: "Position", coordinates2: "Position") -> float:
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians

        lon1, lat1, lon2, lat2 = map(
            radians,
            [
                float(coordinates1.lon),
                float(coordinates1.lat),
                float(coordinates2.lon),
                float(coordinates2.lat),
            ],
        )
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    @staticmethod
    def get_last():
        try:
            result = DB.find_last_position()
            return Position(*result) if result else False
        except Exception as ex:
            print("Exception on Position.get_last()")
            print("Exception: ", ex)
            return False

    def save(self):
        try:
            print("Current distance: ", self.distance)
            return self if DB.save(**self.__dict__) else False
        except Exception as ex:
            print("Exception on Position.save()")
            print("Exception: ", ex)
            return False
