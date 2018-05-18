#!/usr/bin/python3

# this file contains class motor.

# TODO:
# a) class motor
# b) (maybe) class for whole movement(2 motor control)

import logging

from . import misc

class Motor:
    """
    for one-side RPi motor control.
    """

    def __init__(self, port_forward, port_backward, freq=100):
        self.logger = logging.getLogger(__name__)
        self._type = (port_forward, port_backward)
        self.pwm_forward = misc.getpwm(port_forward, freq)
        self.pwm_backward = misc.getpwm(port_backward, freq)
        self.currentspeed = 0
        self.pwm_forward.start(0)
        # self.pwm_backward.start(0)
        self.logger.info(
            "Class Motor(f:%d, b:%d) created at freq %d.",
            port_forward, port_backward, freq
        )


    # may unsafe in multi-threading
    def set_speed(self, speed):
        """
        set oneside speed by control the dutycycle.
        speed ranges from -100 to 100
        """
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        self.logger.info("Motor(f:%d, b:%d) changes to speed %d",
                         *self._type, speed)
        if self.currentspeed >= 0:
            # now forward is on
            if speed >= 0:
                # direct control
                self.pwm_forward.ChangeDutyCycle(speed)
            else:
                # switch open condition
                self.pwm_forward.stop()
                self.pwm_backward.start(-speed)
        else:
            #neg as above
            if speed < 0:
                # direct control
                self.pwm_backward.ChangeDutyCycle(-speed)
            else:
                # switch open condition
                self.pwm_backward.stop()
                self.pwm_forward.start(speed)
        self.currentspeed = speed
        self.logger.info("Motor speed change finished.")


    def stop(self):
        """
        totally stop everything.
        Must call restart before use.
        """
        self.logger.info("Motor(f:%d, b:%d) halts.",
                         *self._type)
        self.pwm_forward.stop()
        self.pwm_backward.stop()


    def restart(self):
        """
        just re-initialize this object.
        """
        self.currentspeed = 0
        port_forward, port_backward = self._type
        misc.GPIO.cleanup(port_forward)
        misc.GPIO.cleanup(port_backward)
        self.pwm_forward = misc.getpwm(port_forward, self.freq)
        self.pwm_backward = misc.getpwm(port_backward, self.freq)
        self.pwm_forward.start(0)


