import pygame
from src.bullet import Bala

class Player:
    def __init__(self):
        # Cargar imágenes del tanque y escalarlas
        self.sprites = {
            "izquierda": self.cargar_y_escalar_imagen("../res/tanque_izquierda.png", 1.5),
            "derecha": self.cargar_y_escalar_imagen("../res/tanque_derecha.png", 1.5),
            "arriba": self.cargar_y_escalar_imagen("../res/tanque_arriba.png", 1.5),
            "abajo": self.cargar_y_escalar_imagen("../res/tanque_abajo.png", 1.5),
            "arriba_izquierda": self.cargar_y_escalar_imagen("../res/tanque_arriba_izquierda.png", 1.5),
            "arriba_derecha": self.cargar_y_escalar_imagen("../res/tanque_arriba_derecha.png", 1.5),
            "abajo_izquierda": self.cargar_y_escalar_imagen("../res/tanque_abajo_izquierda.png", 1.5),
            "abajo_derecha": self.cargar_y_escalar_imagen("../res/tanque_abajo_derecha.png", 1.5),
        }
        self.image = self.sprites["abajo"]
        self.rect = self.image.get_rect(center=(400, 300))
        self.velocidad = 1
        self.direccion = "abajo"  # Dirección inicial del tanque
        self.balas = []  # Lista para almacenar las balas disparadas
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()  # Tiempo del último disparo

    def cargar_y_escalar_imagen(self, ruta, escala):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (imagen.get_width() * escala, imagen.get_height() * escala))

    def update(self, pantalla ,muro):
        teclas = pygame.key.get_pressed()
        direccion = None
        nuevo_rect = self.rect.copy()

        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
            nuevo_rect.x -= self.velocidad * 0.707
            nuevo_rect.y -= self.velocidad * 0.707
            direccion = "arriba_izquierda"
        elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_UP] or teclas[pygame.K_w]):
            nuevo_rect.x += self.velocidad * 0.707
            nuevo_rect.y -= self.velocidad * 0.707
            direccion = "arriba_derecha"
        elif (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            nuevo_rect.x -= self.velocidad * 0.707
            nuevo_rect.y += self.velocidad * 0.707
            direccion = "abajo_izquierda"
        elif (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            nuevo_rect.x += self.velocidad * 0.707
            nuevo_rect.y += self.velocidad * 0.707
            direccion = "abajo_derecha"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            nuevo_rect.x -= self.velocidad
            direccion = "izquierda"
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            nuevo_rect.x += self.velocidad
            direccion = "derecha"
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
            nuevo_rect.y -= self.velocidad
            direccion = "arriba"
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            nuevo_rect.y += self.velocidad
            direccion = "abajo"

        # Verificar colisión con el muro
        if not nuevo_rect.colliderect(muro):
            self.rect = nuevo_rect

        if direccion:
            self.image = self.sprites[direccion]
            self.direccion = direccion  # Actualizar la dirección del tanque

        # Verificar el clic izquierdo del ratón para disparar
        if pygame.mouse.get_pressed()[0]:  # 0 es el botón izquierdo
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_disparo >= 2000:  # Verifica si han pasado 2 segundos
                self.disparar()
                self.tiempo_ultimo_disparo = tiempo_actual  # Actualiza el tiempo del último disparo

        # Actualizar las balas
        for bala in self.balas[:]:
            bala.update()
            if bala.fuera_de_pantalla(pantalla):  # Eliminar balas fuera de la pantalla
                self.balas.remove(bala)

    def disparar(self):
        # Crear una nueva bala en la posición del tanque según la dirección
        nueva_bala = Bala(self.rect.centerx, self.rect.centery, self.direccion)
        self.balas.append(nueva_bala)

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
        # Dibujar las balas
        for bala in self.balas:
            bala.draw(pantalla)

