import serial


class Sektor:

    def __init__(self):
        self.gps = serial.Serial('/dev/ttyS0', baudrate=9600)

    def start(self):
        print(self.gps)

    def get_locations(self):
        pass

    def save_location(self):
        pass

    def do_grease(self):
        pass

    def check_distance(self):
        pass

    def turn_on_motor(self):
        pass


if __name__ == '__main__':
    s = Sektor()
    s.start()
