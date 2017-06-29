'''

rc.py

A pilot using RC control

'''

import os
import math
import random
import time
from operator import itemgetter
from datetime import datetime
from pilots import BasePilot

from navio import rcinput, pwm, leds, util, mpu9250

import methods, config

util.check_apm()


class RC(BasePilot):
    def __init__(self, **kwargs):

        self.rcin = rcinput.RCInput()

        self.led = leds.Led()

        self.throttle_center = 1500
        self.yaw_center = 1500
        self.calibrated = False

        super(RC, self).__init__(**kwargs)

    def decide(self, img_arr):

        if float(self.rcin.read(config.ARM_CHANNEL)) > 1490:
            if not self.calibrated:
                self.calibrate_rc(self.rcin)

            self.led.setColor('Green')
            rc_pos_throttle = float(self.rcin.read(config.THROTTLE_CHANNEL))
            rc_pos_yaw = float(self.rcin.read(config.YAW_CHANNEL))

            throttle = (rc_pos_throttle - self.throttle_center) / 500.0
            yaw = (rc_pos_yaw - self.yaw_center) / 500.0
        else:

            self.led.setColor('Blue')
            throttle = 0
            yaw = 0
            self.calibrated = False

        return methods.yaw_to_angle(yaw), throttle

    def calibrate_rc(self, rcin):

        print("Please center your receiver sticks")
        self.led.setColor('Cyan')
        time.sleep(2.00)

        print("Calibrating RC Input...")
        self.led.setColor('Magenta')
        yaw = 0
        throttle = 0

        for x in range(0, 100):
            yaw += float(rcin.read(config.YAW_CHANNEL))
            throttle += float(rcin.read(config.THROTTLE_CHANNEL))

            time.sleep(0.02)

        yaw /= 100.0
        throttle /= 100.0

        self.throttle_center = throttle
        self.yaw_center = yaw

        self.calibrated = True

        print("Done")

    def pname(self):
        return "RC"
