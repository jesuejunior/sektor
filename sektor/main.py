import gps
from math import radians, cos, sin, asin, sqrt

from .db import DB


class Sektor:

    def start():
        session = gps.gps('localhost', '2947')
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        while True:
            try:
                report = session.next()
                location = Sektor.get_locations(report)

            except KeyError:
                pass
            except KeyboardInterrupt:
                quit()
            except StopIteration:
                session = None
                print("GPSD has terminated")

    def get_locations(report):
        if report['class'] == 'TPV':
            if hasattr(report, 'speed'):
                return {
                    'latitude': report.lat,
                    'longitude': report.lon,
                    'speed': report.speed,
                }
        return None

    def save_location(report):
        DB.save(latitude=report)

    def do_grease(report):
        pass

    def check_distance(report):
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
