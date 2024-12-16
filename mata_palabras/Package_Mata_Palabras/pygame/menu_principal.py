import pygame
from Modulo_central import crear_boton, dibujar, imagenes, sonidos, DIMENSIONES_PANTALLA, boton_sonido, ajustar_volumen, mostrar_icono_volumen

def crear_menu_principal():
    from botones import crear_boton, dibujar
    from Datos_juego import imagenes, sonidos, DIMENSIONES_PANTALLA, boton_sonido
    from Configuraciones import ajustar_volumen, mostrar_icono_volumen

    pygame.init()
    pygame.mixer.init()

    ventana = pygame.display.set_mode(DIMENSIONES_PANTALLA)
    pygame.display.set_caption("Mata Palabras")

    icono_ventana = pygame.image.load(imagenes["Icono"])
    pygame.display.set_icon(icono_ventana)

    imagen_icono = pygame.image.load(imagenes["Icono_volumen"])
    icono_volumen = pygame.transform.scale(imagen_icono, (50, 50))
    pygame.mixer.music.load(sonidos["cancion_menu"])
    volumen = 0.5
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)
    mostrar_icono = False

    imagen_menu_principal = pygame.image.load(imagenes["Menu"])
    
    boton_empezar = crear_boton(ventana = ventana,
                                posicion = (275, 271),
                                dimensiones_boton = [400 , 100], 
                                path_imagen = imagenes["Empezar"])
    
    boton_puntuacion = crear_boton(ventana = ventana,
                                posicion = (273,456),
                                dimensiones_boton = [245 , 85],
                                path_imagen = imagenes["Puntuacion"])

    siguiente_pantalla = "menu"
    bandera = True
    while bandera == True:
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                siguiente_pantalla = "salir"
                bandera = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_empezar["Rectangulo"].collidepoint(evento.pos):
                    boton_sonido.play()
                    pygame.mixer.music.stop()
                    siguiente_pantalla = "inicio"
                    bandera = False
                    
                elif boton_puntuacion["Rectangulo"].collidepoint(evento.pos):
                    boton_sonido.play()
                    pygame.mixer.music.stop()
                    siguiente_pantalla = "puntuacion"
                    bandera = False


        volumen, mostrar_icono = ajustar_volumen(lista_eventos, volumen, icono_volumen)
        if ventana != None:
            dibujar(boton_empezar)

            pygame.draw.rect(ventana, "Green",boton_empezar["Rectangulo"],9)

            dibujar(boton_puntuacion)

            pygame.draw.rect(ventana, "Green",boton_puntuacion["Rectangulo"],9)

            ventana.blit(imagen_menu_principal, [0,0])
            
            if mostrar_icono:
                mostrar_icono_volumen(ventana, icono_volumen, mostrar_icono)

        pygame.display.update()
        pygame.time.delay(100)
    return siguiente_pantalla


