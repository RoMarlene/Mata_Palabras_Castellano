import pygame
from Datos_juego import *
from Palabras import *
from Esenciales import *
from Enemigos import *
from Disaster import *
from Linea import crear_linea
from Comodines import *

def inicializar_pantalla(titulo, icono, fondo, fuente_config, color_fuente, musica=None, volumen=0.5)-> tuple:
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
    nombre_fuente, tamaño_fuente = fuente_config 
    fuente = pygame.font.SysFont(nombre_fuente, tamaño_fuente)

    if musica:
        pygame.mixer.music.load(musica)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)

    return ventana, fondo_imagen, fuente, color_fuente

def manejar_boton(evento: pygame.event, boton: dict, sonido: pygame.mixer.Sound, contexto: str, nombre_boton:str)-> str:
    """
    Esta funcion maneja los botones para ir a las diferentes ventanas

    Args:
        evento (pygame.event): El evento
        boton (dict): El boton
        sonido (pygame.mixer.Sound): El sonido del boton
        contexto (str):  Cual pantalla es 
        nombre_boton (str): El nombre del boton

    Returns:
        str: Retorna la siguiente pantalla
    """
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

def manejar_colores_cuadro_texto(activo: bool, color_activo: tuple, color_inactivo: tuple) -> tuple:
    """
    Esta funcion maneja los colores del cuadro de texto!

    Args:
        activo (bool): Si el cuadro esta activo
        color_activo (tuple): El color dle cuadro si esta activo
        color_inactivo (tuple): El color del cuadro si esta inactivo

    Returns:
        tuple: El color actual que tendrá el cuadro de texto
    """
    if activo:
        color_actual = color_activo
    else:
        color_actual = color_inactivo

    return color_actual

def manejar_eventos_generales(eventos, contexto, activo=False, texto_actual="", input_rect=None, botones=None)-> tuple:
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

def blitear_imagenes(ventana, elementos):
    """
    Blitea múltiples imágenes en la ventana.

    Args:
        ventana: La superficie principal donde se dibujarán los elementos.
        elementos: Una lista de tuplas con el formato:
            [(imagen, posición), (imagen, posición), ...]
            - imagen: Superficie de Pygame (puede ser texto renderizado o imagen cargada).
            - posición: Tupla con las coordenadas (x, y) donde se bliteará la imagen.
    """
    for imagen, posicion in elementos:
        ventana.blit(imagen, posicion)

def manejar_eventos_juego(eventos: pygame.event, boton_volver: str, fuente:str, ventana: pygame, reloj:int, puntaje_actual:int,  
                    datos=None, mensajes=None) -> tuple:
    """
    Maneja los eventos del juego, incluyendo eventos de teclado, ratón, lógica de comodines y entrada de palabras.

    Args:
        eventos (pygame.event): El evento
        boton_volver (str): El boton de volver
        fuente (str): La fuente
        ventana (pygame): La ventana
        reloj (int): Controla el tiempo
        puntaje_actual (int): El puntaje actual
        datos (_type_, optional): Los datos. Defaults to None.
        mensajes (_type_, optional): Los mensajes. Defaults to None.

    Returns:
        tuple: retorna la bandera del juego, la siguiente pantalla y el tiempo restante
        """
    bandera_juego = True
    siguiente_pantalla = None
    tiempo_restante = 0  # Inicializamos en 0 para evitar valores None
    texto_ingresado = ""  # Acumulador de texto ingresado por el usuario

    for evento in eventos:
        if evento.type == pygame.QUIT:
            bandera_juego = False
            siguiente_pantalla = "salir"

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver and boton_volver == "menu":
                bandera_juego = False

        elif evento.type == pygame.KEYDOWN:
            # Manejar uso de comodines
            resultado = manejar_comodines(evento, datos, tiempo_restante, ventana, mensajes, fuente)
            
            try:
                tiempo_restante, comodin_usado = resultado
            except:
                tiempo_restante = resultado, 0
                comodin_usado = False

            if comodin_usado:
                continue 

            # Captura de texto del usuario
            if evento.key == pygame.K_RETURN:  # Si presiona Enter, validar palabra
                palabra_correcta = validar_palabra(texto_ingresado, datos, diccionario_palabras, datos["vida"], puntaje_actual)

                if palabra_correcta:
                    # Si el comodín de duplicador está activo, forzar recursión explícita
                    if datos["multiplicador_puntos"] == 2 and datos["esperando_palabra"]:
                        datos["esperando_palabra"] = False  # Resetear la espera
                        comodin_duplicar_puntos(10)

                    puntaje_actual = calcular_puntaje(diccionario_palabras, puntaje_actual, texto_ingresado)

                texto_ingresado = ""  # Resetear input después de validar

            elif evento.key == pygame.K_BACKSPACE:
                texto_ingresado = texto_ingresado[:-1]  # Borrar última letra

            else:
                texto_ingresado += evento.unicode  # Agregar letra a la palabra

    # Evita que el tiempo quede en None
    tiempo_restante = crear_temporizador(datos["duracion_total"], datos["tiempo_inicio"])
    if tiempo_restante == None:
        tiempo_restante = 0  

    pygame.display.flip()

    return bandera_juego, siguiente_pantalla, tiempo_restante


def gestionar_temporizador(evento: pygame.event, datos: dict, tiempo_restante: int, diccionario_mensajes:dict)-> tuple:
    """
    
    Maneja la activación del temporizador y evita que se use el comodín dos veces.

    Args:
        evento (pygame.event): El evento
        datos (dict): El diccionario de datos
        tiempo_restante (int): El tiempo restante_
        diccionario_mensajes (dict): El diccionario de mensajes

    Returns:
        tuple: Retorna el tiempo restante y el tiempo inicio actualizado.
    """
    if evento.type == pygame.KEYDOWN:
        if evento.key == TECLAS_JUEGO["comodin_tiempo"]:
            if datos["comodin_tiempo_disponible"]:
                datos = activar_comodin_tiempo(datos, diccionario_mensajes)
    
    tiempo_restante = calcular_tiempo_restante(datos)
    return tiempo_restante, datos["tiempo_inicio"]

def verificar_juego_terminado(juego_terminado: bool, vidas: int, ventana: pygame, imagen_fondo_juego:str, mensajes: dict, 
    color_texto: tuple[int, int, int], fuente, puntaje_actual: int, datos: dict, tiempo_restante: int) -> dict:
    """
    Verifica si el juego ha terminado y prepara los datos para la función de finalizar el juego.
    Devuelve un diccionario con los datos necesarios para crear la pantalla final.

    Args:
        juego_terminado (bool): Si el juego esta terminado
        vidas (int): _Las vidas
        ventana (pygame): La ventana
        imagen_fondo_juego (str): La imagen de fondo del juego
        mensajes (dict): El diccionario de mensajes
        color_texto (tuple[int, int, int]): El color del texto
        fuente (_type_): La fuente del texto
        puntaje_actual (int): El puntaje actual
        datos (dict): el diccionario de datos
        tiempo_restante (int): El tiempo restante

    Returns:
        dict: Los datos necesarios para la pantalla final.
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

        # Preparar los datos para la ventana final.
        resultado["juego_terminado"] = True
        resultado["datos_finales"] = {
            "puntaje_actual": puntaje_actual,
            "tiempo_jugado": datos["duracion_total"] - tiempo_restante,
            "vidas_restantes": vidas
        }
    
    return resultado

def dibujar_rectangulo_texto(ventana: pygame.Surface, color_actual: tuple[int, int, int], input_rect: pygame.Rect, 
                            fuente: pygame.font.Font, texto_usuario: str):
    """
    Dibuja el rectangulo de texto

    Args:
        ventana (pygame.Surface): La ventana
        color_actual (tuple[int, int, int]): El color actual
        input_rect (pygame.Rect): El rectangulo en si 
        fuente (pygame.font.Font): La fuente
        texto_usuario (str): El texto del usuario
    """
    pygame.draw.rect(ventana, color_actual, input_rect, 2)
    texto_renderizado = fuente.render(texto_usuario, True, datos["BLANCO"])
    ventana.blit(texto_renderizado, (input_rect.x + 5, input_rect.y + 5))

def manejar_comodines(evento: pygame.event, datos:dict, tiempo_restante: int, ventana: pygame.Surface, mensajes:dict, fuente:pygame.font)-> tuple:
    """
    Maneja los comodines del juego: tiempo extra, vida extra y duplicador de puntos.
    """
    comodin_usado = False 
    if evento.type == pygame.KEYDOWN:
        tecla_presionada = evento.key

        tecla_comodin_tiempo = TECLAS_JUEGO["comodin_tiempo"]
        tecla_comodin_vida = TECLAS_JUEGO["comodin_vida"]
        tecla_comodin_duplicador = TECLAS_JUEGO["comodin_puntaje_doble"]

        if tecla_presionada == tecla_comodin_tiempo:
            match tecla_presionada:
                case tecla_comodin_tiempo:
                    tiempo_restante, _ = gestionar_temporizador(
                        evento=evento,
                        datos=datos,
                        tiempo_restante=tiempo_restante,
                        diccionario_mensajes=mensajes,
                    )
                    comodin_usado = True

        elif tecla_presionada == tecla_comodin_vida:
            match tecla_presionada:
                case tecla_comodin_vida:
                    datos = activar_comodin_vida(
                        diccionario_juego=datos,
                        diccionario_mensajes=mensajes
                    )
                    comodin_usado = True

        elif tecla_presionada == tecla_comodin_duplicador:
            match tecla_presionada:
                case tecla_comodin_duplicador:
                    if datos["comodin_duplicador_disponible"]:
                        datos["multiplicador_puntos"] = 2
                        datos["palabras_multiplicadas"] = 0
                        datos["comodin_duplicador_disponible"] = False

                        comodin_duplicar_puntos(10)  
                        comodin_usado = True 

            if comodin_usado:
                datos["comodines_disponibles"] -= 1
                if datos["comodines_disponibles"] == 0:
                    datos["tiempo_inicio_mensaje_ultimo_comodin"] = pygame.time.get_ticks()
                    datos["mostrar_mensaje_ultimo_comodin"] = True

    return tiempo_restante, comodin_usado

def inicializar_variables(ventana):
    datos["multiplicador_puntos"] = 1
    datos["palabras_multiplicadas"] = 0
    datos["vida"] = 3
    datos["comodin_vida_extra"] = True  
    datos["comodines_disponibles"] = 3
    datos["comodin_tiempo_disponible"] = True  
    datos["comodin_duplicador_disponible"] = True  
    datos["tiempo_extra"] = 10
    datos["duracion_total"] = 60
    datos["tiempo_inicio"] = None
    multiplicador_puntos = datos["multiplicador_puntos"]
    palabras_multiplicadas = datos["palabras_multiplicadas"]
    reloj = pygame.time.Clock()
    datos["vida"] = 3
    datos["comodin_vida_extra"] = True  
    datos["comodines_disponibles"] = 3
    datos["duracion_total"] = 60
    datos["tiempo_inicio"] = None  
    tiempo_restante = datos["duracion_total"]

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

    input_rect = datos["rectangulo_texto_juego"]
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color(color)
    color_actual = color_inactivo
    texto_usuario = ""
    activo = False
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

    comodin_activo = False

    return (imagen_temporizador, imagen_puntuacion, imagen_vidas, siguiente_pantalla, color_fondo, color_texto, 
        inicio_linea, final_linea, grosor, color, linea_defensiva, linea_y, bandera_juego, datos["tiempo_inicio"], 
        input_rect, color_inactivo, color_activo, color_actual, texto_usuario, activo, posicion_vidas, posicion_puntajes,
        mensaje, enemigos, palabras_seleccionadas, ancho_celda, alto_celda, matriz, posiciones_ocupadas, puntaje_actual, juego_terminado, 
        comodin_activo, tiempo_restante, reloj, multiplicador_puntos, palabras_multiplicadas)