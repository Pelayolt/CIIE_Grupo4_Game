import pygame
from settings import CollisionLayer, COLLISION_RULES

class Elemento:
    def __init__(self, x, y, imagen=None, collision_layer=CollisionLayer.NONE):
        self.x = x
        self.y = y
        self.collision_layer = collision_layer  # Asigna la capa de colisión
        self.imagen = imagen

        # Si hay imagen, ajustamos el rectángulo y la máscara
        if self.imagen:
            self.rect_element = self.imagen.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.imagen)
        else:
            self.rect_element = pygame.Rect(x, y, 0, 0)
            self.mask = None

    def dibujar(self, pantalla, mundo):
        """Dibuja el elemento en la pantalla."""
        if self.imagen:
            pantalla.blit(self.imagen, (self.rect_element.x - mundo.camara_x, self.rect_element.y - mundo.camara_y))
        else:
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect_element)

    def check_collision(self, other_element):
        """Verifica colisión con otro elemento basado en la tabla de colisiones."""
        # Si las capas no pueden colisionar, retorna False
        if other_element.collision_layer not in COLLISION_RULES.get(self.collision_layer, set()):
            return False

        # Verificar colisión por máscara si ambos tienen imagen
        if self.rect_element.colliderect(other_element.rect_element):
            offset_x = other_element.rect_element.x - self.rect_element.x
            offset_y = other_element.rect_element.y - self.rect_element.y

            if self.mask and other_element.mask:
                return bool(self.mask.overlap(other_element.mask, (offset_x, offset_y)))
            return True  # Si no hay máscaras, pero hay colisión de rectángulos
        return False

class Boton(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, imagen, CollisionLayer.NONE)

class Puerta(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, imagen, CollisionLayer.WALL)

class Muro(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, imagen, CollisionLayer.WALL)

class MuroBajo(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, imagen, CollisionLayer.LOW_WALL)

class Trampa(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, imagen, CollisionLayer.NONE)

class Decoracion(Elemento):
    def __init__(self, x, y, tamaño_tile, imagen):
        imagen = pygame.transform.scale(imagen, (tamaño_tile, tamaño_tile))  # Escalamos la imagen
        super().__init__(x, y, imagen, CollisionLayer.NONE)

