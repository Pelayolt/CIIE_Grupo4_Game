from .elemento_gui import ElementoGUI
from ..extras.settings import Settings
import pygame

class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, color, texto, posicion):
        # Se crea la imagen del texto
        ElementoGUI.__init__(self, pantalla)
        self.idle = self.font.render(texto, True, color)
        self.text = self.idle
        self.hover = self.font.render(texto, True, Settings.VERDE)
        self.rect = self.text.get_rect()
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.text, self.rect)

    
class TextoRes(TextoGUI):
    def __init__(self, pantalla, color, texto, posicion, res, director):
        self.res = res
        self.director = director
        super().__init__(pantalla, color, texto, posicion)
    def accion(self):
        from .menu import MainMenu

        if self.res == (1024,576):
            Settings.RESOLUTION_SCALE = 1
        elif self.res == (768,432):
            Settings.RESOLUTION_SCALE = 0.75
        elif self.res == (1280,720):
            Settings.RESOLUTION_SCALE = 1.25

        Settings.updateRes(Settings)
        print(Settings.RESOLUTION_SCALE)
        print(Settings.ANCHO)
        
        self.director.pantalla = pygame.display.set_mode(self.res)
        escena = MainMenu(self.director)
        escena.irAConfiguraciones()
        self.director.cambiar_escena(escena)




class TextoJugar(TextoGUI):
    def __init__(self, pantalla,posicion):
        TextoGUI.__init__(self, pantalla, Settings.NEGRO, 'Jugar', posicion)
        
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class TextoResume(TextoGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, Settings.NEGRO, "Continuar", posicion)

    def accion(self):
        self.pantalla.menu.continuar()

class TextoSalir(TextoGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, Settings.NEGRO, "Salir", posicion)
    
    def accion(self):
        self.pantalla.menu.salirPrograma()

class TextoConfiguraciones(TextoGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, Settings.NEGRO, "Configuraciones", posicion)

    def accion(self):
        self.pantalla.menu.irAConfiguraciones()
