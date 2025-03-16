from .interactable import Interactable
from ...extras import CollisionLayer

class Trap(Interactable):
    def __init__(self, x, y, imagen):
        super().__init__(x, y, imagen, CollisionLayer.INTERACTUABLE)

    def interactuar(self, objeto):
        # Suponiendo que el mundo tiene una referencia al jugador: mundo.jugador
        if self.check_collision(objeto) and not self.eliminar:
            self.explotar(objeto)

    def explotar(self, jugador):
        from ...tanks import Player
        if isinstance(jugador, Player):
            self.eliminar = True
            jugador.recibir_dano(1)