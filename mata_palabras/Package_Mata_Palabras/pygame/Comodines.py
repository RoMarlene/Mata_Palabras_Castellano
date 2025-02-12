from Datos_juego import *
from Esenciales import mostrar_mensaje_con_fondo

def crear_comodin_tiempo(diccionario_juego:dict) -> dict:
    """Aplica el comodín de tiempo extra si está disponible.

    Args:
        diccionario_juego (dict): Diccionario con la información del juego.

    Returns:
        dict: Diccionario del juego actualizado tras aplicar el comodín de tiempo extra.
    """
    if diccionario_juego["comodines_disponibles"] > 0 and diccionario_juego["comodin_tiempo_disponible"]:
        incremento_tiempo = diccionario_juego["tiempo_extra"]
        diccionario_juego = actualizar_comodin_tiempo(diccionario_juego, incremento_tiempo)
        diccionario_juego["comodin_tiempo_disponible"] = False

    return diccionario_juego

def verificar_comodin(diccionario_juego: dict, tipo_comodin: str)-> bool:
    """Verifica si el comodin está disponible en el juego y 
    devuelve un booleano indicando su estado.

    Args:
        diccionario_juego (dict): El diccionario del juego
        tipo_comodin (str): Una clave específica dentro del diccionario que representa un tipo de comodín.

    Returns:
        bool: True si el comodín está disponible, False en caso contrario.
    """
    estado = True
    
    if diccionario_juego["comodines_disponibles"] <= 0:
        estado = False
    elif diccionario_juego[tipo_comodin] == False:
        estado = False

    return estado

def actualizar_comodin_tiempo(diccionario_juego: dict, incremento_tiempo: int)-> dict:
    """
    Actualiza los datos del comodín de tiempo en el diccionario del juego.

    Args:
        diccionario_juego (dict): Diccionario que contiene la información del juego.
        incremento_tiempo (int): Cantidad de tiempo (en segundos o minutos) que se debe sumar.

    Returns:
        dict: Diccionario actualizado con los cambios aplicados.
    """
    diccionario_juego["duracion_total"] += incremento_tiempo
    diccionario_juego["comodines_disponibles"] -= 1
    
    if diccionario_juego["comodines_disponibles"] <= 0:
        diccionario_juego["comodin_tiempo_disponible"] = False

    return diccionario_juego

def activar_comodin_tiempo(diccionario_juego: dict, diccionario_mensajes: dict)-> dict:
    """
    Activa el comodín de tiempo extra, validando su disponibilidad y actualizando el juego.

    Args:
        diccionario_juego (dict): Diccionario que contiene la información del juego.
        diccionario_mensajes (dict): Diccionario con los mensajes del juego.

    Returns:
        dict: Diccionario del juego actualizado."""
    estado = verificar_comodin(diccionario_juego, "comodin_tiempo_disponible")
    
    if estado:
        diccionario_juego = crear_comodin_tiempo(diccionario_juego)
        diccionario_juego["mensaje_comodin"] = diccionario_mensajes["mensaje_tiempo_extra"]
        diccionario_juego["comodin_intentado"] = False
    
    diccionario_juego["tiempo_inicio_mensaje_comodin"] = pygame.time.get_ticks()
    
    return diccionario_juego

def calcular_tiempo_restante(datos: dict)-> float:
    """
    Calcula el tiempo restante basado en la duración total y el tiempo transcurrido.

    Args:
        datos (dict): Diccionario con la información del tiempo en el juego.
        "tiempo_inicio" (int): Momento en que comenzó el tiempo (milisegundos).
        "duracion_total" (float): Tiempo total disponible (segundos).

    Returns:
        float: Tiempo restante en segundos. Si es negativo, devuelve 0.
    """
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = (tiempo_actual - datos["tiempo_inicio"]) / 1000
    tiempo_restante = datos["duracion_total"] - tiempo_transcurrido
    if tiempo_restante < 0:
        tiempo_restante = 0

    return tiempo_restante

def activar_comodin_vida(diccionario_juego: dict, diccionario_mensajes: dict)-> dict:
    """
    Activa el comodín de vida extra si está disponible.

    Args:
        diccionario_juego (dict): Diccionario con la información del juego.
        diccionario_mensajes (dict): Diccionario con los mensajes del juego.

    Returns:
        dict: Diccionario del juego actualizado.
    """

    if diccionario_juego["comodines_disponibles"] > 0 and diccionario_juego["comodin_vida_extra"]:
        diccionario_juego["vida"] += 1
        diccionario_juego["comodines_disponibles"] -= 1
        diccionario_juego["comodin_vida_extra"] = False
        diccionario_juego["mensaje_comodin"] = diccionario_mensajes["mensaje_vida_agregada"]

    diccionario_juego["tiempo_inicio_mensaje_comodin"] = pygame.time.get_ticks()
    
    return diccionario_juego

def actualizar_mensaje_comodin(datos: dict):
    """
    Elimina el mensaje del comodín después de 1 segundo si ha pasado suficiente tiempo.

    Args:
        datos (dict): Diccionario con la información del juego.
            - "mensaje_comodin" (str | None): Mensaje actual del comodín.
            - "tiempo_inicio_mensaje_comodin" (int): Momento en que se mostró el mensaje (milisegundos).
    """
    if datos["mensaje_comodin"]:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - datos["tiempo_inicio_mensaje_comodin"]

        if tiempo_transcurrido > 1000:
            datos["mensaje_comodin"] = None

def mostrar_mensaje_comodin(pantalla: object, datos: dict, fuente: str):
    """Muestra el mensaje adecuado según el estado de los comodines

    Args:
        pantalla (object): La ventana
        datos (dict): El diccionario de datos
        fuente (str): La fuente que se utiliza para el mensaje
    """
    
    mensaje = datos["mensaje_comodin"]

    if mensaje:
        posicion_mensaje = posiciones["posicion_mensaje_comodin"]
        color_fondo = datos["BLANCO"]
        color_texto = datos["NEGRO"]

        mostrar_mensaje_con_fondo(pantalla, mensaje, posicion_mensaje, color_texto, color_fondo, fuente)