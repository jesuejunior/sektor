# encoding: utf-8
import random
from datetime import datetime
from gps3 import gps3

from db import DB
from position import Position
from turbine import Turbine


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

        distance_measure = 0

        last_position = (
            last_position if last_position else Position(lat=0, lon=0, speed=0, time=0)
        )

        for new_data in gps_socket:
            if new_data:
                print("getting new data...")
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
                    distance_now = Position.distance(position, last_position)

                    position.distance = distance_now + last_position.distance
                    distance_measure += distance_now

                    position.oil = Sektor.do_grease(distance_now, position.speed)

                    if distance_measure >= 45 and distance_measure <= 55:
                        distance_measure = 0
                        print("Saved for ~50 meters")
                        position.save()

                    last_position = Position(**position.__dict__)

                print("Done")

    def do_grease(distance, speed):
        # 300000 is 300KM
        if (distance % 300000 == 0) and speed <= 30:
            Turbine.oil()
            return True
        else:
            return False


if __name__ == "__main__":
    Sektor.start()
