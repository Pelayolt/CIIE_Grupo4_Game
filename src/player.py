import pygame
import settings
import numpy
from bullet import Bala

class Player:
    def __init__(self, pantalla):
        self.sprite_cannon = self.cargar_y_escalar_imagen("../res/tanque_player/tanque_canhon.png", settings.RESIZE_PLAYER)
        # Cargar imágenes del tanque y escalarlas
        self.sprites = {
            "izquierda": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_izquierda.png", settings.RESIZE_PLAYER),
            "derecha": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_derecha.png", settings.RESIZE_PLAYER),
            "arriba": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_arriba.png", settings.RESIZE_PLAYER),
            "abajo": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_abajo.png", settings.RESIZE_PLAYER),
            "arriba_izquierda": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_arriba_izquierda.png", settings.RESIZE_PLAYER),
            "arriba_derecha": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_arriba_derecha.png", settings.RESIZE_PLAYER),
            "abajo_izquierda": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_abajo_izquierda.png", settings.RESIZE_PLAYER),
            "abajo_derecha": self.cargar_y_escalar_imagen("../res/tanque_player/tanque_abajo_derecha.png", settings.RESIZE_PLAYER),
        }
        self.velocidad = 3
        self.direccion = "abajo"  # Dirección inicial del tanque
        self.balas = []  # Lista para almacenar las balas disparadas
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()  # Tiempo del último disparo
        self.angulo_cannon = 0

        self.pantalla = pantalla
        self.ancho_pantalla, self.alto_pantalla = pantalla.get_size()
        self.imagen_base_tanque = self.sprites["abajo"]
        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, -self.angulo_cannon)

        self.rect_base = self.imagen_base_tanque.get_rect(center=(self.ancho_pantalla // 2 + self.ancho_pantalla, self.alto_pantalla // 2 + self.alto_pantalla))
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_base.center)
        self.hitbox = pygame.Rect(self.ancho_pantalla // 2 + self.ancho_pantalla, self.alto_pantalla // 2 + self.alto_pantalla, self.rect_base.width * 0.8, self.rect_base.height * 0.8)


    def cargar_y_escalar_imagen(self, ruta, escala):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (int(imagen.get_width() * escala), int(imagen.get_height() * escala)))

    def update(self, pantalla, mundo):
        teclas = pygame.key.get_pressed()
        direccion = None
        nuevo_hitbox = self.hitbox.copy()

        # Movimiento en X e Y por separado
        movimiento_x = 0
        movimiento_y = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimiento_x = -self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimiento_x = self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            movimiento_y = -self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            movimiento_y = self.velocidad

        # Movimiento en diagonal (se reduce velocidad)
        if movimiento_x != 0 and movimiento_y != 0:
            movimiento_x *= 0.707  # √2/2 para mantener velocidad uniforme
            movimiento_y *= 0.707

        # --- Verificar colisiones por separado ---
        colision_x = False
        colision_y = False

        # 1. Mover en X y verificar colisión
        nuevo_hitbox.x += movimiento_x
        if any(nuevo_hitbox.colliderect(elemento.rect_element) for elemento in mundo.elementos):
            nuevo_hitbox.x -= movimiento_x  # Si hay colisión, deshacer movimiento en X
            colision_x = True

        # 2. Mover en Y y verificar colisión
        nuevo_hitbox.y += movimiento_y
        if any(nuevo_hitbox.colliderect(elemento.rect_element) for elemento in mundo.elementos):
            nuevo_hitbox.y -= movimiento_y  # Si hay colisión, deshacer movimiento en Y
            colision_y = True

        # Verificar si el jugador sale de la pantalla y cambiar la cámara
        if nuevo_hitbox.right > mundo.camara_x + mundo.ancho_pantalla + 50:
            mundo.cambiar_pantalla("derecha")
        elif nuevo_hitbox.left < mundo.camara_x - 50:
            mundo.cambiar_pantalla("izquierda")
        elif nuevo_hitbox.bottom > mundo.camara_y + mundo.alto_pantalla + 50:
            mundo.cambiar_pantalla("abajo")
        elif nuevo_hitbox.top < mundo.camara_y - 50:
            mundo.cambiar_pantalla("arriba")

        # --- Determinar la dirección final según los movimientos permitidos ---
        if movimiento_x < 0 and movimiento_y < 0 and not colision_x and not colision_y:
            direccion = "arriba_izquierda"
        elif movimiento_x > 0 and movimiento_y < 0 and not colision_x and not colision_y:
            direccion = "arriba_derecha"
        elif movimiento_x < 0 and movimiento_y > 0 and not colision_x and not colision_y:
            direccion = "abajo_izquierda"
        elif movimiento_x > 0 and movimiento_y > 0 and not colision_x and not colision_y:
            direccion = "abajo_derecha"
        elif movimiento_x < 0 and not colision_x:
            direccion = "izquierda"
        elif movimiento_x > 0 and not colision_x:
            direccion = "derecha"
        elif movimiento_y < 0 and not colision_y:
            direccion = "arriba"
        elif movimiento_y > 0 and not colision_y:
            direccion = "abajo"

        # Aplicar el movimiento final
        self.hitbox = nuevo_hitbox
        self.rect_base.center = self.hitbox.center  # Asegurar que el sprite coincida con la hitbox

        if direccion:
            self.imagen_base_tanque = self.sprites[direccion]
            self.direccion = direccion  # Actualizar la dirección del tanque

        # Disparo del tanque
        if pygame.mouse.get_pressed()[0]:  # 0 es el botón izquierdo
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_disparo >= 1000:  # 1 segundo entre disparos
                self.disparar()
                self.tiempo_ultimo_disparo = tiempo_actual  # Actualiza el tiempo del último disparo

        # Actualizar las balas
        for bala in self.balas[:]:
            if bala.update(mundo, self.ancho_pantalla, self.alto_pantalla):
                self.balas.remove(bala)

    def update_cannon_position(self, mundo):
        # Obtener la posición del ratón en relación con la cámara
        cursorx, cursory = pygame.mouse.get_pos()
        diff_x = cursorx - (self.rect_base.centerx - mundo.camara_x)
        diff_y = cursory - (self.rect_base.centery - mundo.camara_y)

        # Calcular el ángulo del cañón
        self.angulo_cannon = numpy.degrees(numpy.arctan2(diff_y, diff_x))  # Guardar el ángulo para disparos

        # Rotar la imagen del cañón
        self.imagen_canon = pygame.transform.rotate(self.sprite_cannon, -self.angulo_cannon + 90)

        # Mantener el cañón centrado en el tanque
        self.rect_canon = self.imagen_canon.get_rect(center=self.rect_base.center)

    def disparar(self):
        # Crear una nueva bala en la posición del cañón con el ángulo del cañón
        nueva_bala = Bala(self.rect_canon.centerx - 5, self.rect_canon.centery - 5, self.angulo_cannon)
        self.balas.append(nueva_bala)

    def draw(self, pantalla, mundo):

        # Dibujar las balas
        for bala in self.balas:
            bala.draw(pantalla, mundo)

        # Dibujar tanque
        pantalla.blit(self.imagen_base_tanque, (self.rect_base.x - mundo.camara_x, self.rect_base.y - mundo.camara_y))

        self.update_cannon_position(mundo)

        pantalla.blit(self.imagen_canon, (self.rect_base.centerx - self.rect_canon.width // 2 - mundo.camara_x, self.rect_base.centery - self.rect_canon.height // 2 - mundo.camara_y))

        #Mostrar la Hitbox
        #pygame.draw.rect(pantalla, (255, 0, 0), (self.hitbox.x - mundo.camara_x, self.hitbox.y - mundo.camara_y, self.hitbox.width, self.hitbox.height), 2)
