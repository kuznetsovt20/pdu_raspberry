import pygame
import time
import os

from gpiozero import Button
from pyModbusTCP.client import ModbusClient
from menu import *
from datetime import datetime
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.updateData, self.readData, self.updateIp = True, False, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 320, 240
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = 'whitrabt.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.pdus = PduMenu(self)
        self.pqms = PqmMenu(self)
        self.confirms = ConfirmDataMenu(self)
        self.confirmIps = ConfirmIpMenu(self)
        self.connectionIssues = ConnectionIssuesMenu(self)
        self.readDatas = ReadDataMenu(self)
        self.curr_menu = self.main_menu
        self.ipAddress, self.ampOverload = 1, 1
        self.diAlarms = False
        self.faultCode = 'Error code: '
        self.volt12, self.volt23, self.volt31, self.volt1n, self.volt2n, self.volt3n = 0, 0, 0, 0, 0, 0
        self.amp1, self.amp2, self.amp3, self.wat1, self.wat2, self.wat3 = 0, 0, 0, 0, 0, 0
        self.menu_x, self.menu_y = 30, 40
        self.u1, self.u2, self.u3, self.u12, self.u23, self.u31, self.i1, self.i2, self.i3, self.p1, self.p2, self.p3 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        self.buttonNext, self.buttonBack, self.buttonDown, self.buttonUp = Button(27), Button(17), Button(22), Button(23)

    def transfer_loop(self):
        while self.updateData:
            self.check_events()
            pygame.display.update()
            self.reset_keys()
            self.display.fill(self.BLACK)
            self.draw_text('Transferring data', 20, 50, 100)
            self.window.blit(self.display, (0,0))
            self.writeParam()
            self.updateData = False
            self.updateIp = False
            self.curr_menu = self.readDatas

    def check_events(self):
        if self.buttonNext.is_pressed:
            self.START_KEY = True
        if self.buttonBack.is_pressed:
            self.BACK_KEY = True
        if self.buttonDown.is_pressed:
            self.DOWN_KEY = True
        if self.buttonUp.is_pressed:
            self.UP_KEY = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing, self.confirmation = False, False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.START_KEY = True
                if event.key == pygame.K_LEFT:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (x,y)
        self.display.blit(text_surface,text_rect)

    def writeParam(self):
        c = ModbusClient(host='192.168.1.254', port=502, unit_id=1, auto_open=True, auto_close=True, debug=True, timeout=1)
        if c.is_open:
            if self.updateIp:
                print(c.write_multiple_registers(259, [25700])) #IP 100.100
                print(c.write_multiple_registers(263, [25700])) #gateway 100.100
                print(c.write_multiple_registers(264, [25601])) #gateway 100.1

                if self.ipAddress == 10:
                    print('ip 10')
                    print(c.write_multiple_registers(260, [25610])) #IP 100.10
                elif self.ipAddress == 11:
                    print('ip 11')
                    print(c.write_multiple_registers(260, [25611])) #IP 100.11
                elif self.ipAddress == 12:
                    print('ip 12')
                    print(c.write_multiple_registers(260, [25612])) #IP 100.12
                print("IP updated")
                self.curr_menu = self.game.main_menu
                time.sleep(20)
            else:
                now = datetime.now()
                print(c.write_multiple_registers(4104, [500])) #ct1
                print(c.write_multiple_registers(4105, [100])) #ct2
                print(c.write_multiple_registers(4121, [0])) #energy reading - primary
                print(c.write_multiple_registers(4256, [1])) #RO type mode - alarm

                print(c.write_multiple_registers(4166, [1])) #enable all alarms
                print(c.write_multiple_registers(4168, [1])) #enable alarm channels 1
                print(c.write_multiple_registers(4174, [12])) #average current
                print(c.write_multiple_registers(4175, [1])) #greater than
                print(c.write_multiple_registers(4176, [self.ampOverload*4])) #threshold
                print(c.write_multiple_registers(4177, [100])) #channel 1 delay
                print(c.write_multiple_registers(4178, [1])) #ro id

                if self.ipAddress == 10:
                    print(c.write_multiple_registers(4168, [7])) #enable alarm channels 1-3
                    print(c.write_multiple_registers(4179, [52])) #input on di1
                    print(c.write_multiple_registers(4181, [2])) #set point to off
                    print(c.write_multiple_registers(4182, [0])) #channel 2 delay
                    print(c.write_multiple_registers(4183, [1])) #ro id
                    print(c.write_multiple_registers(4184, [53])) #input on di2
                    print(c.write_multiple_registers(4186, [2])) #set point to off
                    print(c.write_multiple_registers(4187, [0])) #channel 3 delay
                    print(c.write_multiple_registers(4188, [1])) #ro id

        else:
            print('connection issues')
    
    def floatDecoder(self, instance):
        if instance != None:
            print(instance)
            decoder = BinaryPayloadDecoder.fromRegisters(instance, byteorder=Endian.BIG, wordorder=Endian.BIG)   
            return float('{0:.2f}'.format(decoder.decode_32bit_float()))
        else:
            return 0

    def readParam(self):
        print('reading param')
        c = ModbusClient(host='192.168.1.254', port=502, unit_id=1, auto_close=True, auto_open=True, debug=True, timeout=1)
        self.volt1n = self.floatDecoder(c.read_holding_registers(12290, 2))
        self.volt2n = self.floatDecoder(c.read_holding_registers(12292, 2))
        self.volt2n = self.floatDecoder(c.read_holding_registers(12294, 2))
        self.volt12 = self.floatDecoder(c.read_holding_registers(12298, 2))
        self.volt23 = self.floatDecoder(c.read_holding_registers(12300, 2))
        self.volt31 = self.floatDecoder(c.read_holding_registers(12302, 2))
        self.amp1 = self.floatDecoder(c.read_holding_registers(12306, 2))
        self.amp2 = self.floatDecoder(c.read_holding_registers(12308, 2))
        self.amp3 = self.floatDecoder(c.read_holding_registers(12310, 2))
        self.wat1 = self.floatDecoder(c.read_holding_registers(12316, 2))
        self.wat2 = self.floatDecoder(c.read_holding_registers(12318, 2))
        self.wat3 = self.floatDecoder(c.read_holding_registers(12320, 2))