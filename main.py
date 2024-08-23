from game import Game
from gpiozero import Button

g = Game()
buttonNext, buttonBack, buttonDown, buttonUp = Button(27), Button(17), Button(22), Button(23)

while g.running:
    g.curr_menu.display_menu()
    g.transfer_loop()

    if buttonNext.is_pressed:
        g.self.START_KEY = True
    if buttonBack.is_pressed:
        g.self.BACK_KEY = True
    if buttonDown.is_pressed:
        g.self.DOWN_KEY = True
    if buttonUp.is_pressed:
        g.self.UP_KEY = True