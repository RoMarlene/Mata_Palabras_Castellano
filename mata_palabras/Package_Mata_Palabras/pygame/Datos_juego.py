import pygame
from Archivos import *

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
    "AZUL": (0, 0, 121),
    "Rectangulo_texto_final": pygame.Rect(200, 300, 400, 50),
    "rectangulo_texto_juego": pygame.Rect(50, 500, 200, 50),
    "color_inactivo": pygame.Color('lightskyblue3'),
    "color_activo" : pygame.Color('dodgerblue2'),
    "tamaño_icono_volumen": (50, 50),
    "volumen_predefinido": 0.5,
    "tamaño_boton_empezar": (245, 85),
    "tamaño_boton_puntuacion": (245, 85),
    "tamaño_boton_volver": (160, 56),
    "longitud_minima": 5,
    "comodines_disponibles": 3,  # Total de comodines disponibles
    "comodin_tiempo_disponible": True,  # Estado del comodín de tiempo
    "tiempo_extra": 10,
    "mensaje_comodin": None,  # Inicialmente, no hay mensaje
    "tiempo_inicio_mensaje_comodin": 0  # Guardará el tiempo en que se activó
}

posiciones = {
    "posicion_temporizador": (50, 20),
    "posicion_vida": (50, 50),
    "posicion_puntaje": (48, 75),
    "posicion_mensaje_final": (250, 450),
    "posicion_mensaje_inicio": (183, 531),
    "posicion_boton_empezar": (275, 271),
    "posicion_boton_puntuacion": (273,456),
    "posicion_boton_volver": (624, 68)
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
    "sin_comodines": "¡Ya no hay comodines disponibles!",
    "mensaje_final": "¡Nombre guardado!",
    "mensaje_inicio": "Presiona ENTER para empezar el juego",
    "mensaje_tiempo_extra": "¡Comodín usado! Tiempo extra añadido"
    
}

TECLAS_JUEGO = {
    "iniciar_juego": pygame.K_RETURN,
    "volumen_arriba": pygame.K_UP,
    "volumen_abajo": pygame.K_DOWN,
    "enviar": pygame.K_RETURN,
    "borrar": pygame.K_BACKSPACE,
    "comodin_tiempo": pygame.K_1,
    "comodin_vida": pygame.K_2,
    "comodin_congelacion": pygame.K_3,
}


# Inicialización de pygame y recursos
pygame.mixer.init()
boton_sonido = pygame.mixer.Sound(sonidos["botones"])

# Dimensiones globales
DIMENSIONES_PANTALLA = (datos["ANCHO"], datos["ALTO"])


