from extras.settings import RESIZE_PLAYER
from tanks.enemies.enemy import Enemy

class Mecha(Enemy):
    def __init__(self, x, y, modo_patrulla):
        super().__init__(20, 2.5, x, y, RESIZE_PLAYER, RESIZE_PLAYER, tank_level="_boss1")