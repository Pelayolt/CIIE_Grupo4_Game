from .interactable import Interactable
from ...extras import CollisionLayer

class IceCube(Interactable):
    def __init__(self, x, y, imagen):
        super().__init__(x, y, imagen, CollisionLayer.INTERACTUABLE)

    def interactuar(self, objeto):
        from ...tanks import Player
        if self.check_collision(objeto) and isinstance(objeto, Player):
            objeto.establecer_posicion(objeto.posx_change_screen, objeto.posy_change_screen)


