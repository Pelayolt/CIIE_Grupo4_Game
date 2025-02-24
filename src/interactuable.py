import abc
import pygame

from elements import Elemento
from settings import CollisionLayer


class Interactuable(Elemento):

    def __init__(self, x, y, imagen,layer):
        super().__init__(x, y, imagen, layer)

    @abc.abstractmethod
    def activar(self):
        """Método que se ejecutará cuando se active el objeto."""
        raise NotImplementedError("Debe implementarse en la subclase")


class Boton(Interactuable):
    def __init__(self, x, y, sprite, objetos_a_activar, mundo):
        super().__init__(x, y, sprite, CollisionLayer.INTERACTUABLE)
        self.camara_temporal_activa = False
        self.tiempo_activacion = 0
        self.tiempo_objetos = 0  # ⏳ Nuevo temporizador para los objetos
        self.objetos_activados = False  # ⚡ Controla si ya fueron activados
        self.x = x
        self.y = y
        self.sprite = sprite
        self.objetos_a_activar = objetos_a_activar
        self.mundo = mundo

        self.camara_x_original = self.mundo.camara_x
        self.camara_y_original = self.mundo.camara_y

    def update(self):
        """Controla el tiempo de activación de la cámara y los objetos."""
        if self.camara_temporal_activa:
            tiempo_actual = pygame.time.get_ticks()

            # ⚡ Activar los objetos después de 1 segundo
            if not self.objetos_activados and tiempo_actual - self.tiempo_objetos >= 1000:
                for objeto in self.objetos_a_activar:
                    objeto.activar()
                self.objetos_activados = True  # Solo activarlos una vez

            # ⏳ Restaurar la cámara después de 2 segundos
            if tiempo_actual - self.tiempo_activacion >= 2000:
                self.mundo.camara_x = self.camara_x_original
                self.mundo.camara_y = self.camara_y_original
                self.mundo.enfocando_objeto = False
                self.camara_temporal_activa = False

    def activar(self):
        """Mueve la cámara y programa la activación de objetos después de 1 segundo."""
        if not self.camara_temporal_activa:
            self.mundo.enfocando_objeto = True

            self.camara_x_original = self.mundo.camara_x
            self.camara_y_original = self.mundo.camara_y

            self.mundo.camara_x = self.objetos_a_activar[0].x - self.mundo.ancho_pantalla // 2
            self.mundo.camara_y = self.objetos_a_activar[0].y - self.mundo.alto_pantalla // 2

            self.tiempo_activacion = pygame.time.get_ticks()
            self.tiempo_objetos = self.tiempo_activacion  # ⏳ Se activarán después de 1 segundo
            self.objetos_activados = False  # ⚡ Reset para permitir nueva activación

            self.camara_temporal_activa = True





class Puerta(Interactuable):
    def __init__(self, x, y, sprite_cerrado, sprite_abierto):
        super().__init__(x,y,sprite_cerrado,CollisionLayer.WALL)
        self.x = x
        self.y = y
        self.abierta = False  # Estado inicial: cerrada
        self.sprite_abierto = sprite_abierto
        self.sprite_cerrado = sprite_cerrado

    def activar(self):
        self.abierta = not self.abierta  # Cambia el estado
        if self.abierta:
            self.collision_layer = CollisionLayer.NONE
            self.imagen=self.sprite_abierto
        else:
            self.collision_layer = CollisionLayer.WALL
            self.imagen=self.sprite_cerrado


