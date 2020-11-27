# -*- coding: utf-8 -*-

from printer import Printer
from picamera import PiCamera


camera = PiCamera()
printer = Printer('FC:58:FA:32:69:2D')
camera.capture('pictures/test.jpg')
printer.print('pictures/test.jpg')
