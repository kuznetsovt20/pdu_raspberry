import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 0, 0)

    def draw_cursor(self):
        self.game.draw_text('*', 17, self.cursor_rect.x, self.cursor_rect.y)

    def draw_menu_buttons(self, text1, text2, text3, text4):
        self.game.draw_text(text1, 17, 200, 10)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "startup"
        self.offset = 190
        self.menu_x, self.menu_y = 30, 40
        self.select_x, self.select_y = self.menu_x, self.menu_y + 40
        self.startup_x, self.startup_y = self.menu_x, self.select_y + 20
        self.readValues_x, self.readValues_y = self.menu_x, self.startup_y + 20
        self.creditsValues_x, self.creditsValues_y = self.menu_x, self.readValues_y + 20
        self.cursor_rect.bottomleft = (self.startup_x + self.offset, self.startup_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('>main>.. ', 17, self.menu_x, self.menu_y)
            self.game.draw_text('Main options:', 17, self.select_x, self.select_y)
            self.game.draw_text('|  start-up wizard', 17, self.startup_x, self.startup_y)
            self.game.draw_text('|  read values', 17, self.readValues_x, self.readValues_y)
            self.game.draw_text('|  credits', 17, self.creditsValues_x, self.creditsValues_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'startup':
                self.cursor_rect.bottomleft = (self.readValues_x + self.offset, self.readValues_y)
                self.state = 'read'
            elif self.state == 'read':
                self.cursor_rect.bottomleft = (self.creditsValues_x + self.offset, self.creditsValues_y)
                self.state = 'credits'
            elif self.state == 'credits':
                self.cursor_rect.bottomleft = (self.startup_x + self.offset, self.startup_y)
                self.state = 'startup'
        elif self.game.UP_KEY:
            if self.state == 'startup':
                self.cursor_rect.bottomleft = (self.creditsValues_x + self.offset, self.creditsValues_y)
                self.state = 'credits'
            elif self.state == 'credits':
                self.cursor_rect.bottomleft = (self.readValues_x + self.offset, self.readValues_y)
                self.state = 'read'
            elif self.state == 'read':
                self.cursor_rect.bottomleft = (self.startup_x + self.offset, self.startup_y)
                self.state = 'startup'
     
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'startup':
                self.game.curr_menu = self.game.pdus
            elif self.state == 'read':
                self.game.curr_menu = self.game.readDatas
            elif self.state == 'credits':
                pass
            self.run_display = False

class PduMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "pdu500"
        self.offset = 160
        self.menu_x, self.menu_y = 30, 40
        self.select_x, self.select_y = self.menu_x, self.menu_y + 40
        self.pdu500_x, self.pdu500_y = self.menu_x, self.select_y + 20
        self.pdu600_x, self.pdu600_y = self.menu_x, self.pdu500_y + 20
        self.pdu700_x, self.pdu700_y = self.menu_x, self.pdu600_y + 20
        self.cursor_rect.bottomleft = (self.pdu500_x + self.offset, self.pdu500_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('>main>pdu>.. ', 17, self.menu_x, self.menu_y)
            self.game.draw_text('PDU type:', 17, self.select_x, self.select_y)
            self.game.draw_text('|  pdu 500 kVA', 17, self.pdu500_x, self.pdu500_y)
            self.game.draw_text('|  pdu 600 kVA', 17, self.pdu600_x, self.pdu600_y)
            self.game.draw_text('|  pdu 700 kVA', 17, self.pdu700_x, self.pdu700_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'pdu500':
                self.cursor_rect.bottomleft = (self.pdu600_x + self.offset, self.pdu600_y)
                self.state = 'pdu600'
            elif self.state == 'pdu600':
                self.cursor_rect.bottomleft = (self.pdu700_x + self.offset, self.pdu700_y)
                self.state = 'pdu700'
            elif self.state == 'pdu700':
                self.cursor_rect.bottomleft = (self.pdu500_x + self.offset, self.pdu500_y)
                self.state = 'pdu500'
        elif self.game.UP_KEY:
            if self.state == 'pdu500':
                self.cursor_rect.bottomleft = (self.pdu700_x + self.offset, self.pdu700_y)
                self.state = 'pdu700'
            elif self.state == 'pdu700':
                self.cursor_rect.bottomleft = (self.pdu600_x + self.offset, self.pdu600_y)
                self.state = 'pdu600'
            elif self.state == 'pdu600':
                self.cursor_rect.bottomleft = (self.pdu500_x + self.offset, self.pdu500_y)
                self.state = 'pdu500'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'pdu500':
                self.game.ampOverload = 250
                self.game.curr_menu = self.game.pqms
            elif self.state == 'pdu600':
                self.game.ampOverload = 300
                self.game.curr_menu = self.game.pqms
            elif self.state == 'pdu700':
                self.game.ampOverload = 350
                self.game.curr_menu = self.game.pqms
            self.run_display = False
        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

class PqmMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "pqm10"
        self.offset = 100
        self.menu_x, self.menu_y = 30, 40
        self.select_x, self.select_y = self.menu_x, self.menu_y + 40
        self.pqm10_x, self.pqm10_y = self.menu_x, self.select_y + 20
        self.pqm11_x, self.pqm11_y = self.menu_x, self.pqm10_y + 20
        self.pqm12_x, self.pqm12_y = self.menu_x, self.pqm11_y + 20
        self.cursor_rect.bottomleft = (self.pqm10_x + self.offset, self.pqm10_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('>main>pdu>pqm>.. ', 17, self.menu_x, self.menu_y)
            self.game.draw_text('pqm position:', 17, self.select_x, self.select_y)
            self.game.draw_text('|  pqm #1', 17, self.pqm10_x, self.pqm10_y)
            self.game.draw_text('|  pqm #2', 17, self.pqm11_x, self.pqm11_y)
            self.game.draw_text('|  pqm #3', 17, self.pqm12_x, self.pqm12_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'pqm10':
                self.cursor_rect.bottomleft = (self.pqm11_x + self.offset, self.pqm11_y)
                self.state = 'pqm11'
            elif self.state == 'pqm11':
                self.cursor_rect.bottomleft = (self.pqm12_x + self.offset, self.pqm12_y)
                self.state = 'pqm12'
            elif self.state == 'pqm12':
                self.cursor_rect.bottomleft = (self.pqm10_x + self.offset, self.pqm10_y)
                self.state = 'pqm10'
        elif self.game.UP_KEY:
            if self.state == 'pqm10':
                self.cursor_rect.bottomleft = (self.pqm12_x + self.offset, self.pqm12_y)
                self.state = 'pqm12'
            elif self.state == 'pqm12':
                self.cursor_rect.bottomleft = (self.pqm11_x + self.offset, self.pqm11_y)
                self.state = 'pqm11'
            elif self.state == 'pqm11':
                self.cursor_rect.bottomleft = (self.pqm10_x + self.offset, self.pqm10_y)
                self.state = 'pqm10'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'pqm10':
                self.game.ipAddress = 10
                self.game.diAlarms = True
                self.game.curr_menu = self.game.confirms
            elif self.state == 'pqm11':
                self.game.ipAddress = 11
                self.game.curr_menu = self.game.confirms
            elif self.state == 'pqm12':
                self.game.ipAddress = 12
                self.game.curr_menu = self.game.confirms
            self.run_display = False
        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.pdus
            self.run_display = False

class ConfirmDataMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.menu_x, self.menu_y = 30, 40
        self.regNum = 0
        self.regValue = 0

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('>main>pdu>pqm>confirmation>.. ', 17, self.menu_x, self.menu_y)
            self.game.draw_text('pqm parameters to update:', 17, 30, 80)
            self.game.draw_text('|  ct ratio 500:100', 17, 30, 100)
            if self.game.ipAddress == 10:
                self.game.draw_text('|  alarm: DI + overload ' + str(self.game.ampOverload) + 'A', 17, 30, 120)
                self.game.draw_text('|  ip: 100.100.100.10', 17, 30, 140)
            elif self.game.ipAddress == 11:
                self.game.draw_text('|  alarm: overload ' + str(self.game.ampOverload) + 'A', 17, 30, 120)
                self.game.draw_text('|  ip: 100.100.100.11', 17, 30, 140)
            elif self.game.ipAddress == 12:
                self.game.draw_text('|  alarm: overload ' + str(self.game.ampOverload) + 'A', 17, 30, 120)
                self.game.draw_text('|  ip: 100.100.100.12', 17, 30, 140)
            self.game.draw_text('|  date & time', 17, 30, 160)
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.game.updateData = True
            self.run_display = False
        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.pqms
            self.run_display = False

class ConfirmIpMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.menu_x, self.menu_y = 30, 40

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('>main>pdu>pqm>.. ', 17, self.menu_x, self.menu_y)
            self.game.draw_text('Ready to set new IP?', 17, 100, 100)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.game.updateData = True
            self.game.updateIp = True
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

class ConnectionIssuesMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.menu_x, self.menu_y = 30, 40

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('>..>confirm>connection> ', 17, self.menu_x, self.menu_y)
            self.game.draw_text('connection issues to', 17, self.select_x, self.select_y)
            self.game.draw_text('192.168.0.1', 17, self.select_x, self.select_y+20)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            pass
            self.run_display = False
        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

class ReadDataMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.menu_x, self.menu_y = 30, 40

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.readParam()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('>read data.. ', 17, self.menu_x, self.menu_y)
            self.game.draw_text('V1-2: ' + str(self.game.volt12), 17, 30, 80)
            self.game.draw_text('V2-3: ' + str(self.game.volt23), 17, 30, 100)
            self.game.draw_text('V3-1: ' + str(self.game.volt31), 17, 30, 120)
            self.game.draw_text('V1-N: ' + str(self.game.volt1n), 17, 30, 150)
            self.game.draw_text('V2-N: ' + str(self.game.volt2n), 17, 30, 170)
            self.game.draw_text('V3-N: ' + str(self.game.volt3n), 17, 30, 190)
            self.game.draw_text('I1: ' + str(self.game.amp1), 17, 160, 80)
            self.game.draw_text('I2: ' + str(self.game.amp2), 17, 160, 100)
            self.game.draw_text('I3: ' + str(self.game.amp3), 17, 160, 120)
            self.game.draw_text('W1: ' + str(self.game.wat1), 17, 160, 150)
            self.game.draw_text('W2: ' + str(self.game.wat2), 17, 160, 170)
            self.game.draw_text('W3: ' + str(self.game.wat3), 17, 160, 190)
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.game.curr_menu = self.game.confirmIps
            self.run_display = False
        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
            print('Now im out')




