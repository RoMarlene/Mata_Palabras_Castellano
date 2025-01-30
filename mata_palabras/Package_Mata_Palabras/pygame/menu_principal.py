import pygame
from Botones import crear_boton, dibujar
from Datos_juego import imagenes, sonidos, boton_sonido, posiciones, datos
from Configuraciones import ajustar_volumen, mostrar_icono_volumen
from Funciones import *

def crear_menu_principal():
    ventana, imagen_menu_principal, _, _ = inicializar_pantalla(
        titulo="Mata Palabras",
        icono=imagenes["Icono"],
        fondo=imagenes["Menu"],
        fuente_config=("Arial", 30),  # Se puede omitir si no se usa en el menú
        color_fuente=(255, 255, 255),
        musica=sonidos["cancion_menu"],
        volumen=datos["volumen_predefinido"]
    )

    imagen_icono = pygame.image.load(imagenes["Icono_volumen"])
    icono_volumen = pygame.transform.scale(imagen_icono, (50, 50))
    volumen = datos["volumen_predefinido"]
    mostrar_icono = False

    # Crear los botones
    boton_empezar = crear_boton(
        ventana=ventana,
        posicion=posiciones["posicion_boton_empezar"],
        dimensiones_boton=datos["tamaño_boton_empezar"],
        path_imagen=imagenes["Empezar"]
    )

    boton_puntuacion = crear_boton(
        ventana=ventana,
        posicion=posiciones["posicion_boton_puntuacion"],
        dimensiones_boton=datos["tamaño_boton_empezar"],
        path_imagen=imagenes["Puntuacion"]
    )

    botones = {
        "inicio": {"Rectangulo": boton_empezar["Rectangulo"], "Sonido": boton_sonido},
        "puntuacion": {"Rectangulo": boton_puntuacion["Rectangulo"], "Sonido": boton_sonido}
    }

    siguiente_pantalla = "menu"
    bandera = True

    while bandera:
        eventos = pygame.event.get()
        bandera, siguiente_pantalla, _, _ = manejar_eventos_generales(eventos, "menu", botones=botones)

        # Ajustar volumen según los eventos
        volumen, mostrar_icono = ajustar_volumen(eventos, volumen)

        # Dibujar elementos en la ventana
        dibujar(boton_empezar)
        dibujar(boton_puntuacion)
        ventana.blit(imagen_menu_principal, (0, 0))

        # Mostrar ícono de volumen si es necesario
        if mostrar_icono:
            mostrar_icono_volumen(ventana, icono_volumen, mostrar_icono)

        pygame.display.update()

    return siguiente_pantalla
