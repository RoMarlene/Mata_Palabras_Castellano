from Datos_juego import *
from Esenciales import mostrar_mensaje_con_fondo

def crear_comodin_tiempo(diccionario_juego, tiempo_inicio, diccionario_mensajes):
    """
    Aplica el efecto del comodín de tiempo extra al juego.
    """
    incremento_tiempo = diccionario_juego["tiempo_extra"]  # Usamos el valor de tiempo_extra
    diccionario_juego = actualizar_comodin_tiempo(diccionario_juego, incremento_tiempo)

    # Guardar mensaje en datos
    diccionario_juego["mensaje_comodin"] = diccionario_mensajes["mensaje_tiempo_extra"]
    diccionario_juego["tiempo_inicio_mensaje_comodin"] = pygame.time.get_ticks()  # Guardamos el tiempo de inicio

    return diccionario_juego

def verificar_comodin(diccionario_juego, tipo_comodin, diccionario_mensajes):
    """
    Verifica el estado del comodín solicitado y devuelve el mensaje correspondiente.

    Parámetros:
    - diccionario_juego: dict, contiene los datos del juego.
    - tipo_comodin: str, el tipo de comodín a verificar (ej. "comodin_tiempo_disponible").
    - diccionario_mensajes: dict, contiene los mensajes del juego.

    Retorno:
    - mensaje: str, mensaje que describe el estado del comodín.
    - estado: bool, True si el comodín puede usarse, False si no.
    """
    mensaje = None
    estado = True

    if diccionario_juego["comodines_disponibles"] <= 0:
        mensaje = diccionario_mensajes["sin_comodines"]
        estado = False
    elif diccionario_juego[tipo_comodin] == False:
        mensaje = diccionario_mensajes["comodines_usados"]
        estado = False

    return mensaje, estado

def actualizar_comodin_tiempo(diccionario_juego, incremento_tiempo):
    """
    Actualiza los datos del comodín de tiempo en el diccionario del juego.
    """
    diccionario_juego["duracion_total"] += incremento_tiempo
    print(f"Tiempo total actualizado: {diccionario_juego['duracion_total']}")
    diccionario_juego["comodines_disponibles"] -= 1
    diccionario_juego["comodin_tiempo_disponible"] = False
    return diccionario_juego

def activar_comodin_tiempo(diccionario_juego, tiempo_inicio, diccionario_mensajes, fuente, pantalla, color_texto):
    """
    Activa el comodín de tiempo extra, validando su disponibilidad y actualizando el juego.
    """
    mensaje, estado = verificar_comodin(diccionario_juego, "comodin_tiempo_disponible", diccionario_mensajes)

    if estado:
        diccionario_juego = crear_comodin_tiempo(diccionario_juego, tiempo_inicio, diccionario_mensajes)
    else:
        mostrar_mensaje_con_fondo(pantalla, mensaje, (240, 250), (0, 0, 0), color_texto, fuente)
        datos["mensaje_comodin"] = mensajes["mensaje_tiempo_extra"]
        datos["tiempo_inicio_mensaje_comodin"] = pygame.time.get_ticks()

    return diccionario_juego

def calcular_tiempo_restante(datos):
    """
    Calcula el tiempo restante basado en la duración total y el tiempo transcurrido.
    """
    tiempo_transcurrido = (pygame.time.get_ticks() - datos["tiempo_inicio"]) / 1000
    tiempo_restante = datos["duracion_total"] - tiempo_transcurrido
    if tiempo_restante < 0:
        tiempo_restante = 0  # Evitar tiempos negativos sin usar max
    return tiempo_restante

def actualizar_mensaje_comodin(datos):
    """ Elimina el mensaje del comodín después de 1 segundo """
    if datos["mensaje_comodin"]:  # Si hay un mensaje activo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - datos["tiempo_inicio_mensaje_comodin"] > 1000:  # 1 segundo
            datos["mensaje_comodin"] = None

def mostrar_mensaje_comodin(pantalla, datos, posiciones, fuente):
    """ Muestra el mensaje del comodín si está activo """
    if datos["mensaje_comodin"]:
        mostrar_mensaje_con_fondo(pantalla, datos["mensaje_comodin"], (240, 250), datos["NEGRO"], datos["BLANCO"], fuente)