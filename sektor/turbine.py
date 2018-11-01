# encoding: utf-8
import time
from gpiozero import PWMOutputDevice


class Turbine:
    def clean():
        # PARAMS:  pin, *, active_high=True, initial_value=0, frequency=100, pin_factory=None
        print("Starting cleaning time")
        with PWMOutputDevice(04) as motor:
            motor.on()
            time.sleep(10)
            motor.off()

    def oil():
        print("Starting oil on the chain")
        with PWMOutputDevice(17) as motor:
            motor.on()
            time.sleep(10)
            motor.off()
