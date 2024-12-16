import pygame

#Esta funcion crea los botones para los botones
#Recibe la ventana, la posicion, las dimensiones y como parametro opcional, fuente y el path de la imagen.
#Devuelve el boton
def crear_boton(ventana: str, posicion: int, dimensiones_boton: int, fuente: str = None, path_imagen: str = None) -> dict:
    boton = {}
    boton["Ventana"] = ventana #Surface
    boton["Posicion"] = posicion #Tupla
    boton["Dimensiones"] = dimensiones_boton #Tupla
    boton["Presionado"] = False

    if path_imagen != None:
        imagen_juego = pygame.image.load(path_imagen)
        boton["Superficie"] = pygame.transform.scale(imagen_juego, boton["Dimensiones"])
    else:
        pass

    boton["Rectangulo"] = boton["Superficie"].get_rect()
    
    boton["Rectangulo"].topleft = boton["Posicion"]
    
    return boton


#Esta funcion dibuja el boton, recibe el boton.
def dibujar(boton: dict):
    try:
        # Verifica que la ventana esté activa antes de intentar blitear
        if boton["Ventana"]:
            boton["Ventana"].blit(boton["Superficie"], boton["Posicion"])
    except pygame.error as e:
        print("Error al intentar dibujar en la ventana:", e)
