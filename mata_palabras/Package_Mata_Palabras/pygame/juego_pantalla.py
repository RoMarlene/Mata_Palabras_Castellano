import pygame
from Datos_juego import imagenes, DIMENSIONES_PANTALLA, boton_sonido, sonidos, datos, posiciones, mensajes, diccionario_palabras
from Esenciales import mostrar_texto, iniciar_temporizador, mostrar_mensaje_con_fondo
from Botones import crear_boton, dibujar
from Linea import *
from Enemigos import *
from Disaster import *
from Palabras import *
from Final import crear_final
from Funciones import *
from Comodines import *

def ventana_juego():
    ventana, imagen_fondo_juego, fuente, color_fuente = inicializar_pantalla(
        titulo="Juego",
        icono=imagenes["Icono"],
        fondo=imagenes["Juego"],
        fuente_config=("Acumin Variable Concept", 24),
        color_fuente=(128, 128, 128),
        musica=sonidos["sonido_juego"],
        volumen=0.5
    )

    boton_volver = crear_boton(ventana = ventana,
                                posicion = (624, 68),
                                dimensiones_boton = [160 , 56],
                                path_imagen = imagenes["Volver"])
    (
    imagen_temporizador, imagen_puntuacion, imagen_vidas, 
    siguiente_pantalla, color_fondo, color_texto, 
    inicio_linea, final_linea, grosor, color, 
    linea_defensiva, linea_y, bandera_juego, 
    datos["tiempo_inicio"], input_rect, color_inactivo, 
    color_activo, color_actual, texto_usuario, activo, 
    posicion_vidas, posicion_puntajes, mensaje, 
    enemigos, palabras_seleccionadas, ancho_celda, 
    alto_celda, matriz, posiciones_ocupadas, puntaje_actual, 
    juego_terminado, TIEMPO_CONGELADO, comodin_activo, 
    inicio_congelamiento, tiempo_restante, reloj, multiplicador_puntos, palabras_multiplicadas
) = inicializar_variables(ventana)
    
    iniciar_temporizador()

    while bandera_juego:
        eventos = pygame.event.get()
        for evento in eventos:
            siguiente_pantalla = manejar_boton(
                    evento=evento, 
                    boton=boton_volver, 
                    sonido=boton_sonido, 
                    contexto="juego", 
                    nombre_boton="volver"
                )
            
            if siguiente_pantalla == "menu":
                pygame.mixer.music.stop()  # Detenemos la música de esta pantalla
                bandera_juego = False  # Terminamos el bucle del juego
                break  # Salimos del bucle de eventos

        # Aquí sigue el resto de la lógica del juego, solo si no se ha presionado "Volver"
        if bandera_juego == False:
            break

        bandera_juego, siguiente_pantalla, tiempo_restante = manejar_eventos_juego(
    eventos=eventos,
    contexto="juego",
    boton_volver=boton_volver,
    comodin_activo=comodin_activo,
    puntaje_actual=puntaje_actual,
    tiempo_congelamiento=TIEMPO_CONGELADO,
    TIEMPO_CONGELADO=TIEMPO_CONGELADO,
    datos=datos,
    fuente=fuente,    # Aquí se pasa la fuente
    ventana=ventana,
    reloj=reloj,
    mensajes=mensajes  # ✅ Ahora sí se pasa el diccionario de mensajes
)

        resultado = verificar_juego_terminado(
            juego_terminado=juego_terminado,
            vidas=datos["vida"],
            ventana=ventana,
            imagen_fondo_juego=imagen_fondo_juego,
            mensajes=mensajes,
            color_texto=color_fuente,
            fuente=fuente,
            puntaje_actual=puntaje_actual,
            datos=datos,
            tiempo_restante=tiempo_restante
        )

        if resultado["juego_terminado"]:
            siguiente_pantalla = crear_final(
            puntaje_actual=puntaje_actual,
            tiempo_jugado=datos["duracion_total"] - tiempo_restante,
            vidas_restantes=datos["vida"]
        )
            bandera_juego = False
            break

        palabras_enemigos = []
        for enemigo in enemigos:
            palabras_enemigos.append(enemigo["palabra"])

        color_actual = manejar_colores_cuadro_texto(activo, color_activo, color_inactivo)

        texto_usuario, activo, eliminar_palabra, datos["vida"], puntaje_actual, texto_procesado = manejar_cuadro_texto(
        eventos, texto_usuario, activo, input_rect, palabras_enemigos, datos["vida"], puntaje_actual, diccionario_palabras
        )

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
            datos["vida"] = restar_vidas(datos["vida"])
            if datos["vida"] <= 0:
                juego_terminado = True

        ventana.blit(imagen_fondo_juego, [0, 0])

        if tiempo_restante > 0:
                dibujar(boton_volver)
                elementos = [
                (imagen_fondo_juego, [0, 0]),
                (imagen_temporizador, [0, 0]),
                (imagen_vidas, [15, 50]),
                (imagen_puntuacion, [5, 75])
            ]

                dibujar(boton_volver)
                blitear_imagenes(ventana, elementos)
                mostrar_texto(ventana, str(tiempo_restante), posiciones["posicion_temporizador"], datos["color_temporizador"], datos["tamaño_fuente_temporizador"])
                mostrar_texto(ventana, str(datos["vida"]), posicion_vidas, color_texto, datos["tamaño_fuente_temporizador"])
                mostrar_texto(ventana, puntaje_actual, posicion_puntajes, color_texto, 30)

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

                dibujar_enemigos(ventana, enemigos, fuente, color_texto)
                mostrar_mensaje_comodin(ventana, datos, fuente, mensajes)  
                actualizar_mensaje_comodin(datos)  # Se encarga de eliminar el mensaje cuando pase el tiempo
        else:
            if tiempo_restante <= 0:
                posicion = (240, 250)
                mostrar_mensaje_con_fondo(ventana, mensaje, posicion, color_fondo, color_texto, fuente)

        dibujar_rectangulo_texto(ventana, color_actual, input_rect,fuente, texto_usuario)

        dibujar_linea(linea_defensiva)

        pygame.display.flip()
    return siguiente_pantalla