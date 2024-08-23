from game import Game
from gpiozero import Button

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.transfer_loop()

    if g.buttonNext.is_pressed:
        g.START_KEY = True
    if g.buttonBack.is_pressed:
        g.BACK_KEY = True
    if g.buttonDown.is_pressed:
        g.DOWN_KEY = True
    if g.buttonUp.is_pressed:
        g.UP_KEY = True