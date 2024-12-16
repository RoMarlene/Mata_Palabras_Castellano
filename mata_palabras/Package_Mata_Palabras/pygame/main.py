import pygame
from Modulo_central import pantallas

# Función que ejecuta la pantalla actual
def ejecutar_pantalla(pantalla_actual):
    funcion = pantallas.get(pantalla_actual)
    if funcion:
        return funcion()

# Bucle principal
pantalla_actual = "menu"
while pantalla_actual != "salir":
    pantalla_actual = ejecutar_pantalla(pantalla_actual)

pygame.quit()