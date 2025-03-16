import math
import time
import numpy as np
from ...extras import TILE_SIZE, ResourceManager
from ...elements import Element

class Bullet(Element):
    # Cargar sprites de colisión una sola vez (variable estática)
    sprites_colision = [ResourceManager.load_and_scale_image(f"expl{i}.png", 20 / TILE_SIZE, 20 / TILE_SIZE)
                        for i in range(1, 11)]

    def __init__(self, arma, angulo=None, desplazamiento_lateral=0, desplazamiento_frontal=0):
        self.arma = arma
        self.angle_rad = math.radians(angulo if angulo else arma.angulo_cannon)
        x, y = self.get_cannon_tip(desplazamiento_lateral, desplazamiento_frontal)

        super().__init__(x, y, arma.imagen_bala, arma.tank.colision_layer_balas)

        self.velocidad = 7
        self.vel_x = math.cos(self.angle_rad) * self.velocidad
        self.vel_y = math.sin(self.angle_rad) * self.velocidad
        self.dano = 1

        # Estado de la bala
        self.colisionando = False
        self.tiempo_colision = 0
        self.frame_actual = 0

    def update(self, mundo, ancho_pantalla, alto_pantalla):
        """Actualiza la posición de la bala y verifica colisiones."""
        if self.colisionando:
            return self.actualizar_colision()

        # Mover la bala
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect_element.topleft = (self.x, self.y)

        # Verificar si la bala sale de la pantalla
        if self.fuera_de_pantalla(mundo, ancho_pantalla, alto_pantalla):
            return True  # Eliminar la bala

        # Verificar colisiones con los elementos del mundo
        for elemento in mundo.elementos_por_capa.get(2, []):  # Evita KeyError si la capa no existe
            if self.check_collision(elemento):
                self.realizar_dano(elemento)
                self.iniciar_colision()
                return False  # No eliminar aún, esperar animación
        return False

    def iniciar_colision(self, elemento=None):
        """Activa la animación de colisión y detiene el movimiento."""
        self.colisionando = True
        self.tiempo_colision = time.time()
        self.rect_element = self.sprites_colision[0].get_rect(center=self.rect_element.center)  # Centrar explosión

    def realizar_dano(self, elemento):
        if hasattr(elemento, "vida"):
            elemento.recibir_dano(self.dano)
            return True
        return False

    def actualizar_colision(self):
        """Maneja la animación de colisión y decide si eliminar la bala."""
        tiempo_transcurrido = time.time() - self.tiempo_colision
        self.frame_actual = int((tiempo_transcurrido / 1.0) * len(self.sprites_colision))

        return self.frame_actual >= len(self.sprites_colision)  # Eliminar cuando la animación termine

    def get_cannon_tip(self, desplazamiento_lateral, desplazamiento_frontal):
        """Calcula la punta del cañón después de la rotación, permitiendo desplazamiento en ambos ejes."""

        cannon_length = self.arma.rect_canon.height // 4  # Largo del cañón

        # Convertir ángulo a radianes
        angle_rad = self.angle_rad

        # Desplazamiento en la dirección del cañón (frontal)
        x_offset = (cannon_length + desplazamiento_frontal) * np.cos(angle_rad)
        y_offset = (cannon_length + desplazamiento_frontal) * np.sin(angle_rad)

        # Desplazamiento lateral (perpendicular al cañón)
        x_lateral_offset = desplazamiento_lateral * np.cos(angle_rad + np.pi / 2)  # 90° perpendiculares
        y_lateral_offset = desplazamiento_lateral * np.sin(angle_rad + np.pi / 2)

        # Calcular posición final
        cannon_x = self.arma.rect_canon.centerx + x_offset + x_lateral_offset
        cannon_y = self.arma.rect_canon.centery + y_offset + y_lateral_offset

        return cannon_x, cannon_y

    def fuera_de_pantalla(self, mundo, ancho_pantalla, alto_pantalla):
        """Verifica si la bala ha salido de la pantalla."""
        return (self.x < mundo.camara_x or self.x > mundo.camara_x + ancho_pantalla or
                self.y < mundo.camara_y or self.y > mundo.camara_y + alto_pantalla)

    def draw(self, pantalla, x, y):
        """Dibuja la bala o su animación de colisión."""
        if self.colisionando:
            if self.frame_actual < len(self.sprites_colision):
                pantalla.blit(self.sprites_colision[self.frame_actual],
                              (self.rect_element.x - x, self.rect_element.y - y))
        else:
            self.dibujar(pantalla, x, y)


