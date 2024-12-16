import pygame
import csv
import time

# Función para manejar el cuadro de texto y la entrada del usuario
def manejar_cuadro_texto(eventos, texto_usuario: str, activo:bool, input_rect, palabras_actuales:str, vidas:int, puntaje:int, puntajes:int)->tuple:
    eliminar_palabra = False
    texto_procesado = texto_usuario  # Guarda el texto ingresado antes de modificarlo

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(evento.pos):
                activo = True
            else:
                activo = False

        if evento.type == pygame.KEYDOWN and activo:
            if evento.key == pygame.K_RETURN:
                texto_procesado = texto_usuario.lower().strip()
                palabra_encontrada = False

                for palabra in palabras_actuales:
                    if texto_procesado == palabra.lower().strip():
                        palabra_encontrada = True
                        break

                if palabra_encontrada:
                    eliminar_palabra = True
                    puntaje += puntajes.get(texto_procesado, 0)
                else:
                    vidas -= 1

                texto_usuario = ""  # Limpiar después de manejar el texto
            elif evento.key == pygame.K_BACKSPACE:
                texto_usuario = texto_usuario[:-1]
            else:
                texto_usuario += evento.unicode

    return texto_usuario, activo, eliminar_palabra, vidas, puntaje, texto_procesado


# Función para dibujar el cuadro de texto en la pantalla
def dibujar_cuadro_texto(pantalla, fuente, input_rect, texto_usuario, color_actual):
    pygame.draw.rect(pantalla, color_actual, input_rect, 2)
    texto_superficie = fuente.render(texto_usuario, True, (255, 255, 255))
    pantalla.blit(texto_superficie, (input_rect.x + 5, input_rect.y + 5))


# Función para mostrar un mensaje en la pantalla
def mostrar_mensaje(pantalla, mensaje, color, x, y, tamaño=40):
    fuente = pygame.font.Font(None, tamaño)
    texto = fuente.render(mensaje, True, color)
    pantalla.blit(texto, (x, y))


# Función para mostrar un mensaje temporal en la pantalla por un tiempo determinado
def mostrar_mensaje_temporal(pantalla, mensaje, color, x, y, tiempo=3, tamaño=40):
    tiempo_inicial = pygame.time.get_ticks()  # Obtener el tiempo de inicio
    while pygame.time.get_ticks() - tiempo_inicial < tiempo * 1000:  # Convertir a milisegundos
        pantalla.fill((0, 0, 0), (0, 0, pantalla.get_width(), pantalla.get_height()))  # Limpiar la pantalla si es necesario
        mostrar_mensaje(pantalla, mensaje, color, x, y, tamaño)  # Mostrar el mensaje
        pygame.display.update()
        pygame.time.Clock().tick(60)  # Limitar a 60 FPS para un refresco constante


# Función para actualizar la posición de las palabras
def actualizar_posiciones(lista_palabras: list):
    """
    Actualiza las posiciones de las palabras en la pantalla.
    """
    for palabra in lista_palabras:
        palabra["y"] += palabra["velocidad"]



# Función para dibujar las palabras en la pantalla
def dibujar_palabras(pantalla, lista_palabras):
    """
    Dibuja las palabras en la pantalla.
    """
    for palabra in lista_palabras:
        mostrar_mensaje(pantalla, palabra["palabra"], (255, 255, 255), palabra["pos_x"], palabra["pos_y"])
