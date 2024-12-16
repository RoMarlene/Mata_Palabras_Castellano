import pygame
import json
from Modulo_central import crear_boton, dibujar, datos, DIMENSIONES_PANTALLA, imagenes, sonidos,ajustar_volumen, mostrar_icono_volumen
from Disaster import *

# Función para cargar las puntuaciones desde el archivo JSON
def cargar_puntuaciones():
    with open("Estadisticas.json", 'r') as archivo:
        data = json.load(archivo)
    return data

# Función para mostrar las puntuaciones en la pantalla
def mostrar_puntuaciones(puntuaciones, ventana_puntuacion):
    fuente_personalizada = pygame.font.Font(datos["path_fuente"], 30)
    desplazamiento_y = 150 
    desplazamiento_x = 200

    for jugador in puntuaciones:
        texto = f"{jugador['Nombre']}: {jugador['Puntaje']}"
        superficie_texto = fuente_personalizada.render(texto, True, datos["BLANCO"])
        ventana_puntuacion.blit(superficie_texto, (desplazamiento_x, desplazamiento_y))
        desplazamiento_y += 40 

def ventana_puntuacion():
    pygame.init()
    pygame.mixer.init()

    ventana_puntuacion = pygame.display.set_mode(DIMENSIONES_PANTALLA)
    pygame.display.set_caption("Puntuación")

    imagen_fondo_juego = pygame.image.load(imagenes["Fondo_Puntuacion"])

    pygame.mixer.music.load(sonidos["cancion_puntuacion"])  # Cargar la canción
    pygame.mixer.music.play(loops=-1)

    longitud_minima = 5
    boton_volver = crear_boton(
        ventana=ventana_puntuacion,
        posicion=(624, 68),
        dimensiones_boton=[160 , 56],
        path_imagen= imagenes["Puntuacion"]
    )


    puntuaciones = cargar_puntuaciones()
    if puntuaciones:
        ordenar_estadistica(puntuaciones, longitud_minima)
        puntuaciones = cargar_puntuaciones()

    boton_sonido = pygame.mixer.Sound(sonidos["botones"])

    siguiente_pantalla = "puntuacion"
    mostrar_icono = False
    volumen = 0.5
    pygame.mixer.music.set_volume(volumen)

    imagen_icono = pygame.image.load(imagenes["Icono_volumen"])
    icono_volumen = pygame.transform.scale(imagen_icono, (50, 50))

    bandera_juego = True
    while bandera_juego:

        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                siguiente_pantalla = "salir"
                bandera_juego = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver["Rectangulo"].collidepoint(evento.pos):
                    boton_sonido.play()
                    pygame.mixer.music.stop()
                    siguiente_pantalla = "menu"
                    bandera_juego = False

        volumen, mostrar_icono = ajustar_volumen(lista_eventos, volumen, icono_volumen)
        dibujar(boton_volver)
        pygame.draw.rect(ventana_puntuacion, "Green", boton_volver["Rectangulo"], 9)
        
        ventana_puntuacion.blit(imagen_fondo_juego, [0, 0])
        
        if puntuaciones:
            mostrar_puntuaciones(puntuaciones, ventana_puntuacion)

        if mostrar_icono:
            ventana_puntuacion.blit(icono_volumen, (10, 10))


        pygame.display.update()
        pygame.time.delay(100)
    return siguiente_pantalla
