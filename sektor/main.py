# encoding: utf-8
from gps3 import gps3
from math import radians, cos, sin, asin, sqrt

from db import DB


class Sektor:

    def start():
        gps_socket = gps3.GPSDSocket()
        gps_stream = gps3.DataStream()

        gps_socket.connect()
        gps_socket.watch()

        for new_data in gps_socket:
            if new_data:
                gps_stream.unpack(new_data)
                location = Sektor.get_locations(gps_stream)

                saved_location = Sektor.save_location(location)

    def get_locations(gps_data):
        if hasattr(gps_data, 'time'):
            print(gps_data.time)

        if hasattr(gps_data, 'speed'):
            return {
                'latitude': gps_data.lat,
                'longitude': gps_data.lon,
                'speed': gps_data.speed,
            }

        return None

    def save_location(gps_data, last_location):
        try:
            distance = Sektor.check_distance(gps_data, last_location)
            saved = DB.save(
                lat=gps_data.lat,
                lon=gps_data.lon,
                speed=gps_data.speed,
                distance=distance,
                oil=distance > 300
            )

            return saved
        except Exception:
            return False

    def do_grease(gps_data):
        pass

    def check_distance(current_location, ):
        pass

    def turn_on_motor(report):
        pass

    def calc_distance(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r


if __name__ == '__main__':
    Sektor.start()
