import pygame
from Datos_juego import TECLAS_JUEGO

# Función para manejar el cuadro de texto y la entrada del usuario
def manejar_cuadro_texto(eventos, texto_usuario: str, activo: bool, input_rect, palabras_actuales: list, vidas: int, puntaje: int, puntajes: dict, max_longitud_texto: int = 20) -> tuple:
    eliminar_palabra = False
    texto_procesado = ""  # Texto ingresado final para comparación

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            activo = input_rect.collidepoint(evento.pos)

        if evento.type == pygame.KEYDOWN and activo:
            if evento.key == TECLAS_JUEGO["enviar"]:
                puntaje, vidas, eliminar_palabra = validar_palabra(texto_usuario, palabras_actuales, puntajes, vidas, puntaje)
                texto_procesado = texto_usuario.lower().strip()
                texto_usuario = ""  # Limpiar el campo tras validar

            elif evento.key == TECLAS_JUEGO["borrar"]:
                texto_usuario = texto_usuario[:-1]

            elif len(texto_usuario) < max_longitud_texto:
                texto_usuario += evento.unicode

    return texto_usuario, activo, eliminar_palabra, vidas, puntaje, texto_procesado

def manejar_cuadro_texto_final(eventos, texto_usuario: str, activo: bool, input_rect, max_longitud_texto: int = 20) -> tuple:
    """
    Maneja un cuadro de texto simple utilizando un diccionario de teclas.
    - Permite escribir texto dentro de un rectángulo activo.
    - Al presionar la tecla de enviar, devuelve el texto procesado.
    """
    texto_procesado = ""  # Texto final para guardar

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Activa el cuadro si el clic está dentro del rectángulo
            activo = input_rect.collidepoint(evento.pos)

        if evento.type == pygame.KEYDOWN and activo:
            if evento.key == TECLAS_JUEGO["enviar"]:  # Enter
                texto_procesado = texto_usuario.strip()
                texto_usuario = ""  # Limpia el campo después de guardar
            elif evento.key == TECLAS_JUEGO["borrar"]:  # Backspace
                texto_usuario = texto_usuario[:-1]
            else:
                # Agrega texto si no supera el límite
                if len(texto_usuario) < max_longitud_texto:
                    texto_usuario += evento.unicode

    return texto_usuario, activo, texto_procesado

def validar_palabra(texto_usuario: str, palabras_actuales: list, puntajes: dict, vidas: int, puntaje: int) -> tuple:
    texto_procesado = texto_usuario.lower().strip()
    palabra_encontrada = False

    # Iterar sobre las palabras actuales y verificar si coinciden
    for palabra in palabras_actuales:
        if texto_procesado == palabra.lower().strip():
            palabra_encontrada = True
            break

    if palabra_encontrada:
        eliminar_palabra = True
        puntaje += puntajes.get(texto_procesado, 0)
    else:
        eliminar_palabra = False
        vidas -= 1

    return puntaje, vidas, eliminar_palabra

# Función para actualizar la posición de las palabras
def actualizar_posiciones(lista_palabras: list):
    """
    Actualiza las posiciones de las palabras en la pantalla.
    """
    for palabra in lista_palabras:
        palabra["y"] += palabra["velocidad"]
