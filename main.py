import time

from game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.transfer_loop()