import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from src.game import Game

if __name__ == "__main__":
    juego = Game()
    juego.run()                 