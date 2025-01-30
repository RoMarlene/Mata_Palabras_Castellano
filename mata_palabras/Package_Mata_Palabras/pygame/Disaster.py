import random
import json
import pygame

#Esta función crea una matriz para las posiciones en pantalla, crea la matriz con el tamaño de la pantalla
#las "celdas" de la matriz representan posibles posiciones para las palabras.
#recibe el ancho de la pantalla, el alto de la pantalla, el ancho de la celda y el alto de la celda
#Devuelve la matriz.
def crear_matriz_posiciones(ancho_pantalla: int, alto_pantalla: int, ancho_celda:int, alto_celda:int) ->list:
    matriz = []
    filas = alto_pantalla // alto_celda  # Cantidad de filas en la pantalla
    columnas = ancho_pantalla // ancho_celda  # Cantidad de columnas en la pantalla
    
    for fila in range(filas):
        matriz.append([0] * columnas)  # Inicializa todas las posiciones como "libres" (0)
    
    return matriz

#Esta funcion se asegura de ingresar las palabras dentro de las posiciones sin que sibresalga del borde.
#Recibe la palabra, la matriz, el ancho de la celda, el alto de la celda, el ancho de la pantalla y la fuente
#Retorna la posicion
def colocar_palabra_en_matriz(palabra:int, matriz:list, ancho_celda:int, alto_celda:int, ancho_pantalla:int, fuente:str)->tuple|int:
    filas = len(matriz)
    columnas = len(matriz[0])
    ancho_palabra, _ = fuente.size(palabra)  # Calcula el ancho real de la palabra, se ignora la altura
    celdas_ocupadas = (ancho_palabra // ancho_celda) + 1  # Celdas necesarias
    posicion = None

    # Generar posiciones válidas
    posiciones = [
        (fila, columna)
        for fila in range(filas)
        for columna in range(columnas - celdas_ocupadas + 1) #Se asegura de que no sobresalga el borde derecho
    ]

    random.shuffle(posiciones)

    for fila, columna in posiciones:
        x = columna * ancho_celda
        y = fila * alto_celda

        # Verificar si la palabra enta la pantalla
        if x + ancho_palabra <= ancho_pantalla:
            for i in range(celdas_ocupadas):
                matriz[fila][columna + i] = 1
            posicion = (x, y)
            break

    return posicion


"""_summary_
Ordena los puntajes de mayor a menor ajustando los puntajes poniendo 0 al principio.
Args:
    data (int): La puntuaciónn.
    longitud_minima (int): longitud máxima.
"""
def ordenar_estadistica(data:int, longitud_minima:int):
    if data:
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                if int(data[i]['Puntaje']) < int(data[j]['Puntaje']):
                    # Intercambia elementos si están en el orden incorrecto
                    data[i], data[j] = data[j], data[i]

        for jugador in data:
            jugador['Puntaje'] = str(jugador['Puntaje']).zfill(longitud_minima)  

        # Guardamos las puntuaciones ordenadas de vuelta en el archivo
        with open("Estadisticas.json", 'w') as archivo:
            json.dump(data, archivo, indent=4)

#Funcion que congela el tiempo en un periddo especifico
#recibe el tiempo_restante, el tiempo congelado y el inicio de congelamiento
def congelar_tiempo(tiempo_restante: int, tiempo_congelado:int, inicio_congelamiento:int) ->list:
    tiempo_actual = pygame.time.get_ticks()  
    tiempo_transcurrido = (tiempo_actual - inicio_congelamiento) / 1000

    if tiempo_transcurrido < tiempo_congelado:  # Si no terminó
        pygame.time.wait(50)  # evita recursion infinita
        return congelar_tiempo(tiempo_restante, tiempo_congelado, inicio_congelamiento)
    else:
        tiempo_restante -= tiempo_congelado  #Actualizamos el tiempo restante 
        if tiempo_restante < 0:  # Aseguramos que no sea negativo
            tiempo_restante = 0
        return tiempo_restante 