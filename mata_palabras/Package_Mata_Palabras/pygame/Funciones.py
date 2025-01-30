import pygame
from Datos_juego import *
from Palabras import *
from Esenciales import *
from Enemigos import *
from Disaster import *
from Linea import crear_linea
from Comodines import *

"""
Configura e inicializa los recursos para una pantalla genérica.
Devuelve los objetos necesarios para usar en el juego.

Args:
    titulo (str): Título de la ventana.
    icono (str): Ruta al ícono de la ventana.
    fondo (str): Ruta a la imagen de fondo.
    fuente_config (tuple): Configuración de fuente (nombre, tamaño).
    color_fuente (tuple): Color del texto.
    musica (str, opcional): Ruta al archivo de música.
    volumen (float, opcional): Volumen de la música.

Returns:
    ventana, fondo_imagen, fuente, color_fuente
"""
def inicializar_pantalla(titulo, icono, fondo, fuente_config, color_fuente, musica=None, volumen=0.5):
    pygame.init()
    pygame.mixer.init()

    # Configuración de la ventana
    ventana = pygame.display.set_mode(DIMENSIONES_PANTALLA)
    pygame.display.set_caption(titulo)

    # Configuración de recursos gráficos
    icono_ventana = pygame.image.load(icono)
    pygame.display.set_icon(icono_ventana)

    fondo_imagen = pygame.image.load(fondo)

    # Configuración de la fuente
    nombre_fuente, tamaño_fuente = fuente_config  # Asegúrate de que fuente_config sea una tupla (nombre, tamaño)
    fuente = pygame.font.SysFont(nombre_fuente, tamaño_fuente)

    if musica:
        pygame.mixer.music.load(musica)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)

    return ventana, fondo_imagen, fuente, color_fuente

def manejar_boton(evento, boton, sonido, contexto, nombre_boton):
    siguiente_pantalla = None  

    # Verificar que se haya hecho clic en el botón
    if evento.type == pygame.MOUSEBUTTONDOWN and boton["Rectangulo"].collidepoint(evento.pos):
        sonido.play()
        pygame.mixer.music.stop()

        match contexto:
            case "menu":
                match nombre_boton:
                    case "inicio":
                        siguiente_pantalla = "juego"  # El botón "inicio" lleva a "juego"
                    case "puntuacion":
                        siguiente_pantalla = "puntuacion"  # El botón "puntuacion" lleva a la pantalla de puntuaciones
            case "puntuacion" | "juego":
                match nombre_boton:
                    case "volver":
                        siguiente_pantalla = "menu"  # El botón "volver" lleva al menu

    return siguiente_pantalla

def manejar_colores_cuadro_texto(activo, color_activo, color_inactivo):
    if activo:
        color_actual = color_activo
    else:
        color_actual = color_inactivo

    return color_actual

def manejar_eventos_generales(eventos, contexto, activo=False, texto_actual="", input_rect=None, botones=None):
    """
    Maneja eventos generales según el contexto de la pantalla.
    Devuelve una acción, el nuevo estado de la bandera y la siguiente pantalla.
    
    Args:
        eventos (list): Lista de eventos capturados por pygame.
        contexto (str): Indica en qué pantalla se está ejecutando.
        activo (bool, opcional): Indica si un campo de texto está activo (usado en el final del juego).
        texto_actual (str, opcional): Texto ingresado en un cuadro de texto.
        input_rect (pygame.Rect, opcional): Rectángulo del input de texto para detectar clics.
        botones (dict, opcional): Diccionario de botones con estructura {"nombre": {"Rectangulo": rect, "Sonido": sonido}}.
    
    Returns:
        bandera (bool): Controla si el bucle sigue ejecutándose.
        siguiente_pantalla (str): La pantalla a la que se debe cambiar.
        texto_actual (str): Texto actualizado (si aplica).
        activo (bool): Nuevo estado del campo de texto.
    """
    bandera = True
    siguiente_pantalla = None
    
    for evento in eventos:
        match evento.type:
            case pygame.QUIT:
                bandera = False
                siguiente_pantalla = "salir"

            case pygame.KEYDOWN:
                match contexto:
                    case "menu":
                        if evento.key == TECLAS_JUEGO["iniciar_juego"]:
                            bandera = False
                            siguiente_pantalla = "juego"
                    case "inicio":
                        if evento.key == pygame.K_RETURN:
                            bandera = False
                            siguiente_pantalla = "juego"
                    case "final":
                        if activo and evento.key == TECLAS_JUEGO["enviar"]:
                            siguiente_pantalla = "guardar"

            case pygame.MOUSEBUTTONDOWN:
                if contexto == "final" and input_rect and input_rect.collidepoint(evento.pos):
                    activo = True
                else:
                    activo = False

                # Nueva lógica para el menú
                if contexto == "menu" and botones:
                    for nombre, boton in botones.items():
                        if boton["Rectangulo"].collidepoint(evento.pos):
                            boton["Sonido"].play()
                            pygame.mixer.music.stop()
                            siguiente_pantalla = nombre
                            bandera = False
                            break

    return bandera, siguiente_pantalla, texto_actual, activo
"""
Blitea múltiples imágenes en la ventana.

Args:
    ventana: La superficie principal donde se dibujarán los elementos.
    elementos: Una lista de tuplas con el formato:
        [(imagen, posición), (imagen, posición), ...]
        - imagen: Superficie de Pygame (puede ser texto renderizado o imagen cargada).
        - posición: Tupla con las coordenadas (x, y) donde se bliteará la imagen.
"""
def blitear_imagenes(ventana, elementos):
    for imagen, posicion in elementos:
        ventana.blit(imagen, posicion)

def manejar_eventos_juego(eventos, contexto, boton_volver, fuente, ventana, comodin_activo=False, tiempo_congelamiento=0, TIEMPO_CONGELADO=0, datos=None):
    """
    Maneja los eventos del juego, incluyendo los eventos de teclado y ratón, y la lógica de control del comodín.
    """
    bandera_juego = True
    siguiente_pantalla = None
    tiempo_restante = None  # Inicializamos tiempo_restante

    for evento in eventos:
        match evento:
            case pygame.QUIT:
                bandera_juego = False
                siguiente_pantalla = "salir"
            case pygame.MOUSEBUTTONDOWN:
                # Lógica para manejar clics del ratón
                siguiente_pantalla = boton_volver
                if siguiente_pantalla == "menu":
                    bandera_juego = False
            case pygame.KEYDOWN:
                # Lógica para manejar presion de teclas
                siguiente_pantalla = boton_volver
                if siguiente_pantalla == "menu":
                    bandera_juego = False

                # Verificar si se activa el comodín de tiempo
                if evento.key == TECLAS_JUEGO["comodin_tiempo"]:  # Comprobar si se presiona la tecla del comodín
                    if comodin_activo == False:  # Comprobar si el comodín no está activo
                        activar_comodin_tiempo(
                            evento=evento,
                            diccionario_juego=datos,
                            tiempo_inicio=datos["tiempo_inicio"],
                            diccionario_mensajes=mensajes,
                            fuente=fuente,
                            pantalla=ventana,
                            posicion=(240, 200),  # Puedes cambiar la posición donde se muestra el mensaje
                            color_fondo=(0, 0, 0),  # Fondo negro
                            color_texto=(255, 255, 255)  # Texto blanco
                        )
                        comodin_activo = True  # Marcamos el comodín como activo
                    else:
                        pass  # Si el comodín ya está activo, no hacer nada

    # Temporizador (si el comodín no está activo)
    if comodin_activo == False and datos:
        tiempo_restante = crear_temporizador(datos["duracion_total"], datos["tiempo_inicio"])

    pygame.display.flip()

    return bandera_juego, siguiente_pantalla, tiempo_restante

def gestionar_temporizador(evento, datos, tiempo_restante, diccionario_mensajes, fuente, pantalla):
    print("🔹 Evento recibido en gestionar_temporizador:", evento)  # Debug

    if evento.type == pygame.KEYDOWN:
        if evento.key == TECLAS_JUEGO["comodin_tiempo"]:
            print("✅ Se activó el comodín de tiempo")  # Debug
            activar_comodin_tiempo(datos, datos["tiempo_inicio"], diccionario_mensajes, fuente, pantalla, 
                                    datos["BLANCO"])


    tiempo_restante = calcular_tiempo_restante(datos)
    print("⏳ Tiempo restante calculado:", tiempo_restante)  # Debug

    return tiempo_restante, False

def verificar_juego_terminado(juego_terminado, vidas, ventana, imagen_fondo_juego, mensajes, color_texto, fuente, puntaje_actual, datos, tiempo_restante):
    """
    Verifica si el juego ha terminado y prepara los datos para la función de finalizar el juego.
    Devuelve un diccionario con los datos necesarios para crear la pantalla final.
    """
    resultado = {
        "juego_terminado": False,
        "datos_finales": None  
    }
    if juego_terminado or vidas <= 0:
        ventana.blit(imagen_fondo_juego, [0, 0])
        mostrar_mensaje_con_fondo(ventana, mensajes["vidas_agotadas"], (240, 250), (0, 0, 0), color_texto, fuente)
        pygame.display.flip()
        pygame.time.wait(3000)  # Espera de 3 segundos

        # Preparar los datos para la función crear_final
        resultado["juego_terminado"] = True
        resultado["datos_finales"] = {
            "puntaje_actual": puntaje_actual,
            "tiempo_jugado": datos["duracion_total"] - tiempo_restante,
            "vidas_restantes": vidas
        }
    
    return resultado

def dibujar_rectangulo_texto(ventana, color_actual, input_rect,fuente, texto_usuario):
    pygame.draw.rect(ventana, color_actual, input_rect, 2)
    texto_renderizado = fuente.render(texto_usuario, True, datos["BLANCO"])
    ventana.blit(texto_renderizado, (input_rect.x + 5, input_rect.y + 5))

def inicializar_variables(ventana):
    imagen_temporizador = pygame.image.load(imagenes["Temporizador"])
    imagen_temporizador = pygame.transform.smoothscale(imagen_temporizador, (60, 60))

    imagen_vidas = pygame.image.load(imagenes["Vidas"])
    imagen_vidas = pygame.transform.smoothscale(imagen_vidas, (30, 30))

    imagen_puntuacion = pygame.image.load(imagenes["Puntaje"])
    imagen_puntuacion = pygame.transform.smoothscale(imagen_puntuacion, (50, 50))
    siguiente_pantalla = "juego"

    color_fondo = (0, 0, 0)
    color_texto = datos["BLANCO"]

    inicio_linea = (0, 470)
    final_linea = (800, 470)
    grosor = 5
    color = (0, 0, 121)
    linea_defensiva = crear_linea(ventana=ventana, inicio_linea=inicio_linea, final_linea=final_linea, grosor=grosor, color=color)
    linea_y = inicio_linea[1]
    
    bandera_juego = True
    datos["tiempo_inicio"] = None 

    input_rect = datos["rectangulo_texto_juego"]
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color(color)
    color_actual = color_inactivo
    texto_usuario = ""
    activo = False
    vidas = datos["vida"]
    posicion_vidas = posiciones["posicion_vida"]
    posicion_puntajes = posiciones["posicion_puntaje"]

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
    inicio_congelamiento = 0
    tiempo_restante = datos["duracion_total"]

    return (imagen_temporizador, imagen_puntuacion, imagen_vidas, siguiente_pantalla, color_fondo, color_texto, 
        inicio_linea, final_linea, grosor, color, linea_defensiva, linea_y, bandera_juego, datos["tiempo_inicio"], 
        input_rect, color_inactivo, color_activo, color_actual, texto_usuario, activo, vidas, posicion_vidas, posicion_puntajes,
        mensaje, enemigos, palabras_seleccionadas, ancho_celda, alto_celda, matriz, posiciones_ocupadas, puntaje_actual, juego_terminado,
        TIEMPO_CONGELADO, comodin_activo, inicio_congelamiento, tiempo_restante)


def manejar_comodines(evento, datos, tiempo_restante, inicio_congelamiento, TIEMPO_CONGELADO, ventana, mensajes, fuente):
    if evento.type == pygame.KEYDOWN:
        tecla_presionada = evento.key  # Guardamos la tecla presionada

        # Extraemos los valores de las teclas para que match-case los reconozca correctamente
        tecla_comodin_tiempo = TECLAS_JUEGO["comodin_tiempo"]
        #tecla_comodin_otro = TECLAS_JUEGO["comodin_otro"]
        #tecla_comodin_extra = TECLAS_JUEGO["comodin_extra"]

        # Aquí la comparación para que el match-case sea válido
        if tecla_presionada == tecla_comodin_tiempo:
            match tecla_presionada:
                case tecla_comodin_tiempo:
                    tiempo_restante, _ = gestionar_temporizador(
                    evento=evento,
                    datos=datos,
                    tiempo_restante=tiempo_restante,
                    diccionario_mensajes=mensajes,
                    fuente=fuente,
                    pantalla=ventana
                )
                    print("Tecla presionada en manejar_comodines:", evento.key)

        # elif tecla_presionada == tecla_comodin_otro:
        #     match tecla_presionada:
        #         case tecla_comodin_otro:
        #             pass

        # elif tecla_presionada == tecla_comodin_extra:
        #     match tecla_presionada:
        #         case tecla_comodin_extra:
        #             pass

    return tiempo_restante, inicio_congelamiento