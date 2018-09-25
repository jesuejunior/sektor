import gps
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
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


def get_data(session):

    while True:
        try:
            report = session.next()

            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print report
            if report["class"] == "TPV":
                # if hasattr(report, 'time'):
                #     print(report.time)

                if hasattr(report, "speed"):
                    yield report
                    # print('Latitude {}'.format(report.lat))
                    # print('Longitude {}'.format(report.lon))
                    # print(report.speed * gps.MPS_TO_KPH)

            yield None

        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print("GPSD has terminated")


class Sektor:
    def __init__(self):
        self.session = gps.gps("localhost", "2947")
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        self.gen = get_data(self.session)

        # while

    def start(self):
        pass

    # def __init__(self):
    #     self.gps = serial.Serial('/dev/ttyS0', 9600, timeout=1)

    # def start(self):
    #     while True:
    #         line = self.gps.readline()
    #         print(str(line, 'utf-8', 'ignore'))

    def get_locations(self):
        return

    def save_location(self):
        pass

    def do_grease(self):
        pass

    def check_distance(self):
        haversine()

    def turn_on_motor(self):
        pass


if __name__ == "__main__":
    s = Sektor()
    print(s.get_locations())
