import pygame

#Esta funcion crea la linea de colisiones, recibe la ventana, el inicio de lalinea, el final de la linea
#el grosor de la linea y el color.
#retorna la linea 
def crear_linea(ventana: pygame.Surface, inicio_linea:tuple, final_linea:tuple, grosor: int, color: tuple)-> dict:
    """_summary_

    Args:
        ventana (pygame.Surface): La ventana
        inicio_linea (tuple): El inicio de la linea
        final_linea (tuple): El final de la linea
        grosor (int): El grosor de la linea
        color (tuple): El color de la linea.

    Returns:
        dict: La linea
    """
    linea = {}
    linea["Ventana"] = ventana
    linea["Inicio"] = inicio_linea  #Tupla de coordenadas (x1, y1)
    linea["Final"] = final_linea   #Tupla de coordenadas (x2, y2)
    linea["Grosor"] = grosor
    linea["Color"] = color

    return linea

# Esta funcion dibuja la línea con las coordenadas de inicio y fin
def dibujar_linea(linea):
    """
    Dibuja la linea en si

    """
    pygame.draw.line(linea["Ventana"], linea["Color"], linea["Inicio"], linea["Final"], linea["Grosor"])

#Esta funcion crea texto.
def crear_texto(ventana, mensaje, fuente="Arial", tamano=30, color=(255, 255, 255), posicion=(0, 0)):
    """Crea la linea"""
    fuente_objeto = pygame.font.SysFont(fuente, tamano)
    texto_superficie = fuente_objeto.render(mensaje, True, color)
    ventana.blit(texto_superficie, posicion)

