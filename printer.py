#!/usr/bin/python3
# -*- coding: utf-8 -*-

from hardware import Paperang


printer = Paperang('FC:58:FA:32:69:2D')
if printer.connected:
    self.printer_hardware.sendImageToBt('test.jpg')
