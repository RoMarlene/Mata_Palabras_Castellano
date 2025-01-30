import pygame
from Datos_juego import imagenes, sonidos, DIMENSIONES_PANTALLA, mensajes, posiciones, datos
from Funciones import manejar_eventos_generales, inicializar_pantalla

def crear_inicio_juego():
    ventana, imagen_inicio, fuente_inicio, color_fuente = inicializar_pantalla(
        titulo="Inicio",
        icono=imagenes["Icono"],
        fondo=imagenes["Fondo_inicio"],
        fuente_config=("Arial", 30),
        color_fuente=datos["BLANCO"],
        musica=sonidos["sonido_inicio"],
        volumen=datos["volumen_predefinido"]
    )

    texto_inicio = fuente_inicio.render(mensajes["mensaje_inicio"], True, color_fuente)

    bandera_inicio = True
    siguiente_pantalla = "inicio"

    while bandera_inicio:
        ventana.blit(imagen_inicio, (0, 0))
        ventana.blit(texto_inicio, posiciones["posicion_mensaje_inicio"])

        eventos = pygame.event.get()
        bandera_inicio, siguiente_pantalla, _, _ = manejar_eventos_generales(eventos, contexto="inicio")

        if siguiente_pantalla == "juego":
            pygame.mixer.music.stop()  # Detiene la música al salir

        pygame.display.update()

    return siguiente_pantalla