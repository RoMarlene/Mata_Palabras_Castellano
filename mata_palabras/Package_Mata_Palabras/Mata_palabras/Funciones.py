import time
import random
from Comodines import *
from archivos import *

#Esta función resta las vidas.
#Recibe las vidas
#Retorna una tupla de mensaje y vidas.
def restar_vidas(vidas: int)-> str|int:
    vidas -= 1
    if vidas > 0:
        mensaje = f"¡Vida perdida! Te quedan: {vidas} vidas."
    else:
        mensaje = f"¡Perdiste alpiste! Te quedaste sin vidas, termina el juego."

    return mensaje, vidas

#Esta funcion ingresa y valida la polabra puesta por el usuario.
#Recibe como parámetro el diccionario y el mensaje
#Retorna un booleano, "False" si la palabra es incorrecta, "True" si no.
def ingresar_y_validar_palabra(diccionario: dict, mensaje: str) -> bool:
    palabra = mensaje.lower()  # Usamos el mensaje que es la palabra ingresada por el usuario
    es_palabra = False
    for clave in diccionario:
        for item in diccionario[clave]["Palabras"]:
            # Comparamos la palabra con cada elemento en la lista de palabras
            if palabra == item:
                es_palabra = True
                break  # Salimos del ciclo ya que no hace falta seguir buscando
        if es_palabra:
            break  # Salimos del ciclo externo si encontramos la palabra
    return es_palabra


#Esta función calcula el porcentaje.
#Recibe el diccionario, el puntaje inicial (0) y la palabra
#Retorna el puntaje
def calcular_puntaje(diccionario: dict, puntaje: int, palabra: str)-> int:
    # Recorre cada categoría en el diccionario
    for clave in diccionario:
        lista_palabras = diccionario[clave]["Palabras"]
        # Recorre la lista de palabras de la categoría
        for palabra_en_lista in lista_palabras:
            if palabra == palabra_en_lista:
                puntaje += diccionario[clave]["Puntaje"]  # Sumar el puntaje de la palabra
                return puntaje  # Sale de la función una vez que encuentra la palabra
    return puntaje

#Esta función obtiene la palabra del diccionario.
#Recibe el diccionario y el tiempo restante
#Retorna un diccionario con la palabra, categoria y puntaje
def obtener_palabra(tiempo_restante: int, diccionario_palabras: dict)-> dict:
    if tiempo_restante > 45: 
        categoria = "Faciles"
    elif tiempo_restante > 30:  
        categoria = "Medias"
    else:
        categoria = "Dificiles" 

    # Selecciona una palabra aleatoria de la categoría seleccionada
    palabra = random.choice(diccionario_palabras[categoria]["Palabras"])
    return {
        "Categoria": categoria,
        "Palabra": palabra,
        "Puntaje": diccionario_palabras[categoria]["Puntaje"]
    }
