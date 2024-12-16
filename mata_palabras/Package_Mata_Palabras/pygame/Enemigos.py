import pygame
import random
from Datos_juego import datos
from Esenciales import *

#Crea los enemigos.
#Recibe la dimension de pantalla, el numero de enemigos, el tiempo restante, el diccionario de palabras y las palabras seleccionadas
#Retorna una lista de enemigos
def crear_enemigos(DIMENSIONES_PANTALLA: tuple, numero_enemigos: int, tiempo_restante:int, diccionario_palabras:dict, palabras_seleccionadas: str)-> list:
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

#Acá actualiza la posicion de los enemigos
#recibe la lista de enemigos y las dimensiones de pantalla
def actualizar_posiciones_enemigos(enemigos: list, dimensiones_pantalla: tuple):
    for enemigo in enemigos:
        enemigo["y"] += enemigo["velocidad"]
        if enemigo["y"] > dimensiones_pantalla[1]:
            enemigos.remove(enemigo)

#Dibuja los enemigos en pantalla 
def dibujar_enemigos(ventana:int, enemigos: list, fuente: str, color_texto: tuple):
    fuente = pygame.font.Font(datos["path_fuente"], 25)
    for enemigo in enemigos:
        texto_palabra = fuente.render(enemigo["palabra"], True, color_texto)
        ventana.blit(texto_palabra, (enemigo["x"], enemigo["y"]))


#Aca verifica si la palabra se solapa con la otra
#Recibe el enemigo, las posiciones ocupadas y la distancia minima.
def verificar_solapamiento(enemigo:dict, posiciones_ocupadas:tuple, distancia_minima: int=160):
    solapamiento = False 
    for x, y in posiciones_ocupadas:
        # Calcula la distancia entre las posiciones
        distancia = ((enemigo["x"] - x) ** 2 + (enemigo["y"] - y) ** 2) ** 0.5 # fórmula de la distancia euclidiana:
        
        if distancia < distancia_minima:
            solapamiento = True
            break
    return solapamiento