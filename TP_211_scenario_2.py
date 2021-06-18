#!/usr/bin/python3
#  -*- coding: utf-8 -*-

# Author: Emilio Profili
# Creation date : 13/06/2021
# Last updated by: Emilio Profili
# Last updated date: Sun 13 jun 2021 18:30:00 CEST
# Description : TP211 senario 2


import time
import board
import analogio
import simpleio
import pwmio
from adafruit_motor import servo


x1 = pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
x2 = pwmio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
servo1 = servo.Servo(x1)
servo2 = servo.Servo(x2)

light1 = analogio.AnalogIn(board.LIGHT)


def move_up(servo):

    my_servo = servo
    my_servo.angle += 5

    """
    move_up() is a fonction that adds 5 deg
    to the angle of a servo.
    Parameters (Input Variables):
        servo :
            servo object that you want to move up.
    Output:
        moves the chosen servo.
    Dependencies:
        adafruit_motor
        servo
    """


def move_down(servo):

    my_servo = servo
    my_servo.angle -= 5

    """
    move_down() is a fonction that substract 5 deg to the angle of a servo.
    Parameters (Input Variables):
        servo :
            servo object that you want to move down.
    Output:
        moves the chosen servo.
    Dependencies:
        adafruit_motor
        servo
    """

while True:
    hight = simpleio.map_range(light1.value, 0, 320, 0, 10)
    print(int(hight))

    for i in range(0, 10, 1):
        if i <= hight:
            move_up(servo1)
            move_down(servo2)

    time.sleep(0.01)
