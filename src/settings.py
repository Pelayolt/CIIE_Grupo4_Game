from enum import Enum

FPS = 60
ANCHO, ALTO = 1024, 576

RESIZE_PLAYER = 2.5
RESIZE_CANNON = 2.0

RESIZE_ENEMY_BROWN = 2.7
RESIZE_ENEMY_GREEN = 2.3
RESIZE_ENEMY_ = 2.5

TILE_SIZE = 32

TIME_FRAME = 30
COOLDOWN = 2000

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS_OSCURO = (30, 30, 30)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
ELIMINAR_FONDO = (248, 0, 255)

class CollisionLayer(Enum):
    PLAYER = 1
    ENEMY = 2
    BULLET_PLAYER = 3
    BULLET_ENEMY = 4
    BULLET_ANY = 5
    WALL = 6
    LOW_WALL = 7
    NONE = 8  # Para elementos sin colisión

COLLISION_RULES = {
    CollisionLayer.PLAYER: {CollisionLayer.ENEMY, CollisionLayer.BULLET_ENEMY, CollisionLayer.BULLET_ANY, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
    CollisionLayer.ENEMY: {CollisionLayer.PLAYER, CollisionLayer.BULLET_PLAYER, CollisionLayer.BULLET_ANY, CollisionLayer.WALL, CollisionLayer.LOW_WALL},
    CollisionLayer.BULLET_PLAYER: {CollisionLayer.ENEMY, CollisionLayer.WALL},
    CollisionLayer.BULLET_ENEMY: {CollisionLayer.PLAYER, CollisionLayer.WALL},
    CollisionLayer.BULLET_ANY: {CollisionLayer.PLAYER, CollisionLayer.ENEMY, CollisionLayer.WALL},
    CollisionLayer.WALL: set(),
    CollisionLayer.LOW_WALL: set(),
    CollisionLayer.NONE: set()  # No colisiona con nada
}