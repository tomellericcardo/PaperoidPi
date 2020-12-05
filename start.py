# -*- coding: utf-8 -*-

from gpiozero import Button
from printer import Printer
from picamera import PiCamera

from datetime import datetime
from time import sleep
from os import system


PATH = '/home/pi/PaperoidPi'
PRINTER_MAC = 'FC:58:FA:32:69:2D'
BUTTON_GPIO = 12


class Paperoid:

    def __init__(self, path, printer_mac, button_gpio):
        self.path = path
        self.stopping = False
        self.camera_connected = False
        self.init_button(button_gpio)
        self.connect_printer(printer_mac)
        self.start_camera()

    def init_button(self, button_gpio):
        self.button = Button(button_gpio, hold_time = 3)
        self.button.when_held = self.shutdown
        self.button.when_released = self.shoot

    def connect_printer(self, printer_mac):
        self.printer = Printer(printer_mac)
        while not self.printer.connected:
            sleep(5)
            self.printer = Printer(printer_mac)
        path = '%s/pictures/placeholder.jpg' % self.path
        self.printer.init_converter(path)

    def start_camera(self):
        self.camera = PiCamera()
        self.camera.resolution = (720, 720)
        self.camera.rotation = 90
        self.camera.start_preview()
        self.camera_connected = True

    def shoot(self):
        if self.printer.connected and not self.stopping:
            timestamp = datetime.now().isoformat()
            path = '%s/pictures/%s.jpg' % (self.path, timestamp)
            self.camera.capture(path)
            self.printer.print(path)

    def stop(self):
        self.stopping = True
        if self.printer.connected:
            self.printer.disconnect()
        if self.camera_connected:
            self.camera.stop_preview()
            self.camera.close()

    def shutdown(self):
        self.stop()
        system('shutdown now')


if __name__ == '__main__':
    p = Paperoid(PATH, PRINTER_MAC, BUTTON_GPIO)
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        p.stop()
