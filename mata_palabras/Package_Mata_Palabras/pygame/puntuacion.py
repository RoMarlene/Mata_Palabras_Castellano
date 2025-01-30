import pygame
import json
from Botones import crear_boton, dibujar
from Datos_juego import datos, DIMENSIONES_PANTALLA, imagenes, sonidos
from Configuraciones import ajustar_volumen
from Disaster import ordenar_estadistica
from Funciones import *

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
    ventana, imagen_fondo_juego, _, _ = inicializar_pantalla(
        titulo="Puntuación",
        icono=imagenes["Icono"],
        fondo=imagenes["Fondo_Puntuacion"],
        fuente_config=("Arial", 30),
        color_fuente=datos["BLANCO"],
        musica=sonidos["cancion_puntuacion"],
        volumen=datos["volumen_predefinido"]
    )

    # Configurar el botón de volver
    boton_volver = crear_boton(
        ventana=ventana,
        posicion=(624, 68),
        dimensiones_boton=[160, 56],
        path_imagen=imagenes["Volver"]  # Asegúrate de que esta clave sea correcta
    )

    boton_sonido = pygame.mixer.Sound(sonidos["botones"])
    imagen_icono = pygame.image.load(imagenes["Icono_volumen"])
    icono_volumen = pygame.transform.scale(imagen_icono, (50, 50))
    longitud_minima = datos["longitud_minima"]

    # Cargar y ordenar puntuaciones
    puntuaciones = cargar_puntuaciones()
    if puntuaciones:
        ordenar_estadistica(puntuaciones, longitud_minima)

    siguiente_pantalla = "puntuacion"
    bandera_juego = True
    volumen = datos["volumen_predefinido"]
    mostrar_icono = False

    while bandera_juego:
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            # Usar la función manejar_boton
            siguiente_pantalla = manejar_boton(evento, boton_volver, boton_sonido, "puntuacion", "volver") or siguiente_pantalla

            if siguiente_pantalla == "menu":
                bandera_juego = False
                break

            # Manejar salida con el evento QUIT
            if evento.type == pygame.QUIT:
                siguiente_pantalla = "salir"
                bandera_juego = False
                break

        # Ajustar el volumen según los eventos
        volumen, mostrar_icono = ajustar_volumen(lista_eventos, volumen)

        # Dibujar en la ventana
        dibujar(boton_volver)
        ventana.blit(imagen_fondo_juego, (0, 0))

        if puntuaciones:
            mostrar_puntuaciones(puntuaciones, ventana)

        if mostrar_icono:
            ventana.blit(icono_volumen, (10, 10))

        pygame.display.update()


    return siguiente_pantalla
