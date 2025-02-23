import numpy as np
import pygame

import settings
from bullet import Bala
from elements import Elemento
from settings import CollisionLayer
from weapon import Dash, Weapon
import spritesheet


class Tank(Elemento):

    def __init__(self, vida, velocidad, x, y, resizex, resizey, tank_type="", collision_layer=CollisionLayer.NONE, ruta=""):

        self.vida = vida
        self.velocidad = velocidad
        self.velocidad_base = 3

        self.ruta = ruta
        self.tank_type = tank_type

        # Generamos sprites para el tanque
        self.sprites = self.generar_sprites(ruta, resizex, resizey, tank_type)

        super().__init__(x, y, self.sprites["abajo"], collision_layer)

        self.arma = Weapon(self)

        self.direccion = "abajo"
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()

        self.ultimo_uso_secundaria = pygame.time.get_ticks()

    def generar_sprites(self, ruta, resizex, resizey, tank_type):
        sprite_base = self.escalar_y_cargar(self, ruta + "bodies/body_tracks" + tank_type + ".png", resizex, resizey)
        sprite_base_45 = self.escalar_y_cargar(self, ruta + "bodies/body_tracks_45" + tank_type + ".png", resizex, resizey)

        return {
            "arriba": sprite_base,
            "derecha": pygame.transform.rotate(sprite_base, -90),
            "izquierda": pygame.transform.rotate(sprite_base, 90),
            "abajo": pygame.transform.rotate(sprite_base, 180),
            "arriba_izquierda": sprite_base_45,
            "arriba_derecha": pygame.transform.rotate(sprite_base_45, -90),
            "abajo_izquierda": pygame.transform.rotate(sprite_base_45, 90),
            "abajo_derecha": pygame.transform.rotate(sprite_base_45, 180)
        }

    def establecer_posicion(self, x, y):
        self.rect_element.x = x
        self.rect_element.y = y

    def actualizar_posicion(self, movimiento_x, movimiento_y, mundo):
        self.verificar_colision(movimiento_x, 0, mundo)
        self.verificar_colision(0, movimiento_y, mundo)

        direccion = self.determinar_direccion(movimiento_x, movimiento_y)
        if direccion:
            self.direccion = direccion
            self.imagen = self.sprites[direccion]

    def verificar_colision(self, dx, dy, mundo):
        self.rect_element.x += dx
        self.rect_element.y += dy

        if any(self.check_collision(e) for e in mundo.elementos_por_capa[2]):
            self.rect_element.x -= dx
            self.rect_element.y -= dy

    def determinar_direccion(self, dx, dy):
        direcciones = {
            (-1, -1): "arriba_izquierda",
            (1, -1): "arriba_derecha",
            (-1, 1): "abajo_izquierda",
            (1, 1): "abajo_derecha",
            (-1, 0): "izquierda",
            (1, 0): "derecha",
            (0, -1): "arriba",
            (0, 1): "abajo"
        }
        dx = -1 if dx < 0 else (1 if dx > 0 else 0)
        dy = -1 if dy < 0 else (1 if dy > 0 else 0)
        return direcciones.get((dx, dy), self.direccion)  # Usa la última dirección si no encuentra coincidencia

    def equipar_especial(self, weapon):
        # Equipamos armas
        self.arma = weapon  # Equipar el Dash
        self.ultimo_uso_secundaria = pygame.time.get_ticks()

    def usar_arma_especial(self):  # usar habilidad especial
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_uso_secundaria >= settings.COOLDOWN:
            self.arma.activar_secundaria(self)
            self.ultimo_uso_secundaria = tiempo_actual  # Reinicia el cooldown



