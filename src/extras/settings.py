from enum import Enum

import pygame

from ..controller import KeyboardControl
from .. import SingletonMeta

class Settings(metaclass=SingletonMeta):

    controller = KeyboardControl()

    FPS = 60
    RESOLUTION_SCALE = 1
    ANCHO, ALTO = int(RESOLUTION_SCALE*1024), int(RESOLUTION_SCALE*576)
    HABITACION_ANCHO = int(RESOLUTION_SCALE*32)     # Ancho de cada habitación en el minimapa
    HABITACION_ALTO = int(RESOLUTION_SCALE*18)      # Alto de cada habitación en el minimapa
    ESPACIADO = 4            # Espacio entre habitaciones en el minimapa
    MINIMAPA_POS = (50, int((ALTO - HABITACION_ALTO * 4 - ESPACIADO * 3 - RESOLUTION_SCALE*50)))  # Posición en pantalla (esquina superior derecha)
    BUTTON_SIZEX, BUTTON_SIZEY = ANCHO * 0.4, ALTO * 0.1
    VOLUMEN_MUSICA = 1
    VOLUMEN_SFX = 1
    

    RESIZE_PLAYER = 2.5
    RESIZE_CANNON = 2.0

    TILE_SIZE = int(RESOLUTION_SCALE*32)
    BOMB_SIZE= int(3*RESOLUTION_SCALE)

    def updateRes(self):
        self.ANCHO, self.ALTO = int(self.RESOLUTION_SCALE*1024), int(self.RESOLUTION_SCALE*576)
        self.HABITACION_ANCHO = int(self.RESOLUTION_SCALE*32)
        self.HABITACION_ALTO = int(self.RESOLUTION_SCALE*18)
        self.MINIMAPA_POS = (50, int((self.ALTO - self.HABITACION_ALTO * 4 - self.ESPACIADO * 3 - self.RESOLUTION_SCALE*50)))

        self.TILE_SIZE = int(self.RESOLUTION_SCALE*32)
        self.BUTTON_SIZEX, self.BUTTON_SIZEY = self.ANCHO * 0.4, self.ALTO * 0.1


    TIME_FRAME = 30
    COOLDOWN = 2000

    NEGRO = (0, 0, 0)
    NEGRO_TRANSLUCIDO = (0, 0, 0, 180)
    BLANCO = (255, 255, 255)
    BLANCO_TRANSLUCIDO = (180, 180, 180, 180)
    GRIS_OSCURO = (30, 30, 30)
    ROJO = (136, 0, 21)
    ROJO_CLARO = (217, 0, 4)
    ROJO_TRANSLUCIDO = (255, 0, 0, 180)
    VERDE = (0, 255, 0)
    AMARILLO = (255, 255, 0)
    ELIMINAR_FONDO = (248, 0, 255)

    EVENTO_JUGADOR_MUERTO = pygame.USEREVENT + 1
    EVENTO_BOSS_MUERTO = pygame.USEREVENT + 2
    EVENTO_COLECCIONABLE_RECOGIDO = pygame.USEREVENT + 3

    class CollisionLayer(Enum):
        PLAYER = 1
        ENEMY = 2
        BULLET_PLAYER = 3
        BULLET_ENEMY = 4
        BULLET_BOSS2 = 5
        BULLET_ANY = 6
        WALL = 7
        LOW_WALL = 8
        INTERACTUABLE= 9
        NONE = 10  # Para elementos sin colisión
        BOTH = 11

    COLLISION_RULES = {
        CollisionLayer.PLAYER: {CollisionLayer.ENEMY, CollisionLayer.BULLET_BOSS2, CollisionLayer.BULLET_ENEMY, CollisionLayer.BULLET_ANY, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
        CollisionLayer.ENEMY: {CollisionLayer.PLAYER, CollisionLayer.ENEMY, CollisionLayer.BULLET_PLAYER, CollisionLayer.BULLET_ANY, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
        CollisionLayer.BULLET_PLAYER: {CollisionLayer.ENEMY, CollisionLayer.WALL},
        CollisionLayer.BULLET_ENEMY: {CollisionLayer.PLAYER, CollisionLayer.WALL},
        CollisionLayer.BULLET_BOSS2: {CollisionLayer.PLAYER},
        CollisionLayer.BULLET_ANY: {CollisionLayer.PLAYER, CollisionLayer.ENEMY, CollisionLayer.WALL},
        CollisionLayer.WALL: set(),
        CollisionLayer.LOW_WALL: set(),
        CollisionLayer.NONE: set(),  # No colisiona con nada
        CollisionLayer.INTERACTUABLE: {CollisionLayer.PLAYER},
        CollisionLayer.BOTH: {CollisionLayer.PLAYER, CollisionLayer.ENEMY}
    }