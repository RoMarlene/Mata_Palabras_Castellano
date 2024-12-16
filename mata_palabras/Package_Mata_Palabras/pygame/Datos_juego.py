import pygame
from archivos import *

palabras_csv = "Palabras.csv"
diccionario_palabras = obtener_lista_palabras(palabras_csv)

# Configuración de datos
datos = {
    "ANCHO": 800,
    "ALTO": 600,
    "path_fuente": "Fuente\\SpaceOutOpen.ttf",
    "BLANCO": (255, 255, 255),
    "NEGRO": (0, 0, 0),
    "GRIS": (128, 128, 128),
    "duracion_total": 60,
    "tiempo_inicio": None,
    "color_temporizador": (255, 255, 255),
    "tamaño_fuente": 30,
    "tamaño_fuente_temporizador": 26,
    "maximo_enemigos": 3,
    "vida": 3,
    "posicion_vida": (50, 50),
    "posicion_puntaje": (48, 75),
    "AZUL": "(0, 0, 121)"
}

posiciones = {
    "posicion_temporizador": (50, 20)
}

imagenes = {
    "Juego": "Imagenes\\Juego.png",
    "Icono": "Imagenes\\Icono.png",
    "Menu": "Imagenes\\Menu_principal.png",
    "Empezar": "Imagenes\\Empezar.jpg",
    "Puntuacion": "Imagenes\\Puntuacion.jpg",
    "Volver": "Imagenes\\Volver.jpg",
    "Fondo_Puntuacion": "Imagenes\\Puntuacion.png",
    "Fondo_inicio": "Imagenes\\Inicio.png",
    "Icono_volumen": "Imagenes\\Volumen.png",
    "Temporizador": "Imagenes\\Temporizador.png",
    "Vidas": "Imagenes\\Vidas.png",
    "Puntaje": "Imagenes\\Puntuacion_icono.png",
    "Final": "Imagenes\\Final.png"
}

sonidos = {
    "cancion_menu": "sonidos\\Cancion_Menu_principal.mp3",
    "cancion_puntuacion": "sonidos\\Cancion_Puntuacion.mp3",
    "botones": "sonidos\\Sonido_Boton.wav",
    "sonido_inicio": "sonidos\\Cancion_inicio.wav",
    "sonido_juego": "sonidos\\cancion_juego.mp3",
    "sonido_final": "sonidos\\cancion_final.wav"
}

mensajes = {
    "tiempo_agotado": "¡Se acabó el tiempo! :(",
    "vidas_agotadas": "¡Se acabaron las vidas! Perdiste.",
    "congelacion": "¡Corre, corre! ¡El tiempo ha vuelto a correr!",
    "comodines_usados": "Este comodín ya no está disponible.",
    "Comodines_en_uso": "Comodín en uso"
    # Agrega más mensajes aquí según sea necesario
}
# Inicialización de pygame y recursos
pygame.mixer.init()
boton_sonido = pygame.mixer.Sound(sonidos["botones"])

# Dimensiones globales
DIMENSIONES_PANTALLA = (datos["ANCHO"], datos["ALTO"])
