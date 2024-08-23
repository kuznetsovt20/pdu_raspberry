from game import Game
from gpiozero import Button

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.transfer_loop()