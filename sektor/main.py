# encoding: utf-8
from gps3 import gps3
from math import radians, cos, sin, asin, sqrt

from db import DB


def clear_screen():
    print(chr(27) + '[2j')
    # print('\033c')
    # print('\x1bc')


class Sektor:

    def start():
        gps_socket = gps3.GPSDSocket()
        gps_stream = gps3.DataStream()

        gps_socket.connect()
        gps_socket.watch()

        old_location = {'lat': 0, 'lon': 0}

        for new_data in gps_socket:
            if new_data:
                print('getting new data...')
                gps_stream.unpack(new_data)
                current_location = Sektor.get_locations(gps_stream)

                saved_location = Sektor.save_location(
                    current_location,
                    old_location
                )

                if saved_location:
                    old_location['lat'] = current_location['lat']
                    old_location['lon'] = current_location['lon']

            clear_screen()

    def get_locations(gps_data):
        print('ta chegando aqui')
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
            distance = Sektor.calc_distance(gps_data, last_location)
            saved = DB.save(
                lat=gps_data.lat,
                lon=gps_data.lon,
                speed=gps_data.speed,
                distance=distance,
                oil=Sektor.do_grease(gps_data)
            )

            return saved
        except Exception:
            return False

    def do_grease(gps_data, last_location):
        gps_data.lat

    def turn_on_motor(report):
        pass

    def get_last_location():
        return 2

    def calc_distance(coordinates1, coordinates2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [
            coordinates1['lon'],
            coordinates1['lat'],
            coordinates2['lon'],
            coordinates2['lat']
        ])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r


if __name__ == '__main__':
    Sektor.start()
