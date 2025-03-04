import math

import pygame

import settings
from resourcesmanager import ResourceManager


class Ui:
    def __init__(self, mundo):
        """Inicializa la UI con la pantalla y el tanque del jugador."""
        self.mundo = mundo
        self.font = pygame.font.Font(None, 36)  # Fuente para los textos
        self.cursor_image = ResourceManager.load_and_scale_image("mirilla.png", 0.75, 0.75)  # Cursor personalizado
        self.set_cursor()


    def set_cursor(self):
        """Establece un cursor personalizado."""
        cursor_size = (self.cursor_image.get_width() // 2, self.cursor_image.get_height() // 2)
        cursor = pygame.cursors.Cursor(cursor_size, self.cursor_image)
        pygame.mouse.set_cursor(cursor)

    def dibujar_minimapa(self):
        """Dibuja el minimapa con habitaciones y conexiones."""
        minimapa = pygame.Surface((200, 100), pygame.SRCALPHA)  # Superficie del minimapa
        minimapa.fill((0, 0, 0, 0))  # Fondo completamente transparente

        # Posiciones de cada habitación en el minimapa
        posiciones = {}

        # Dibujar habitaciones
        for fila in range(4):
            for col in range(3):
                x = col * (settings.HABITACION_ANCHO + settings.ESPACIADO)
                y = fila * (settings.HABITACION_ALTO + settings.ESPACIADO)

                posiciones[(fila, col)] = (x + settings.HABITACION_ANCHO // 2, y + settings.HABITACION_ALTO // 2)

                pygame.draw.rect(minimapa, settings.NEGRO_TRANSLUCIDO, (x, y, settings.HABITACION_ANCHO, settings.HABITACION_ALTO), border_radius=3)

        # Dibujar conexiones con colores variables
        for ((y1, x1), (y2, x2), color) in settings.CONEXIONES:
            if (y1, x1) in posiciones and (y2, x2) in posiciones:
                # Obtener coordenadas de los centros de las habitaciones
                x1_px, y1_px = posiciones[(y1, x1)]
                x2_px, y2_px = posiciones[(y2, x2)]

                # Calcular la dirección de la línea
                dx, dy = x2_px - x1_px, y2_px - y1_px
                distancia = math.sqrt(dx ** 2 + dy ** 2)

                # Normalizar dirección y ajustar para que la línea comience desde el borde de la habitación
                if distancia > 0:
                    ajuste_x = (dx / distancia) * (settings.HABITACION_ANCHO // 2)
                    ajuste_y = (dy / distancia) * (settings.HABITACION_ALTO // 2)

                    x1_px += ajuste_x
                    y1_px += ajuste_y
                    x2_px -= ajuste_x
                    y2_px -= ajuste_y

                # Dibujar la línea ajustada
                pygame.draw.line(minimapa, color, (x1_px, y1_px), (x2_px, y2_px), 8)

        # Dibujar el minimapa en la pantalla
        self.mundo.pantalla.blit(minimapa, settings.MINIMAPA_POS)

    def draw_health_bar(self, tank):
        """Dibuja la barra de vida justo debajo del tanque."""

        # Posición del tanque
        x = tank.rect_element.x + tank.rect_element.width // 2 - tank.barra_vida[0].get_width() // 2 - self.mundo.camara_x
        y = tank.rect_element.y - self.mundo.camara_y

        # Asegurar que la vida no sea negativa
        vida_actual = max(tank.vida, 0)
        self.mundo.pantalla.blit(tank.barra_vida[vida_actual], (x, y))

    def draw_health_bar_player(self, jugador):
        x = 20
        y = 20

        # Asegurar que la vida no sea negativa
        vida_actual = max(jugador.vida, 0)
        self.mundo.pantalla.blit(jugador.barra_vida[vida_actual], (x, y))

