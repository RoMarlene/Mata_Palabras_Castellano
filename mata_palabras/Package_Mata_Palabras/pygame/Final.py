import pygame
from Modulo_central import crear_boton, dibujar, imagenes, sonidos, DIMENSIONES_PANTALLA, boton_sonido, ajustar_volumen, mostrar_icono_volumen
from archivos import *
from Datos_juego import datos

def crear_final(puntaje_actual, tiempo_jugado, vidas_restantes):
    pygame.init()
    pygame.mixer.init()

    ventana = pygame.display.set_mode(DIMENSIONES_PANTALLA)
    pygame.display.set_caption("Final :)")

    icono_ventana = pygame.image.load(imagenes["Icono"])
    pygame.display.set_icon(icono_ventana)

    imagen_icono = pygame.image.load(imagenes["Icono_volumen"])
    icono_volumen = pygame.transform.scale(imagen_icono, (50, 50))
    pygame.mixer.music.load(sonidos["sonido_final"])
    volumen = 0.5
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)
    mostrar_icono = False

    imagen_final = pygame.image.load(imagenes["Final"])
    fuente = pygame.font.SysFont("Acumin Variable Concept", datos["tamaño_fuente"])
    color_texto = datos["BLANCO"]
    
    boton_volver = crear_boton(
        ventana=ventana,
        posicion=(624, 68),
        dimensiones_boton=[160, 56],
        path_imagen=imagenes["Puntuacion"]
    )

    siguiente_pantalla = "menu"

    # Configuración del cuadro de texto
    input_rect = pygame.Rect(200, 300, 400, 50) 
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color('dodgerblue2')
    color_actual = color_inactivo
    texto_usuario = ""
    activo = False
    bandera = True

    while bandera:
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                siguiente_pantalla = "salir"
                bandera = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Activar el cuadro de texto al hacer clic en él
                if input_rect.collidepoint(evento.pos):
                    activo = True
                else:
                    activo = False
                
                if boton_volver["Rectangulo"].collidepoint(evento.pos):
                    boton_sonido.play()
                    pygame.mixer.music.stop()
                    siguiente_pantalla = "menu"
                    bandera = False

            elif evento.type == pygame.KEYDOWN:
                if activo:  # Solo captura texto si el cuadro está activo
                    if evento.key == pygame.K_RETURN:
                        if texto_usuario.strip(): 
                            guardar_puntaje_json(texto_usuario, puntaje_actual, tiempo_jugado, vidas_restantes)
                            texto_usuario = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_usuario = texto_usuario[:-1]
                    else:
                        texto_usuario += evento.unicode


        color_actual = color_activo if activo else color_inactivo

        dibujar(boton_volver)
        pygame.draw.rect(ventana, "Green", boton_volver["Rectangulo"], 9)
        # Dibujar en la ventana
        ventana.blit(imagen_final, [0, 0])

        # Mostrar texto de entrada
        pygame.draw.rect(ventana, color_actual, input_rect, 2)  # Dibujar el cuadro de texto
        texto_renderizado = fuente.render(texto_usuario, True, color_texto)
        ventana.blit(texto_renderizado, (input_rect.x + 5, input_rect.y + 5))

        # Volumen y botones
        volumen, mostrar_icono = ajustar_volumen(lista_eventos, volumen, icono_volumen)
        if mostrar_icono:
            mostrar_icono_volumen(ventana, icono_volumen, mostrar_icono)

        pygame.display.update()
        pygame.time.delay(100)

    return siguiente_pantalla
