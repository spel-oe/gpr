#!/usr/bin/env python
# coding=utf-8

# Bibliotheken importieren
from lib_oled96 import ssd1306
from smbus import SMBus
from PIL import ImageFont
import time

class display():
    def __init__(self):
        self.draw = 0
        self.fontBig = 0
        self.fontSmall = 0
        self.oled = 0
        self.number = 333
        self.update = False
        self.init()
    def init(self):
        # Display einrichten
        i2cbus = SMBus(1)			# 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1
        self.oled = ssd1306(i2cbus)

        # Ein paar Abkürzungen, um den Code zu entschlacken
        self.draw = self.oled.canvas

        # Schriftarten festlegen
        self.fontSmall = ImageFont.truetype('FreeSans.ttf', 13)
        self.fontBig = ImageFont.truetype('FreeSans.ttf', 55)

        # Display zum Start löschen
        self.oled.cls()
        self.oled.display()

    def drawer(self, bg):

        self.draw.text((0, 0), "Measurement Number:", font=self.fontSmall, fill=1)
        if (bg):
            self.draw.rectangle((0, 13, 128, 64), outline=1, fill=1)
            self.draw.text((0,  10), str(self.number), font=self.fontBig, fill=0)
        else :
            self.draw.rectangle((0, 13, 128, 64), outline=0, fill=0)
            self.draw.text((0,  10), str(self.number), font=self.fontBig, fill=1)
        # Ausgaben auf Display schreiben
        self.oled.display()

    def start(self):
        self.update = 1
    def stop(self):
        self.update = 0
    
    def work(self):
        if (self.update):
            self.drawer(True)
        else:
            self.drawer(False)
    def worker(self):
        delay = 1
        while True:
            if (self.update): 
                self.drawer(True)
                time.sleep(delay)
            self.drawer(False)
            time.sleep(delay)

#iface = Display()
#iface.number = 666
#iface.update = True
#iface.worker()

