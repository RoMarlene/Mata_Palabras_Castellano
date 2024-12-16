import pygame

#Esta funcion crea la linea de colisiones, recibe la ventana, el inicio de lalinea, el final de la linea
#el grosor de la linea y el color.
#retorna la linea 
def crear_linea(ventana, inicio_linea: tuple, final_linea:tuple, grosor: int, color: tuple):
    linea = {}
    linea["Ventana"] = ventana
    linea["Inicio"] = inicio_linea  #Tupla de coordenadas (x1, y1)
    linea["Final"] = final_linea   #Tupla de coordenadas (x2, y2)
    linea["Grosor"] = grosor
    linea["Color"] = color

    return linea

# Esta funcion dibuja la línea con las coordenadas de inicio y fin
def dibujar_linea(linea):
    pygame.draw.line(linea["Ventana"], linea["Color"], linea["Inicio"], linea["Final"], linea["Grosor"])

#Esta funcion crea texto.
def crear_texto(ventana, mensaje, fuente="Arial", tamano=30, color=(255, 255, 255), posicion=(0, 0)):
    fuente_objeto = pygame.font.SysFont(fuente, tamano)
    texto_superficie = fuente_objeto.render(mensaje, True, color)
    ventana.blit(texto_superficie, posicion)

