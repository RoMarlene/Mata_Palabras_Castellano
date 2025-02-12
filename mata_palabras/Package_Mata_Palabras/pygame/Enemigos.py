import pygame
import random
from Datos_juego import datos
from Esenciales import *

def crear_enemigos(DIMENSIONES_PANTALLA: tuple, numero_enemigos: int, tiempo_restante:int, diccionario_palabras:dict, palabras_seleccionadas: str)-> list:
    """Crea los enemigos.

    Args:
        DIMENSIONES_PANTALLA (tuple): La dimensión de la pantalla.
        numero_enemigos (int): El número de enemigos.
        tiempo_restante (int): El tiempo restante.
        diccionario_palabras (dict): El diccionario de palabras.
        palabras_seleccionadas (str): Las palabras que fueron seleccionadas.

    Returns:
        list: La lista de enemigos.
    """
    enemigos = []
    for i in range(numero_enemigos):
        palabra_info = obtener_palabra(tiempo_restante, diccionario_palabras, palabras_seleccionadas)
        if palabra_info == None:
            break 

        nuevo_x = random.randint(0, DIMENSIONES_PANTALLA[0] - 110)
        nuevo_y = random.randint(-110, -50)

        enemigos.append({
            "palabra": palabra_info["Palabra"],
            "x": nuevo_x,
            "y": nuevo_y,
            "puntaje": palabra_info["Puntaje"],
            "velocidad": 0.5
        })
        palabras_seleccionadas.append(palabra_info["Palabra"])
    return enemigos

def actualizar_posiciones_enemigos(enemigos: list, dimensiones_pantalla: tuple):
    """
    Actualiza la posición de los enemigos.
    Args:
        enemigos (list): La lista de enemigos
        dimensiones_pantalla (tuple): La dimension de la pantalla.
    """
    for enemigo in enemigos:
        enemigo["y"] += enemigo["velocidad"]
        if enemigo["y"] > dimensiones_pantalla[1]:
            enemigos.remove(enemigo)

def dibujar_enemigos(ventana: pygame.Surface, enemigos: list, fuente: str, color_texto: tuple):
    """
    Dibuja los enemigos en pantalla

    Args:
        ventana (pygame.Surface): Superficie donde se dibujarán los enemigos (la ventana principal del juego).
        enemigos (list): La lista de enemigos.
        fuente (str): La fuente que utilizarán los enemigos
        color_texto (tuple): El color de texto que tendrán los enemigos
    """
    fuente = pygame.font.Font(datos["path_fuente"], 25)
    for enemigo in enemigos:
        texto_palabra = fuente.render(enemigo["palabra"], True, color_texto)
        ventana.blit(texto_palabra, (enemigo["x"], enemigo["y"]))


def verificar_solapamiento(enemigo:dict, posiciones_ocupadas:tuple, distancia_minima: int=170):
    """Evita que las palabras se solapen (no mucho)

    Args:
        enemigo (dict): La lista de enmigos
        posiciones_ocupadas (tuple): Las posiciones que están ocupadadas
        distancia_minima (int, optional): La distancia minima. Por defecto es 160.

    Returns:
        bool: Retorna el solapamiento.
    """
    solapamiento = False 
    for x, y in posiciones_ocupadas:
        # Calcula la distancia entre las posiciones
        distancia = ((enemigo["x"] - x) ** 2 + (enemigo["y"] - y) ** 2) ** 0.5 # fórmula de la distancia euclidiana
        if distancia < distancia_minima:
            solapamiento = True
            break
    return solapamiento