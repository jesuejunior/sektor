# encoding: utf-8
import random
import time
from datetime import datetime
from gps3 import gps3
from gpiozero import Button

from db import DB
from position import Position
from turbine import Turbine
from const import HOLD_TIME


class Sektor:
    def track():
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
                    distance_measure += distance_now
                    position.distance = distance_now + last_position.distance

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

    def run():
        DB.init()
        degreaer = Button(21)
        degreaer.wait_for_press(HOLD_TIME)
        oil = Button(13)
        oil.wait_for_press(HOLD_TIME)
        time.sleep(30)

        print("########### degreaer: ", degreaer)
        print("@@@@@@@@@@@ oil: ", oil)

        if oil:
            Turbine.oil()
        if degreaer:
            Turbine.clean()
        else:
            Sektor.track()


if __name__ == "__main__":
    Sektor.run()
