import pygame
import random
from Datos_juego import datos

"""
Inicialización del tiempo al inicio del juego
"""
def iniciar_temporizador():
    if datos["tiempo_inicio"] == None:
        datos["tiempo_inicio"] = pygame.time.get_ticks()


"""
Crea el temporizador.
Args:
    duracion_total (int): El tiempo total que dura el tiempo.
    tiempo_inicio (int): El tiempo de inicio.

Returns:
    int: El tiempo restante.
"""
def crear_temporizador(duracion_total, tiempo_inicio, datos):
    tiempo_actual = pygame.time.get_ticks()

    if datos["tiempo_congelado"]:  
        tiempo_restante = datos["tiempo_restante_congelacion"]  # Mantiene el tiempo congelado
    else:
        tiempo_restante = duracion_total - (tiempo_actual - tiempo_inicio) // 1000  # Calcula tiempo normal

    if tiempo_restante < 0:
        tiempo_restante = 0

    return tiempo_restante

"""
Esta funcion resta las vidas.
Args:
    vidas (int):L vida

Returns:
    int: Retorna la nueva vida, o sea, la vida actualizada
"""
def restar_vidas(vidas: int) -> int:
    nueva_vida = vidas - 1
    return nueva_vida

"""
    verifica si el "objeto" colisiona con la linea

Args:
    enemigos (list): La lista de enemigos
    linea_y (int): Linea en posicion Y.

Returns:
    bool: La colisión detectada.
"""
def verificar_colision_con_linea(enemigos: list, linea_y: int)->bool:
    colision_detectada = False 

    for enemigo in enemigos:
        if enemigo["y"] >= linea_y:
            colision_detectada = True
    
    return colision_detectada  


def mostrar_texto(pantalla, texto: str, posicion: tuple, color: tuple, tamaño_fuente: int):
    """
    Muestra texto genérico en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibujará el texto.
        texto (str): Texto a mostrar.
        posicion (tuple): Posición (x, y) donde se ubicará el texto.
        color (tuple): Color del texto en formato RGB.
        tamaño_fuente (int): Tamaño de la fuente.
    """
    texto = str(texto)
    fuente = pygame.font.Font(datos["path_fuente"], tamaño_fuente)  # Usa la fuente configurada
    texto_renderizado = fuente.render(texto, True, color)
    pantalla.blit(texto_renderizado, posicion)

"""
Calcula el puntaje.

Args:
    diccionario (dict): El diccionario del csv.
    puntaje (int): El puntaje.
    palabra (str): La palabra.

Returns:
    int: El puntaje actualizado.
"""
def calcular_puntaje(diccionario: dict, puntaje: int, palabra: str) -> int:
    puntaje_actualizado = puntaje
    for clave in diccionario:
        lista_palabras = diccionario[clave]["Palabras"]
        for palabra_lista in lista_palabras:
            if palabra == palabra_lista:  
                puntaje_actualizado += diccionario[clave]["Puntaje"] * datos["multiplicador_puntos"]  # Aplicamos el multiplicador  
                break  
    return puntaje_actualizado


def mostrar_mensaje_con_fondo(pantalla, mensaje: str, posicion: tuple, color_fondo: tuple, color_texto: tuple, fuente):
    """
    Dibuja un mensaje con un fondo semitransparente en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará el mensaje.
        mensaje (str): El texto que se mostrará en pantalla.
        posicion (tuple): Coordenadas (x, y) de la esquina superior izquierda del fondo.
        color_fondo (tuple): Color del fondo en formato RGB.
        color_texto (tuple): Color del texto en formato RGB.
        fuente (pygame.font.Font): Fuente utilizada para renderizar el texto.
    """
    # Renderiza el texto
    texto = fuente.render(mensaje, True, color_texto)

    if color_fondo:  # Si hay un color de fondo especificado
        margen = 10
        fondo = pygame.Surface((texto.get_width() + margen * 2, texto.get_height() + margen * 2), pygame.SRCALPHA)
        fondo.fill((*color_fondo, 70))  # Fondo semitransparente
        pantalla.blit(fondo, posicion)

        # Centrar el texto dentro del fondo
        rect_texto = texto.get_rect(center=(posicion[0] + fondo.get_width() // 2, posicion[1] + fondo.get_height() // 2))
    else:
        # Posición directa del texto sin fondo
        rect_texto = texto.get_rect(topleft=posicion)

    pantalla.blit(texto, rect_texto)

"""
Selecciona una palabra del diccionario según la categoría basada en el tiempo restante.

Dependiendo del tiempo restante, selecciona una palabra de la categoría correspondiente:
- "Faciles" si el tiempo es mayor a 45 segundos.
- "Medias" si el tiempo es mayor a 30 segundos pero menor o igual a 45 segundos.
- "Dificiles" si el tiempo es menor o igual a 30 segundos.

Además, evita palabras previamente seleccionadas para evitar repeticiones.

Args:
    tiempo_restante (int): Tiempo restante en el juego.
    diccionario_palabras (dict): Diccionario que contiene palabras categorizadas y sus puntajes.
    palabras_seleccionadas (list): Lista de palabras que ya se seleccionaron previamente.

Returns:
    dict: Contiene la categoría de la palabra, la palabra seleccionada, y su puntaje asociado.
"""
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
