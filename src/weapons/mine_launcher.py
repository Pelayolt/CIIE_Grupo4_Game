import pygame
from elements.interactable.mine import Mine
from weapons.weapon import Weapon

class MineLauncher(Weapon):
    def __init__(self, tank):
        super().__init__(tank)
        self.tiempo_inicio = pygame.time.get_ticks()
        # self.imagenes_accesorio_base = self.tank.generar_sprites(settings.RESIZE_PLAYER, settings.RESIZE_PLAYER, "jugador", "armas/mina")
        self.activo = False
        self.minas = []

    def activar_secundaria(self, tank, mundo):
        self.actvio = True
        self.tiempo_inicio = pygame.time.get_ticks()
        nova_mina = Mine(self.tank.rect_element.x, self.tank.rect_element.y)
        mundo.elementos_por_capa[2].append(nova_mina)
        mundo.elementos_actualizables.append(nova_mina)
        self.minas.append(nova_mina)

    def update_secundaria(self, tank, mundo):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio  # Milisegundos desde el inicio del Dash

        for mina in self.minas:
            if (tiempo_actual - mina.tiempo_creacion) > mina.duracion:
                mina.interactuar()
                self.minas.remove(mina)

    def dibujar_minas(self, mundo):
        for mina in self.minas:
            mina.dibujar(mundo)