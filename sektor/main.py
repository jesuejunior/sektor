# encoding: utf-8
import random
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
from gps3 import gps3

from db import DB


def fake_data():
    while True:
        yield {
            "lat": random.random(),
            "lon": random.random(),
            "speed": random.random(),
            "time": datetime.now(),
        }


class Position:
    def __init__(self, lat, lon, speed, time, distance=0, oil=False):
        self.lat = lat
        self.lon = lon
        self.speed = int(speed)
        self.distance = distance
        self.time = time
        self.oil = oil

    @staticmethod
    def calc_distance(coordinates1: "Position", coordinates2: "Position") -> float:
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

    def save(self, last_location):
        try:
            distance = Position.calc_distance(self, last_location)
            self.distance = distance
            self.oil = Sektor.do_grease(distance, self.speed)
            return self if DB.save(**self.__dict__) else False
        except Exception as ex:
            print("Exception: ", ex)
            return False


class Sektor:
    def start():
        DB.init()
        gps_socket = gps3.GPSDSocket()
        data = gps3.DataStream()

        gps_socket.connect()
        gps_socket.watch()

        last_position = Position(lat=0, lon=0, speed=0, time=0)

        # TO-DO: Will it work forever?
        for new_data in gps_socket:
            if new_data:
                print("getting new data...")
                # import ipdb
                # ipdb.set_trace()
                data.unpack(new_data)
                if isinstance(data.TPV.get("lat"), float) and isinstance(
                    data.TPV.get("lon"), float
                ):
                    position = Position(
                        data.TPV["lat"],
                        data.TPV["lon"],
                        data.TPV["speed"],
                        data.TPV["time"],
                    )
                    saved_location = position.save(last_position)
                    if saved_location:
                        last_position = Position(**saved_location.__dict__)
                print("Done")

    def do_grease(distance, speed):
        if distance > 300 and speed <= 20:
            Sektor.turn_on_motor()
            return True
        else:
            return False

    def turn_on_motor():
        print("Starting motor 1")
        return False


if __name__ == "__main__":
    Sektor.start()
