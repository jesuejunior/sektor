# encoding: utf-8
from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
import traceback

from db import DB


class GPS:
    def __init__(
            self, lat, lon,
            speed, time, distance=0,
            oil=False
    ):
        self.lat = lat
        self.lon = lon
        self.speed = speed
        self.distance = distance
        self.time = time
        self.oil = oil

    def get_locations(gps_data):
        if "time" in gps_data:
            print(gps_data["time"])

        if "speed" in gps_data:
            return GPS(
                lat=gps_data["lat"],
                lon=gps_data["lon"],
                speed=gps_data["speed"],
                time=gps_data["time"],
            )

        return None

    def calc_distance(coordinates1: 'GPS', coordinates2: 'GPS') -> float:
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
                float(coordinates2.lat)
            ],
        )
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def save_location(gps_data, last_location):
        try:
            distance = GPS.calc_distance(gps_data, last_location)
            speed = int(gps_data.speed)

            location_data = {
                "time": gps_data.time,
                "lat": gps_data.lat,
                "lon": gps_data.lon,
                "speed": speed,
                "distance": distance,
                "oil": Sektor.do_grease(distance, speed),
            }

            return GPS(**location_data) if DB.save(**location_data) else False
        except Exception as err:
            print('Could not save on database')
            traceback.print_exc()
            return False


class Sektor:
    def start():
        DB.init()
        gps_socket = gps3.GPSDSocket()
        gps_stream = gps3.DataStream()

        gps_socket.connect()
        gps_socket.watch()

        old_location = GPS(lat=0, lon=0, speed=0, time=0)

        # TO-DO: Will it work forever?
        for new_data in gps_socket:
            if new_data:
                print("getting new data...")
                # import ipdb
                # ipdb.set_trace()
                gps_stream.unpack(new_data)
                current_location = GPS.get_locations(gps_stream.TPV)
                # FIX-ME: Move to GPS class
                saved_location = GPS.save_location(current_location, old_location)

                if saved_location:
                    old_location = GPS(**saved_location.__dict__)

    def do_grease(distance, speed):
        if distance > 300 and speed <= 20:
            Sektor.turn_on_motor()
            return True
        else:
            return False

    def turn_on_motor():
        return False


if __name__ == "__main__":
    Sektor.start()
