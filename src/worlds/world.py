import re  # Para extraer números del nombre del archivo
from abc import ABC

import pygame

from .. import Director
from ..elements.interactable.pickable import PickableCollectable
from ..extras import Settings, ResourceManager
from ..elements import Wall, LowWall
from ..elements.activateable import Door
from ..menus.menu import PauseMenu, GameOverMenu
from ..scene import Scene
from ..tanks import Player
from ..tanks.enemies import Enemy
from ..tanks.enemies.bosses import WarTrain
from ..ui import Ui
from .element_factory import ElementFactory


class World(Scene, ABC):
    def __init__(self, alto_pantalla, ancho_pantalla, world_number, song_name):

        super().__init__(Director())

        self.ui = Ui()
        self.control = Settings.controller
        self.world_number = world_number
        self.player = self.director.partida.player

        self.previous_weapon = self.player.arma
        self.previous_key_objs = self.player.key_objs

        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.song_name = song_name

        self.capas = {}
        self.sprites_por_capa = {}
        self.hasSky = False
        self.CONEXIONES = []
        self.num_pantallas_ancho = 3  # Número de pantallas en el eje X
        self.num_pantallas_alto = 4  # Número de pantallas en el eje Y
        self.tiles_por_pantalla_x = self.ancho_pantalla // Settings.TILE_SIZE  # Ancho en tiles de una pantalla
        self.tiles_por_pantalla_y = self.alto_pantalla // Settings.TILE_SIZE  # Alto en tiles de una pantalla

        self.elementos_por_capa = {}
        self.elementos_actualizables = []
        self.enemigos = []

        # Variables de transición
        self.en_transicion = False
        self.enfocando_objeto = False
        self.tiempo_inicio = 0
        self.camara_x, self.camara_y = 0, 0
        self.destino_camara_x, self.destino_camara_y = 0,0

        self.minimap_active = False

        self.traps = ()
        self.lowWalls = ()
        self.decorations = ()

        self.balas = []
        self.minas = []

        # Cargar los mapas desde los archivos CSV
        archivos_mapa = ResourceManager.buscar_archivos_mapa(world_number)
        for archivo in archivos_mapa:
            capa_numero = self.extraer_numero_capa(archivo)  # Obtener número de capa desde el nombre
            self.capas[capa_numero] = ResourceManager.load_map_from_csv(archivo)

        # Cargar dinámicamente los sprites según la capa
        for capa in self.capas.keys():
            carpeta_elementos = ResourceManager.locate_resource(f"elementos_{world_number}_{capa}")
            self.sprites_por_capa[capa] = ResourceManager.load_files_from_folder(carpeta_elementos)

        # Inicializar el diccionario para almacenar elementos por capas y pantallas, elementos_por_capa_y_pantalla[2][0][1] contiene todos los elementos de la capa 2, en la pantalla correspondientes a la fila 0 columna 1
        self.elementos_por_capa_y_pantalla = {
            capa: [[[] for _ in range(self.num_pantallas_ancho)] for _ in range(self.num_pantallas_alto)]
            for capa in self.capas.keys()
        }

        self.num_filas = len(self.capas[1]) if 1 in self.capas else 0
        self.num_columnas = len(self.capas[1][0]) if self.num_filas > 0 else 0
        self.elementos_por_capa = {capa: [] for capa in self.capas.keys()}

        self.started = False

    def play_music(self):
        ResourceManager.load_and_play_wav(self.song_name, -1)

    def stop_music(self):
        ResourceManager.stop_and_unload_wav(self.song_name)

    @staticmethod
    def extraer_numero_capa(archivo):
        """Extrae el número de capa desde el nombre del archivo 'Mapa_X_Y.csv'."""
        match = re.search(r'Mapa_\d+_(\d+)\.csv', archivo)
        return int(match.group(1)) if match else 1  # Si no encuentra número, asume capa 1

    def get_parametros(self):
        return self.alto_pantalla, self.ancho_pantalla

    def generar_elementos(self, mapa_tiles, lista_elementos, sprites, lista_enemigos, lista_actualizables, capa):
        """Crea los elementos del mapa y los agrupa por pantallas y capas."""
        puertas = {}
        id_enemigo = 1
        for y, fila in enumerate(mapa_tiles):
            for x, valor in enumerate(fila):
                valor = int(valor)  # Asegurar que es un número válido
                id_enemigo += 1
                elemento = ElementFactory.create_element(valor, x, y, sprites, puertas, self, id_enemigo)

                if isinstance(elemento, PickableCollectable) and self.player.key_objs >= self.world_number:
                    elemento = None

                if elemento:
                    lista_elementos.append(elemento)  # Agregar a la lista general de elementos

                    # Calcular en qué pantalla se encuentra este elemento
                    col_pantalla = x // self.tiles_por_pantalla_x
                    fila_pantalla = y // self.tiles_por_pantalla_y

                    # Agregar el elemento a su pantalla correspondiente
                    if isinstance(elemento, Player) and capa == 2:
                        for fila in self.elementos_por_capa_y_pantalla[capa]:  # Recorre todas las filas
                            for columna in fila:  # Recorre todas las columnas dentro de cada fila
                                columna.append(elemento)
                    elif isinstance(elemento, WarTrain) and capa == 2:
                        for columna in self.elementos_por_capa_y_pantalla[capa][0]:  # Recorre todas las columnas dentro de cada fila
                            columna.append(elemento)
                    else:
                        self.elementos_por_capa_y_pantalla[capa][fila_pantalla][col_pantalla].append(elemento)

                    # Clasificar elementos especiales
                    if isinstance(elemento, Enemy):
                        lista_enemigos.append(elemento)
                    elif hasattr(elemento, "update") and not isinstance(elemento, Player):
                        lista_actualizables.append(elemento)

    def generar_mapas_binarios(self):
        """Genera mapas binarios donde haya 1s donde haya Muro/MuroBajo/Puerta y 0s en el resto, inflando obstáculos."""
        mapa_binario = [[0 for _ in range(self.num_columnas)] for _ in range(self.num_filas)]

        # Marcar obstáculos en la matriz
        for elemento in self.elementos_por_capa[2]:
            if isinstance(elemento, (Wall, LowWall, Door)):
                tile_x = elemento.x // Settings.TILE_SIZE
                tile_y = elemento.y // Settings.TILE_SIZE
                mapa_binario[tile_y][tile_x] = 1

        # Inflar obstáculos (doblando el grosor)
        inflado = [[valor for valor in fila] for fila in mapa_binario]  # Copia para modificar sin afectar la original
        for y in range(self.num_filas):
            for x in range(self.num_columnas):
                if mapa_binario[y][x] == 1:
                    # Inflar en un radio de 1 celda
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.num_filas and 0 <= nx < self.num_columnas:
                                inflado[ny][nx] = 1

        # Crear submatrices para cada grid de pantalla
        tiles_por_pantalla_x = self.ancho_pantalla // Settings.TILE_SIZE
        tiles_por_pantalla_y = self.alto_pantalla // Settings.TILE_SIZE
        matriz_mapas = [[None for _ in range(4)] for _ in range(3)]

        for i in range(3):
            for j in range(4):
                submatriz = []
                for y in range(tiles_por_pantalla_y):
                    fila = inflado[j * tiles_por_pantalla_y + y][i * tiles_por_pantalla_x:(i + 1) * tiles_por_pantalla_x]
                    submatriz.append(fila)
                matriz_mapas[i][j] = submatriz

        return matriz_mapas

    def add_bullet(self, bala):
        self.balas.append(bala)

    def add_mine(self, mine):
        self.minas.append(mine)

    def cambiar_pantalla(self, direccion):

        dir_cam = {
            "derecha": (1, 0),
            "izquierda": (-1, 0),
            "abajo": (0, 1),
            "arriba": (0, -1)
        }

        for enemigo in self.enemigos:
            if enemigo.en_la_misma_pantalla(self.player):
                enemigo.patrullar()

        if not self.en_transicion and not self.enfocando_objeto:
            # Si no hay transición en curso, iniciar una
            self.tiempo_inicio = pygame.time.get_ticks()  # Guarda el tiempo actual

            trans_x, trans_y = dir_cam[direccion]

            self.destino_camara_x = self.camara_x + trans_x*self.ancho_pantalla
            self.destino_camara_y = self.camara_y + trans_y*self.alto_pantalla

            self.en_transicion = True

    def actualizar_transicion(self):
        """Actualiza la transición de la cámara."""
        if not self.en_transicion:
            return

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

    def elemento_en_pantalla(self, elemento):
        """Verifica si el elemento está dentro del área visible."""
        return (
                self.camara_x - Settings.TILE_SIZE <= elemento.rect_element.x < self.camara_x + self.ancho_pantalla + Settings.TILE_SIZE
                and self.camara_y - Settings.TILE_SIZE <= elemento.rect_element.y < self.camara_y + self.alto_pantalla + Settings.TILE_SIZE
        )

    def obtener_pantalla_actual(self):
        """Calcula en qué pantalla está el jugador basado en su posición."""
        col_pantalla = int(self.camara_x // self.ancho_pantalla)
        fila_pantalla = int(self.camara_y // self.alto_pantalla)

        # Asegurar que está dentro de los límites del mundo
        col_pantalla = max(0, min(col_pantalla, self.num_pantallas_ancho - 1))
        fila_pantalla = max(0, min(fila_pantalla, self.num_pantallas_alto - 1))

        return fila_pantalla, col_pantalla

    def eventos(self, eventos):
        """ Lógica común para todos los mundos """
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.director.salir_programa()
            elif evento.type == Settings.EVENTO_JUGADOR_MUERTO:
                self.player.vida = self.player.vida_inicial
                self.player.cambiar_secundaria(self.previous_weapon)
                self.player.key_objs = self.previous_key_objs
                self.director.apilar_escena(GameOverMenu(self.director))
            elif evento.type == Settings.EVENTO_COLECCIONABLE_RECOGIDO:
                self.player.key_objs += 1

            if self.control.pausar(evento):
                self.director.apilar_escena(PauseMenu( self.director))

            #if self.control.change_weapon(evento):
            #    self.player.cambiar_arma_secundaria()  <-- Opcion de desarrollador

            if self.control.open_minimap(evento):
                self.minimap_active = not self.minimap_active

            self.manejar_evento_especifico(evento)

        self.player.eventos(self)

    def manejar_evento_especifico(self, evento):
        pass

    def update(self, time):

        if not self.started:
            self.play_music()
            self.started = True

        self.player.update(self)

        """Actualiza el mundo y los elementos."""
        for elemento in self.enemigos:
            elemento.update(self.player, self)

        for elemento in self.elementos_actualizables:
            elemento.update(self.player)

        for bala in self.balas[:]:
            if bala.update(self, self.ancho_pantalla, self.alto_pantalla):
                self.balas.remove(bala)

        for lista in [self.enemigos, self.elementos_actualizables, self.elementos_por_capa[2]]:
            for elemento in lista.copy():
                if elemento.eliminar:
                    elemento.animacion_elimninar()
                    lista.remove(elemento)

        for i, fila in enumerate(self.elementos_por_capa_y_pantalla[2]):
            for j, columna in enumerate(fila):
                for elemento in columna:
                    if elemento.eliminar:
                        elemento.animacion_elimninar()
                        self.elementos_por_capa_y_pantalla[2][i][j].remove(elemento)

        self.director.partida.update_save_data(self.camara_x, self.camara_y, self.num_filas, self.num_columnas,
                                               self.world_number)

    def dibujar(self, pantalla):
        self.draw(pantalla)



        self.player.draw(pantalla, self.camara_x, self.camara_y)

        for enemigo in self.enemigos:
            enemigo.dibujar_enemigo(pantalla, self.camara_x, self.camara_y)

        for bala in self.balas:
            bala.draw(pantalla, self.camara_x, self.camara_y)

        for mina in self.minas:
            mina.dibujar(pantalla, self.camara_x, self.camara_y)

        if self.hasSky:
            self.draw_sky(pantalla)

        for enemigo in self.enemigos:
            self.ui.draw_health_bar(enemigo, pantalla, self.camara_x, self.camara_y)

        self.ui.draw_health_bar_player(self.player, pantalla)
        if self.minimap_active:
            self.ui.dibujar_minimapa(self.player, self, pantalla)

    def draw(self, pantalla):
        """Dibuja solo los elementos de la pantalla actual y las pantallas contiguas, sin incluir las diagonales."""

        for capa in sorted(self.capas.keys()):  # Dibuja en orden numérico
            if self.hasSky and max(self.capas.keys()) == capa:
                break  # Si hay cielo, no dibujar la última capa aquí

            fila_pantalla, col_pantalla = self.obtener_pantalla_actual()

            # Dibujar la pantalla actual
            for elemento in self.elementos_por_capa_y_pantalla[capa][fila_pantalla][col_pantalla]:
                if self.elemento_en_pantalla(elemento):
                    elemento.dibujar(pantalla, self.camara_x, self.camara_y)

            # Dibujar las pantallas contiguas (arriba, abajo, izquierda, derecha)
            # Arriba
            if fila_pantalla > 0:
                for elemento in self.elementos_por_capa_y_pantalla[capa][fila_pantalla - 1][col_pantalla]:
                    if self.elemento_en_pantalla(elemento):
                        elemento.dibujar(pantalla, self.camara_x, self.camara_y)

            # Abajo
            if fila_pantalla < self.num_pantallas_alto - 1:
                for elemento in self.elementos_por_capa_y_pantalla[capa][fila_pantalla + 1][col_pantalla]:
                    if self.elemento_en_pantalla(elemento):
                        elemento.dibujar(pantalla, self.camara_x, self.camara_y)

            # Izquierda
            if col_pantalla > 0:
                for elemento in self.elementos_por_capa_y_pantalla[capa][fila_pantalla][col_pantalla - 1]:
                    if self.elemento_en_pantalla(elemento):
                        elemento.dibujar(pantalla, self.camara_x, self.camara_y)

            # Derecha
            if col_pantalla < self.num_pantallas_ancho - 1:
                for elemento in self.elementos_por_capa_y_pantalla[capa][fila_pantalla][col_pantalla + 1]:
                    if self.elemento_en_pantalla(elemento):
                        elemento.dibujar(pantalla, self.camara_x, self.camara_y)

        self.actualizar_transicion()

    def draw_sky(self, pantalla):
        """Dibuja solo la última capa (capa más alta) en la pantalla actual."""
        capa_mas_alta = max(self.capas.keys())
        fila_pantalla, col_pantalla = self.obtener_pantalla_actual()

        for elemento in self.elementos_por_capa_y_pantalla[capa_mas_alta][fila_pantalla][col_pantalla]:
            if self.elemento_en_pantalla(elemento):
                elemento.dibujar(pantalla, self.camara_x, self.camara_y)

        # Dibujar las pantallas contiguas (arriba, abajo, izquierda, derecha)
        # Arriba
        if fila_pantalla > 0:
            for elemento in self.elementos_por_capa_y_pantalla[capa_mas_alta][fila_pantalla - 1][col_pantalla]:
                if self.elemento_en_pantalla(elemento):
                    elemento.dibujar(pantalla, self.camara_x, self.camara_y)

        # Abajo
        if fila_pantalla < self.num_pantallas_alto - 1:
            for elemento in self.elementos_por_capa_y_pantalla[capa_mas_alta][fila_pantalla + 1][col_pantalla]:
                if self.elemento_en_pantalla(elemento):
                    elemento.dibujar(pantalla, self.camara_x, self.camara_y)

        # Izquierda
        if col_pantalla > 0:
            for elemento in self.elementos_por_capa_y_pantalla[capa_mas_alta][fila_pantalla][col_pantalla - 1]:
                if self.elemento_en_pantalla(elemento):
                    elemento.dibujar(pantalla, self.camara_x, self.camara_y)

        # Derecha
        if col_pantalla < self.num_pantallas_ancho - 1:
            for elemento in self.elementos_por_capa_y_pantalla[capa_mas_alta][fila_pantalla][col_pantalla + 1]:
                if self.elemento_en_pantalla(elemento):
                    elemento.dibujar(pantalla, self.camara_x, self.camara_y)



