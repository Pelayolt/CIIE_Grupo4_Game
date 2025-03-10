import pygame
from extras.resourcesmanager import ResourceManager
from extras.settings import CollisionLayer, RESIZE_PLAYER, EVENTO_JUGADOR_MUERTO
from tanks.tank import Tank
from weapons import *

class Player(Tank):

    def __init__(self, x, y, controller):

        # Llamamos primero al constructor de la clase base (Tank)
        super().__init__(4, 3, x, y, RESIZE_PLAYER, RESIZE_PLAYER, collision_layer=CollisionLayer.PLAYER, tank_type="jugador")

        # Equipamos armas
        self.armas = [Weapon(self), Dash(self), Shotgun(self), ReboungGun(self), MineLauncher(self)]  # Lista de armas
        self.armas_pos = 0  # Índice de arma secundaria equipada
        self.colision_layer_balas = CollisionLayer.BULLET_PLAYER
        self.barra_vida = ResourceManager.load_animation(f"vida_jugador.png", 48, 7, 5, resizex=5, resizey=0.5)
        self.control = controller

    def eventos(self, mundo):
        teclas = pygame.key.get_pressed()
        self.movimiento_x, self.movimiento_y = self.obtener_movimiento(teclas)
        self.gestionar_armas(mundo, teclas)

    def update(self, mundo):
        if self.vida <= 0:
            pygame.event.post(pygame.event.Event(EVENTO_JUGADOR_MUERTO))
            self.vida = self.vida_inicial

        self.mover(mundo)
        self.arma.update_secundaria(self, mundo)
        self.arma.update(mundo=mundo)
        self.verificar_fuera_pantalla(mundo)

    def mover(self, mundo):
        self.actualizar_posicion(self.movimiento_x, self.movimiento_y, mundo)

    def obtener_movimiento(self, teclas):
        mov_x = (self.control.derecha(teclas) - self.control.izquierda(teclas)) * self.velocidad
        mov_y = (self.control.abajo(teclas) - self.control.arriba(teclas)) * self.velocidad
        if mov_x != 0 and mov_y != 0:
            mov_x *= 0.707
            mov_y *= 0.707
        return mov_x, mov_y

    def verificar_fuera_pantalla(self, mundo):
        if self.rect_element.right > mundo.camara_x + mundo.ancho_pantalla + 50:
            mundo.cambiar_pantalla("derecha")
        elif self.rect_element.left < mundo.camara_x - 50:
            mundo.cambiar_pantalla("izquierda")
        elif self.rect_element.bottom > mundo.camara_y + mundo.alto_pantalla + 50:
            mundo.cambiar_pantalla("abajo")
        elif self.rect_element.top < mundo.camara_y - 50:
            mundo.cambiar_pantalla("arriba")

    def gestionar_armas(self, mundo, teclas):
        if self.control.principal(teclas):
            if pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= 1000:
                self.arma.activar()
                self.tiempo_ultimo_disparo = pygame.time.get_ticks()

        if self.control.secundaria(teclas):
            self.usar_arma_especial(mundo)

    def cambiar_arma_secundaria(self):
        # Cambia a la siguiente arma en la lista (ciclo circular)
        self.armas_pos = (self.armas_pos + 1) % len(self.armas)
        self.arma = self.armas[self.armas_pos]
        self.arma.cambio_de_arma()

    def draw(self, pantalla, x, y):
        #pantalla, self.ancho_pantalla, self.alto_pantalla

        self.dibujar(pantalla, x, y) #Dibujar base tanque
        self.arma.dibujar_arma(pantalla, x, y)

    def calcular_direccion_canon(self, mundo, jugador):
        # Obtener la posición del ratón en relación con la cámara
        cursorx, cursory = pygame.mouse.get_pos()
        dirx = cursorx - (self.rect_element.centerx - mundo.camara_x)
        diry = cursory - (self.rect_element.centery - mundo.camara_y)

        return dirx, diry
