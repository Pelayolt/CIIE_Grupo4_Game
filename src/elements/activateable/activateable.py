import abc
from ..element import Element
from ...extras import Settings

class Activateable(Element):

    def __init__(self, x, y, imagen,layer):
        super().__init__(x * Settings.TILE_SIZE, y * Settings.TILE_SIZE, imagen, layer)

    @abc.abstractmethod
    def activar(self):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")