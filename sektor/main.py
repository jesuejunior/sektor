# encoding: utf-8
import random
from datetime import datetime
from gps3 import gps3

from db import DB
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
        DB.init()
        gps_socket = gps3.GPSDSocket()
        data = gps3.DataStream()

        gps_socket.connect()
        gps_socket.watch()

        last_position = Position.get_last()

        last_position = last_position if last_position else Position(
            lat=0, lon=0, speed=0, time=0
        )

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
                        lat=data.TPV["lat"],
                        lon=data.TPV["lon"],
                        speed=data.TPV["speed"],
                        time=data.TPV["time"],
                    )
                    distance = Position.calc_distance(position, last_position)

                    position.distance = distance + last_position.distance
                    oil = Sektor.do_grease(distance, position.speed)
                    position.oil = oil

                    position.save()

                    last_position = Position(**position.__dict__)

                    last_position.distance += distance
                    # print("Vindo do last position")
                    # print(last_position.distance)

                    # if saved_location:
                    #     # last_position.distance +=

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
