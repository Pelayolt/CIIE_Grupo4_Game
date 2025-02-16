import pygame
import maps
from player import Player
from settings import Color
from elements import Muro, Arbol, Arbusto, Vacio, Boton, Trampa
from enemy import Enemy
import settings
import math

import pygame

class World:
    def __init__(self, nombre, pantalla, player=None):
        self.nombre = nombre
        self.pantalla = pantalla
        self.player = player

        self.ancho_pantalla, self.alto_pantalla = pantalla.get_size()
        self.tamaño_tile = math.gcd(self.ancho_pantalla, self.alto_pantalla)

        # Cargar el mapa y redimensionarlo
        self.mapa_original = pygame.image.load(f"../res/mapas/{nombre}.png")
        self.mapa = pygame.transform.scale(self.mapa_original, (self.ancho_pantalla, self.alto_pantalla))

        # Obtener dimensiones del mapa en tiles
        self.num_filas = len(maps.mapa1_tiles)
        self.num_columnas = len(maps.mapa1_tiles[0])

        self.ancho_pantalla, self.alto_pantalla = pantalla.get_size()

        # Cargar imágenes de los sprites
        self.sprites = {
            "wall1": pygame.image.load("../res/elementos/wall1.png"),
            "wall7": pygame.image.load("../res/elementos/wall7.png"),
            "wall16": pygame.image.load("../res/elementos/wall16.png"),
            "wall21": pygame.image.load("../res/elementos/wall21.png"),
            "boton": pygame.image.load("../res/elementos/boton.png"),
            "cracks10": pygame.image.load("../res/elementos/cracks10.png"),
            "arbol1": pygame.image.load("../res/elementos/arbol1.png"),
            "arbusto1": pygame.image.load("../res/elementos/arbusto1.png"),
        }

        # Crear la cámara
        self.camara_x, self.camara_y = self.ancho_pantalla, self.alto_pantalla

        # Lista de elementos
        self.elementos = []
        self.generar_elementos()

        # Variables de transición
        self.en_transicion = False
        self.tiempo_inicio = 0
        self.destino_camara_x, self.destino_camara_y = self.ancho_pantalla, self.alto_pantalla

    def generar_elementos(self):
        """Crea los elementos del mapa ajustándolos al tamaño de la pantalla."""
        for y, fila in enumerate(maps.mapa1_tiles):
            for x, valor in enumerate(fila):
                if valor == 23:  # Player
                    if self.player is None:    self.player = Player(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile)
                    self.elementos.append(self.player)
                elif valor == 29:  # Muro
                    self.elementos.append(Muro(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["wall1"]))
                elif valor == 35:  # Muro
                    self.elementos.append(Muro(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["wall7"]))
                elif valor == 44:  # Muro
                    self.elementos.append(Muro(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["wall16"]))
                elif valor == 49:  # Vacio
                    self.elementos.append(Vacio(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["wall21"]))
                elif valor == 14:  # Enemigo
                    self.elementos.append(Enemy(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile))
                elif valor == 80:  # Enemigo
                    self.elementos.append(Boton(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["boton"]))
                elif valor == 59:  # Enemigo
                    self.elementos.append(Trampa(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["cracks10"]))
                elif valor == "2":  # Arbol
                    self.elementos.append(Arbol(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["arbol1"]))
                elif valor == "3":  # Arbusto
                    self.elementos.append(Arbusto(x * self.tamaño_tile, y * self.tamaño_tile, self.tamaño_tile,  self.sprites["arbusto1"]))

    def cambiar_pantalla(self, direccion):

        if not self.en_transicion:
        # Si no hay transición en curso, iniciar una
            self.tiempo_inicio = pygame.time.get_ticks()  # Guarda el tiempo actual
            if direccion == "derecha" and self.camara_x + self.ancho_pantalla < self.num_columnas * self.ancho_pantalla:
                self.destino_camara_x = self.camara_x + self.ancho_pantalla
                self.destino_camara_y = self.camara_y
                self.en_transicion = True
            elif direccion == "izquierda" and self.camara_x > 0:
                self.destino_camara_x = self.camara_x - self.ancho_pantalla
                self.destino_camara_y = self.camara_y
                self.en_transicion = True
            elif direccion == "abajo" and self.camara_y + self.alto_pantalla < self.num_filas * self.alto_pantalla:
                self.destino_camara_x = self.camara_x
                self.destino_camara_y = self.camara_y + self.alto_pantalla
                self.en_transicion = True
            elif direccion == "arriba" and self.camara_y > 0:
                self.destino_camara_x = self.camara_x
                self.destino_camara_y = self.camara_y - self.alto_pantalla
                self.en_transicion = True

    def actualizar_transicion(self):
        """Actualiza la transición de la cámara."""
        if self.en_transicion:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
            duracion_transicion = 1000

            if tiempo_transcurrido < duracion_transicion:
                # Interpolación lineal
                t = tiempo_transcurrido / duracion_transicion
                self.camara_x = self.camara_x + (self.destino_camara_x - self.camara_x) * t
                self.camara_y = self.camara_y + (self.destino_camara_y - self.camara_y) * t
            else:
                # Una vez que se ha completado la transición
                self.camara_x = self.destino_camara_x
                self.camara_y = self.destino_camara_y
                self.en_transicion = False

    def draw(self, pantalla):
        """Dibuja solo los elementos de la pantalla actual."""
        pantalla.blit(self.mapa, (0, 0))


        for elemento in self.elementos:
            if (
                self.camara_x - 80 <= elemento.rect_element.x < self.camara_x + self.ancho_pantalla + 80
                and self.camara_y - 80 <= elemento.rect_element.y < self.camara_y + self.alto_pantalla + 80
            ):
                # Dibujar con ajuste de la cámara
                elemento.dibujar(pantalla, self)

        self.actualizar_transicion()
