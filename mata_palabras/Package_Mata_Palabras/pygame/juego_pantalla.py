import pygame
from Datos_juego import imagenes, DIMENSIONES_PANTALLA, boton_sonido, sonidos, datos, posiciones, mensajes, diccionario_palabras
from Esenciales import crear_temporizador, mostrar_temporizador, iniciar_temporizador, mostrar_mensaje_con_fondo
from botones import crear_boton, dibujar
from Linea import *
from Enemigos import *
from Disaster import *
from Palabras import *

def ventana_juego():
    from Modulo_central import crear_final
    ventana_juego = pygame.display.set_mode(DIMENSIONES_PANTALLA)
    pygame.display.set_caption("Juego")
    imagen_fondo_juego = pygame.image.load(imagenes["Juego"])

    imagen_temporizador = pygame.image.load(imagenes["Temporizador"])
    imagen_temporizador = pygame.transform.smoothscale(imagen_temporizador, (60, 60))

    imagen_vidas = pygame.image.load(imagenes["Vidas"])
    imagen_vidas = pygame.transform.smoothscale(imagen_vidas, (30, 30))

    imagen_puntuacion = pygame.image.load(imagenes["Puntaje"])
    imagen_puntuacion = pygame.transform.smoothscale(imagen_puntuacion, (50, 50))

    boton_volver = crear_boton(ventana = ventana_juego,
                                posicion = (624, 68),
                                dimensiones_boton = [160 , 56],
                                path_imagen = imagenes["Volver"])

    siguiente_pantalla = "juego"

    color_fondo = (128, 128, 128)
    color_texto = datos["BLANCO"]
    fuente = pygame.font.SysFont("Acumin Variable Concept", datos["tamaño_fuente"])

    inicio_linea = (0, 470)
    final_linea = (800, 470)
    grosor = 5
    color = (0, 0, 121)
    linea_defensiva = crear_linea(ventana=ventana_juego, inicio_linea=inicio_linea, final_linea=final_linea, grosor=grosor, color=color)
    linea_y = inicio_linea[1]
    
    pygame.mixer.music.load(sonidos["sonido_juego"])  
    pygame.mixer.music.play(loops=-1)
    
    bandera_juego = True
    datos["tiempo_inicio"] = None 

    input_rect = pygame.Rect(50, 500, 200, 50)
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color(color)
    color_actual = color_inactivo
    texto_usuario = ""
    activo = False
    vidas = datos["vida"]
    posicion_vidas = datos["posicion_vida"]
    posicion_puntajes = datos["posicion_puntaje"]

    iniciar_temporizador()
    mensaje = mensajes["tiempo_agotado"]

    enemigos = []
    palabras_seleccionadas = []
    ancho_celda = 160
    alto_celda = 30
    matriz = crear_matriz_posiciones(datos["ANCHO"], datos["ALTO"], ancho_celda, alto_celda)
    posiciones_ocupadas = []

    puntaje_actual = 0

    juego_terminado = False

    TIEMPO_CONGELADO = 10
    comodin_activo = False
    comodin_usado = False
    inicio_congelamiento = 0
    tiempo_restante = datos["duracion_total"]

    while bandera_juego:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                siguiente_pantalla = "salir"
                bandera_juego = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver["Rectangulo"].collidepoint(evento.pos):
                    pygame.mixer.music.stop()
                    boton_sonido.play()
                    siguiente_pantalla = "menu"
                    bandera_juego = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    if comodin_usado == False:
                        inicio_congelamiento = pygame.time.get_ticks()
                        comodin_activo = True
                        comodin_usado = True
                        mostrar_mensaje_con_fondo(ventana_juego, mensajes["Comodines_en_uso"], (240, 250), (0, 0, 0), color_texto, fuente)
                    else:
                        mostrar_mensaje_con_fondo(ventana_juego, mensajes["comodines_usados"], (240, 250), (0, 0, 0), color_texto, fuente)

                if comodin_activo:
                    tiempo_actual = pygame.time.get_ticks()
                    tiempo_transcurrido = (tiempo_actual - inicio_congelamiento) / 1000

                    if tiempo_transcurrido >= TIEMPO_CONGELADO:
                        comodin_activo = False
                else:
                    tiempo_restante = crear_temporizador(datos["duracion_total"], datos["tiempo_inicio"])


                pygame.display.flip()

        if juego_terminado == True or vidas <= 0:
            ventana_juego.blit(imagen_fondo_juego, [0, 0])
            mostrar_mensaje_con_fondo(ventana_juego, mensajes["vidas_agotadas"], (240, 250), (0, 0, 0), color_texto, fuente)
            pygame.display.flip()
            pygame.time.wait(3000)
            siguiente_pantalla = crear_final(
            puntaje_actual=puntaje_actual, 
            tiempo_jugado=datos["duracion_total"] - tiempo_restante, 
            vidas_restantes=vidas
        )
            bandera_juego = False
            continue
        
        tiempo_restante = crear_temporizador(datos["duracion_total"], datos["tiempo_inicio"])

        palabras_enemigos = []
        for enemigo in enemigos:
            palabras_enemigos.append(enemigo["palabra"])

        if activo:
            color_actual = color_activo
        else:
            color_actual = color_inactivo
        texto_usuario, activo, eliminar_palabra, vidas, puntaje_actual, texto_procesado = manejar_cuadro_texto(
            eventos, texto_usuario, activo, input_rect, palabras_enemigos, vidas, puntaje_actual, diccionario_palabras
        )

        if vidas <= 0:
            juego_terminado = True
            continue

        if eliminar_palabra:
            enemigos_filtrados = []
            for enemigo in enemigos:
                if enemigo["palabra"].lower().strip() != texto_procesado:
                    enemigos_filtrados.append(enemigo)
                else:
                    puntaje_actual = calcular_puntaje(diccionario_palabras, puntaje_actual, texto_procesado)

            enemigos = enemigos_filtrados
        
        colision_detectada = verificar_colision_con_linea(enemigos, linea_y)

        if colision_detectada:
            vidas = restar_vidas(vidas)
            if vidas <= 0:
                juego_terminado = True

        ventana_juego.blit(imagen_fondo_juego, [0, 0])

        if tiempo_restante > 0:
                dibujar(boton_volver)
                pygame.draw.rect(ventana_juego, "Green", boton_volver["Rectangulo"], 9)
                ventana_juego.blit(imagen_fondo_juego, [0, 0])
                mostrar_temporizador(ventana_juego, tiempo_restante, posiciones["posicion_temporizador"], datos["color_temporizador"], datos["tamaño_fuente_temporizador"])
                ventana_juego.blit(imagen_temporizador, [0, 0])
                mostrar_vidas(ventana_juego, vidas, posicion_vidas, color_texto, datos["tamaño_fuente_temporizador"])
                ventana_juego.blit(imagen_vidas, [15, 50])
                mostrar_puntaje(ventana_juego, puntaje_actual, posicion_puntajes, color_texto, 30)
                ventana_juego.blit(imagen_puntuacion, [5, 75])

                if len(enemigos) < datos["maximo_enemigos"]:
                    nuevos_enemigos = crear_enemigos(DIMENSIONES_PANTALLA, datos["maximo_enemigos"], tiempo_restante, diccionario_palabras, palabras_seleccionadas)
                    for nuevo_enemigo in nuevos_enemigos:
                        posicion = colocar_palabra_en_matriz(
                                    nuevo_enemigo['palabra'],
                                    matriz,
                                    ancho_celda,
                                    alto_celda,
                                    datos["ANCHO"],
                                    fuente
                                )
                        if len(posiciones_ocupadas) > 0: 
                            posiciones_ocupadas.clear()
                        solapamiento = verificar_solapamiento(nuevo_enemigo, posiciones_ocupadas)
                        if solapamiento == False:
                            enemigos.append(nuevo_enemigo)
                            posiciones_ocupadas.append((nuevo_enemigo["x"], nuevo_enemigo["y"]))

                actualizar_posiciones_enemigos(enemigos, DIMENSIONES_PANTALLA)

                dibujar_enemigos(ventana_juego, enemigos, fuente, color_texto)
        else:
            if tiempo_restante <= 0:
                posicion = (240, 250)
                mostrar_mensaje_con_fondo(ventana_juego, mensaje, posicion, color_fondo, color_texto, fuente)

        pygame.draw.rect(ventana_juego, color_actual, input_rect, 2)
        texto_renderizado = fuente.render(texto_usuario, True, datos["BLANCO"])
        ventana_juego.blit(texto_renderizado, (input_rect.x + 5, input_rect.y + 5))
        
        # Ajustar ancho del rectángulo de entrada manualmente
        if texto_renderizado.get_width() + 10 > 200:
            input_rect.w = texto_renderizado.get_width() + 10
        else:
            input_rect.w = 200

        dibujar_linea(linea_defensiva)

        pygame.display.flip()
    return siguiente_pantalla