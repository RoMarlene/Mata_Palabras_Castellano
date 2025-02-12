import pygame


def crear_boton(ventana: str, posicion: int, dimensiones_boton: int, fuente: str = None, path_imagen: str = None) -> dict:
    """Crea el boton

    Args:
        ventana (str): Recibe la superficie.
        posicion (int): La posición.
        dimensiones_boton (int): Las dimensiones del botón.
        fuente (str, optional): La fuente del boton. Por defecto devuelve None.
        path_imagen (str, optional): El path de la imagen. Por defecto devuelve None.

    Returns:
        dict: El diccionario del boton (O sea, lo que contiene)
    """
    boton = {}
    boton["Ventana"] = ventana #Surface
    boton["Posicion"] = posicion #Tupla
    boton["Dimensiones"] = dimensiones_boton #Tupla
    boton["Presionado"] = False

    if path_imagen != None:
        imagen_juego = pygame.image.load(path_imagen)
        boton["Superficie"] = pygame.transform.scale(imagen_juego, boton["Dimensiones"])

    boton["Rectangulo"] = boton["Superficie"].get_rect()
    
    boton["Rectangulo"].topleft = boton["Posicion"]
    
    return boton

def dibujar(boton: dict):
    """
    Dibuja el boton.
    Args:
        boton (dict): Recibe el boton
    """
    try:
        # Verifica que la ventana esté activa antes de intentar blitear
        if boton["Ventana"]:
            boton["Ventana"].blit(boton["Superficie"], boton["Posicion"])
    except pygame.error as e:
        print("Error al intentar dibujar en la ventana:", e)
