# encoding: utf-8
import random
from datetime import datetime
from gps3 import gps3

from position import Position


def fake_data():
    while True:
        yield {
            "lat": random.random(),
            "lon": random.random(),
            "speed": random.random(),
            "time": datetime.now(),
        }


class Sektor:
    def start():
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
                    distance = Position.calc_distance(position, last_position)
                    oil = Sektor.do_grease(distance, position.speed)
                    position.oil = oil
                    saved_location = position.save()
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
