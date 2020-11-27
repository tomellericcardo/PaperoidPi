# -*- coding: utf-8 -*-

from gpiozero import Button
from time import time
from os import system

from printer import Printer
from picamera import PiCamera


printer = Printer('FC:58:FA:32:69:2D')

camera = PiCamera()
camera.rotation = 90

b = Button(12)


while True:
    b.wait_for_press()
    start = time()
    b.wait_for_release()
    stop = time()
    if (stop - start) < 3:
        camera.capture('pictures/test.jpg')
        printer.print('pictures/test.jpg')
    else:
        system('shutdown now')
        break