import math
import pygame
import settings
from interactuable import Boton
from ui import Ui
from world import World
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.tamaño_pantalla = 1
        self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.ejecutando = True
        self.en_juego = True


        self.jugador = Player(0, 0)
        self.mundo = World(self.pantalla, "1", self.jugador)
        self.ui = Ui(self.mundo)

    def run(self):
        self.set_cursor()
        while self.ejecutando:
            self.handle_events()
            if self.en_juego:
                self.update()
                self.draw()
                self.clock.tick(settings.FPS)

        pygame.quit()

    def set_cursor(self):
        cursor_image = pygame.image.load("../res/UI/mirilla.png")
        cursor = pygame.cursors.Cursor((cursor_image.get_width() // 2, cursor_image.get_height() // 2), cursor_image)
        pygame.mouse.set_cursor(cursor)

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Detecta cuando se presiona ESC
                    #self.ejecutando = False  # Termina el juego
                    self.en_juego = not self.en_juego
                    if self.en_juego == False:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.pause_menu()
                    else:
                        self.set_cursor()
                    pygame.display.flip()
                elif evento.key == pygame.K_F11:
                    self.pantalla = pygame.display.set_mode((settings.ANCHO, settings.ALTO))
                elif evento.key == pygame.K_e:  # Presionar "E" para activar botones
                    for capa in self.mundo.elementos_por_capa.values():
                        for elemento in capa:
                            if isinstance(elemento, Boton) and self.jugador.rect_element.colliderect(
                                    elemento.rect_element):
                                elemento.activar()
                if evento.key == pygame.K_g: #cambiar arma secundaria con la tecla G (temporario mientras no se pueden encontrar las armas en el juego)
                    self.jugador.cambiar_arma_secundaria()
                if evento.key == pygame.K_m:
                    if self.mundo.mundo_number == "1":
                        self.mundo = World(self.pantalla, "2", self.jugador, True)
                    elif self.mundo.mundo_number == "2":
                        self.mundo = World(self.pantalla, "1", self.jugador)
                    elif self.mundo.mundo_number == "3":
                        self.mundo = World(self.pantalla, "1", self.jugador)


    def pause_menu(self):

        # Opciones del menú
        menu_items = ["Back to Game", "Options", "Quit"]
        selected_item = 0

        # Fuente
        font = pygame.font.Font(None, 74)

        for index, item in enumerate(menu_items):
            color = settings.WHITE if index == selected_item else (150, 150, 150)
            text = font.render(item, True, color)
            rect = text.get_rect(center=(settings.ANCHO/2, (settings.ALTO/2 - 100 + index * 100)))
            self.mundo.pantalla.blit(text, rect)

    def update(self):
        self.jugador.update(self.mundo)
        self.mundo.update()

    def draw(self):
        self.mundo.draw(self.jugador)
        
        for enemigo in self.mundo.enemigos:
            enemigo.dibujar_enemigo(self.mundo, self.jugador)
            #arma
        self.jugador.draw(self.mundo)

        # for enemigo in self.mundo.enemigos:
            #balas
        self.jugador.arma.dibujar_balas(self.mundo)

        if self.mundo.hasSky:
            self.mundo.draw_sky()

        for enemigo in self.mundo.enemigos:
            self.ui.draw_health_bar(enemigo)
        self.ui.draw_health_bar_player(self.jugador)

        pygame.display.flip()


