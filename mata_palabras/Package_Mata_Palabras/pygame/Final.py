import pygame
from Configuraciones import ajustar_volumen, mostrar_icono_volumen
from Datos_juego import datos, DIMENSIONES_PANTALLA, imagenes, sonidos, mensajes, posiciones
from Archivos import guardar_puntaje_json
from Funciones import manejar_eventos_generales, manejar_colores_cuadro_texto, inicializar_pantalla, blitear_imagenes
from Esenciales import mostrar_mensaje_con_fondo  # Importa la función que creaste
from Palabras import manejar_cuadro_texto_final

def crear_final(puntaje_actual, tiempo_jugado, vidas_restantes):
    ventana, fondo_imagen, fuente, color_texto = inicializar_pantalla(
        titulo="Final :)",
        icono=imagenes["Icono"],
        fondo=imagenes["Final"],
        fuente_config=("Acumin Variable Concept", datos["tamaño_fuente"]),
        color_fuente=datos["BLANCO"],
        musica=sonidos["sonido_final"],
        volumen=0.5
    )

    input_rect = datos["Rectangulo_texto_final"]
    color_inactivo = datos["color_inactivo"]
    color_activo = datos["color_activo"]
    texto_usuario = ""
    activo = False  # Inicializamos el estado del cuadro de texto
    bandera = True
    siguiente_pantalla = None

    icono_volumen = pygame.transform.scale(
        pygame.image.load(imagenes["Icono_volumen"]), datos["tamaño_icono_volumen"]
    )
    volumen = datos["volumen_predefinido"]
    mostrar_icono = False

    while bandera:
        eventos = pygame.event.get()
        bandera, siguiente_pantalla, texto_usuario, activo = manejar_eventos_generales(
            eventos, contexto="final", activo=activo, texto_actual=texto_usuario, input_rect=input_rect
        )

        if siguiente_pantalla:
            if siguiente_pantalla == "guardar":
                if texto_usuario.strip():
                    # Guardar el puntaje
                    guardar_puntaje_json(texto_usuario, puntaje_actual, tiempo_jugado, vidas_restantes)
                    
                    # Mostrar mensaje después de guardar
                    mostrar_mensaje_con_fondo(
                        ventana,
                        mensajes["mensaje_final"],
                        posiciones["posicion_mensaje_final"],
                        color_fondo=(0, 0, 0),
                        color_texto=color_texto,
                        fuente=fuente
                    )
                    
                    pygame.display.update()  # Actualizar pantalla para mostrar el mensaje
                    pygame.time.wait(3000)  # Esperar 3 segundos
                    siguiente_pantalla = "menu"  # Cambiar a la pantalla del menú
            bandera = False

        # Cambiar color del cuadro de texto según su estado
        color_actual = manejar_colores_cuadro_texto(activo, color_activo, color_inactivo)
        texto_usuario, activo, texto_procesado = manejar_cuadro_texto_final(
            eventos=eventos,
            texto_usuario=texto_usuario,
            activo=activo,
            input_rect=input_rect,
            max_longitud_texto=20  # Configura el máximo número de caracteres permitidos
        )

        # Renderizar el texto ingresado
        texto_renderizado = fuente.render(texto_usuario, True, color_texto)

        # Blitear elementos
        elementos_a_blitear = [
            (fondo_imagen, (0, 0)),  # Fondo
            (texto_renderizado, (input_rect.x + 5, input_rect.y + 5)),  # Texto del usuario
        ]
        blitear_imagenes(ventana, elementos_a_blitear)

        # Dibujar el rectángulo del cuadro de texto
        pygame.draw.rect(ventana, color_actual, input_rect, 2)

        # Manejar y mostrar el icono de volumen
        volumen, mostrar_icono = ajustar_volumen(eventos, volumen)
        if mostrar_icono:
            ventana.blit(icono_volumen, datos["posicion_icono_volumen"])

        # Actualizar pantalla
        pygame.display.update()
        pygame.time.Clock()

    return siguiente_pantalla
