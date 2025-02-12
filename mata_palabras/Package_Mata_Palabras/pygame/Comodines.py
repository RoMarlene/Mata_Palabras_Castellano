from Datos_juego import *
from Esenciales import mostrar_mensaje_con_fondo

def crear_comodin_tiempo(diccionario_juego, tiempo_inicio, diccionario_mensajes):
    """
    Aplica el efecto del comodín de tiempo extra al juego si está disponible.
    """
    if diccionario_juego["comodines_disponibles"] > 0 and diccionario_juego["comodin_tiempo_disponible"]:
        incremento_tiempo = diccionario_juego["tiempo_extra"]
        diccionario_juego = actualizar_comodin_tiempo(diccionario_juego, incremento_tiempo)
        diccionario_juego["comodin_tiempo_disponible"] = False  # Bloquea el comodín tras usarlo
    return diccionario_juego

def verificar_comodin(diccionario_juego, tipo_comodin, diccionario_mensajes):
    """
    Verifica el estado del comodín solicitado y devuelve el mensaje correspondiente.
    """
    estado = True
    
    if diccionario_juego["comodines_disponibles"] <= 0:
        estado = False
    elif diccionario_juego[tipo_comodin] == False:
        estado = False

    return estado

def actualizar_comodin_tiempo(diccionario_juego, incremento_tiempo):
    """
    Actualiza los datos del comodín de tiempo en el diccionario del juego.
    """
    diccionario_juego["duracion_total"] += incremento_tiempo
    diccionario_juego["comodines_disponibles"] -= 1
    
    if diccionario_juego["comodines_disponibles"] <= 0:
        diccionario_juego["comodin_tiempo_disponible"] = False  
    return diccionario_juego

def activar_comodin_tiempo(diccionario_juego, tiempo_inicio, diccionario_mensajes, fuente, pantalla, color_texto):
    """
    Activa el comodín de tiempo extra, validando su disponibilidad y actualizando el juego.
    """
    estado = verificar_comodin(diccionario_juego, "comodin_tiempo_disponible", diccionario_mensajes)
    
    if estado:
        print(f"DEBUG: diccionario_mensajes = {diccionario_mensajes}") 
        diccionario_juego = crear_comodin_tiempo(diccionario_juego, tiempo_inicio, diccionario_mensajes)
        diccionario_juego["mensaje_comodin"] = diccionario_mensajes["mensaje_tiempo_extra"]
        diccionario_juego["comodin_intentado"] = False  # Se resetea porque el comodín funcionó
    
    diccionario_juego["tiempo_inicio_mensaje_comodin"] = pygame.time.get_ticks()
    return diccionario_juego

def calcular_tiempo_restante(datos):
    """
    Calcula el tiempo restante basado en la duración total y el tiempo transcurrido.
    """
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = (tiempo_actual - datos["tiempo_inicio"]) / 1000
    tiempo_restante = datos["duracion_total"] - tiempo_transcurrido
    if tiempo_restante < 0:
        tiempo_restante = 0
    return tiempo_restante


def activar_comodin_vida(diccionario_juego, diccionario_mensajes, fuente, pantalla, color_texto):
    """
    Activa el comodín de vida extra si está disponible.
    """

    if diccionario_juego["comodines_disponibles"] > 0 and diccionario_juego["comodin_vida_extra"]:
        diccionario_juego["vida"] += 1  # ✅ Sumar una vida
        diccionario_juego["comodines_disponibles"] -= 1  
        diccionario_juego["comodin_vida_extra"] = False
        diccionario_juego["mensaje_comodin"] = diccionario_mensajes["mensaje_vida_agregada"]  # ✅ Mensaje correcto

    diccionario_juego["tiempo_inicio_mensaje_comodin"] = pygame.time.get_ticks()
    
    return diccionario_juego


def actualizar_mensaje_comodin(datos):
    """
    Elimina el mensaje del comodín después de 1 segundo, pero solo si no se ha actualizado recientemente.
    """
    if datos["mensaje_comodin"]:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - datos["tiempo_inicio_mensaje_comodin"]

        if tiempo_transcurrido > 1000:
            datos["mensaje_comodin"] = None

def mostrar_mensaje_comodin(pantalla, datos, fuente, diccionario_mensajes):
    """ Muestra el mensaje adecuado según el estado de los comodines """
    
    mensaje = datos["mensaje_comodin"]

    if mensaje:
        posicion_mensaje = posiciones["posicion_mensaje_comodin"]
        color_fondo = datos["BLANCO"]
        color_texto = datos["NEGRO"]

        mostrar_mensaje_con_fondo(pantalla, mensaje, posicion_mensaje, color_texto, color_fondo, fuente)










