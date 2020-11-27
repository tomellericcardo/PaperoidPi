# -*- coding: utf-8 -*-

from gpiozero import Button
from time import time
from os import system

from printer import Printer
from picamera import PiCamera


address = 'FC:58:FA:32:69:2D'
button = 12


connected = False
printer = Printer(address)
while not printer.connected:
    printer = Printer(address)

camera = PiCamera()
camera.resolution = (500, 500)


b = Button(button)
while True:
    b.wait_for_press()
    start = time()
    b.wait_for_release()
    stop = time()
    if (stop - start) < 3:
        camera.capture('latest.jpg')
        printer.print('latest.jpg')
    else:
        system('shutdown now')
        break
