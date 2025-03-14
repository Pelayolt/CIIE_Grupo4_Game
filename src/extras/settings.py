from enum import Enum

import pygame

from ..controller import KeyboardControl

controller = KeyboardControl()

FPS = 60
ANCHO, ALTO = 1024, 576
HABITACION_ANCHO = 32     # Ancho de cada habitación en el minimapa
HABITACION_ALTO = 18      # Alto de cada habitación en el minimapa
ESPACIADO = 4            # Espacio entre habitaciones en el minimapa
MINIMAPA_POS = (50, ALTO - HABITACION_ALTO * 4 - ESPACIADO * 3 - 50)  # Posición en pantalla (esquina superior derecha)

RESIZE_PLAYER = 2.5
RESIZE_CANNON = 2.0

TILE_SIZE = 32

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
EVENTO_BOSS_MUERTO = pygame.USEREVENT + 2  # Asegúrate de que sea único

class CollisionLayer(Enum):
    PLAYER = 1
    ENEMY = 2
    BULLET_PLAYER = 3
    BULLET_ENEMY = 4
    BULLET_ANY = 5
    WALL = 6
    LOW_WALL = 7
    INTERACTUABLE=8
    NONE = 9  # Para elementos sin colisión
    BOTH = 10

COLLISION_RULES = {
    CollisionLayer.PLAYER: {CollisionLayer.ENEMY, CollisionLayer.BULLET_ENEMY, CollisionLayer.BULLET_ANY, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
    CollisionLayer.ENEMY: {CollisionLayer.PLAYER, CollisionLayer.ENEMY, CollisionLayer.BULLET_PLAYER, CollisionLayer.BULLET_ANY, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
    CollisionLayer.BULLET_PLAYER: {CollisionLayer.ENEMY, CollisionLayer.WALL},
    CollisionLayer.BULLET_ENEMY: {CollisionLayer.PLAYER, CollisionLayer.WALL},
    CollisionLayer.BULLET_ANY: {CollisionLayer.PLAYER, CollisionLayer.ENEMY, CollisionLayer.WALL},
    CollisionLayer.WALL: set(),
    CollisionLayer.LOW_WALL: set(),
    CollisionLayer.NONE: set(),  # No colisiona con nada
    CollisionLayer.INTERACTUABLE: {CollisionLayer.PLAYER},
    CollisionLayer.BOTH: {CollisionLayer.PLAYER, CollisionLayer.ENEMY}
}