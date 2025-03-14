import pygame

from ..extras import TIME_FRAME, ResourceManager, RESIZE_CANNON
from .bullets import BouncingBullet
from .weapon import Weapon

class ReboungGun(Weapon):
    def __init__(self, tank):
        from ..tanks import Player

        super().__init__(tank)
        self.tiempo_inicio = None #Guarda el tiempo de activacivación
        self.esPlayer = isinstance(self.tank, Player)
        if self.esPlayer:
            self.animacion = ResourceManager.load_animation("turret_02_mk1.png", 128, 128, 8)
            self.imagen_canon_base = self.animacion[0]
        else:
            self.animacion = ResourceManager.load_animation(f"weapons{tank.tank_level}_128x128.png", 128, 128, 16, RESIZE_CANNON, RESIZE_CANNON)
            self.imagen_canon_base = self.animacion[4]
        self.activo = False

        self.frame_actual = 0
        self.ultimo_cambio_frame = 0

    def activar_secundaria(self, mundo, tank=None):
        self.tiempo_inicio = pygame.time.get_ticks()
        bala_rebote = BouncingBullet(self)
        mundo.add_bullet(bala_rebote)
        self.activo = True

    def update_secundaria(self, tank, mundo):
        if self.activo and self.esPlayer:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual

            # Si han pasado 30 ms desde el último cambio de frame
            if tiempo_actual - self.ultimo_cambio_frame >= TIME_FRAME:
                self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio

                if self.frame_actual < len(self.animacion) - 1:
                    self.frame_actual += 1
                else:
                    self.frame_actual = 0
                    self.activo = False  # Desactiva la animación cuando termina

                # Actualizar la imagen del cañón
                self.imagen_canon_base = self.animacion[self.frame_actual]
                self.imagen_canon = self.imagen_canon_base