from .enemy import Enemy
from ...extras import Settings

class EnemyRed(Enemy):
    def __init__(self, x, y, modo_patrulla, id_mapa, elite=False):
        super().__init__(12, 2, x, y, Settings.RESIZE_PLAYER, Settings.RESIZE_PLAYER, modo_patrulla, elite, tank_level="_red", id_mapa=id_mapa)