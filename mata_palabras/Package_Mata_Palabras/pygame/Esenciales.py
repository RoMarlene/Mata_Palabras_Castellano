import pygame
import random
from Modulo_central import datos

# Inicialización del tiempo al inicio del juego
def iniciar_temporizador():
    if datos["tiempo_inicio"] == None:
        datos["tiempo_inicio"] = pygame.time.get_ticks()

#Crea el temporizador
#Recibe la duracion total y el tiempo de inicio.
#Devuelve el tiempo restante.
def crear_temporizador(duracion_total: int, tiempo_inicio: int)-> int:
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = (tiempo_actual - tiempo_inicio) // 1000
    tiempo_restante = duracion_total - tiempo_transcurrido
    
    if tiempo_restante < 0:
        tiempo_restante = 0

    return tiempo_restante

#Esta funcion resta las vidas.
#Recibe la vida 
#Retorna la nueva vida, o sea, la vida actualizada
def restar_vidas(vidas: int) -> int:
    nueva_vida = vidas - 1
    return nueva_vida

#Verifica si colisiona con la linea
#Recibe la lista de diccionarios de enemigos y la linea en la coordenada y
#Devuelve un booleano
def verificar_colision_con_linea(enemigos: list, linea_y: int)->bool:
    colision_detectada = False 

    for enemigo in enemigos:
        if enemigo["y"] >= linea_y:
            colision_detectada = True
    
    return colision_detectada  

#Muestra el temporizador
def mostrar_temporizador(pantalla, tiempo_restante: int, posicion: int, color: tuple, tamaño_fuente:int):
    fuente = pygame.font.Font(datos["path_fuente"], tamaño_fuente)  # Usa la fuente por defecto
    texto_tiempo = fuente.render(f"{tiempo_restante}s", True, color)
    pantalla.blit(texto_tiempo, posicion)

#Muestra las vidas
def mostrar_vidas(pantalla, vidas: int, posicion: int, color: tuple, tamaño_fuente: int):
    fuente = pygame.font.Font(datos["path_fuente"], tamaño_fuente)  # Usa la fuente por defecto
    vidas_texto = fuente.render(str(vidas), True, color)
    pantalla.blit(vidas_texto, posicion)

#calcula el puntaje.
#Recibe el diccionario, el puntaje y la palabra
#Retorna el puntaje actualizado
def calcular_puntaje(diccionario: dict, puntaje: int, palabra: str) -> int:
    puntaje_actualizado = puntaje
    for clave in diccionario:
        lista_palabras = diccionario[clave]["Palabras"]
        for palabra_lista in lista_palabras:
            if palabra == palabra_lista:  
                puntaje_actualizado += diccionario[clave]["Puntaje"]  
                break  
    return puntaje_actualizado

#muestra el puntaje
def mostrar_puntaje(pantalla, puntaje: int, posicion: int, color: tuple, tamaño_fuente: int):
    fuente = pygame.font.Font(datos["path_fuente"], tamaño_fuente) 
    puntaje_texto = fuente.render(str(puntaje), True, color)
    pantalla.blit(puntaje_texto, posicion)

#Muestra un mensaje con fondo transparente
#Recibe la pantalla, el mensaje, la posicion, el color del fondo, el color del texto y la fuente
def mostrar_mensaje_con_fondo(pantalla, mensaje: str, posicion: tuple, color_fondo: tuple, color_texto: tuple, fuente: str):
    texto = fuente.render(mensaje, True, color_texto)

    # Crear el fondo transparente con un margen
    margen = 10
    fondo = pygame.Surface((texto.get_width() + margen * 2, texto.get_height() + margen * 2), pygame.SRCALPHA) #canal alfa, transparencia
    fondo.fill((*color_fondo, 70))

    pantalla.blit(fondo, posicion)

    # Colocar el texto centrado dentro del fondo
    rect_texto = texto.get_rect(center=(posicion[0] + fondo.get_width() // 2, posicion[1] + fondo.get_height() // 2))
    pantalla.blit(texto, rect_texto)

#Esta función obtiene la palabra del diccionario.
#Recibe el diccionario y la palabra seleccionada
#Retorna un diccionario
def obtener_palabra(tiempo_restante: int, diccionario_palabras: dict, palabras_seleccionadas: list)-> dict:
    if tiempo_restante > 45: 
        categoria = "Faciles"
    elif tiempo_restante > 30:  
        categoria = "Medias"
    else:
        categoria = "Dificiles" 

    palabras_no_seleccionadas = []

    palabras_disponibles = diccionario_palabras[categoria]["Palabras"]

    for palabra in palabras_disponibles:  
        ya_seleccionada = False 
        for seleccionada in palabras_seleccionadas:  
            if palabra == seleccionada:  
                ya_seleccionada = True  
                break 

        if ya_seleccionada == False:  
            palabras_no_seleccionadas.append(palabra)  

    resultado = None
    palabra = random.choice(diccionario_palabras[categoria]["Palabras"])

    if len(palabras_no_seleccionadas) > 0:  
        palabra_seleccionada = random.choice(palabras_no_seleccionadas)  
        
        resultado = {  
            "Categoria": categoria,  
            "Palabra": palabra_seleccionada,  
            "Puntaje": diccionario_palabras[categoria]["Puntaje"]  
        }  

    return resultado
