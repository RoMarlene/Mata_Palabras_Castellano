import pygame
from juego_pantalla import ventana_juego
from Menu_principal import crear_menu_principal
from Puntuacion import ventana_puntuacion
from Inicio import crear_inicio_juego
from Final import crear_final

# Diccionario de pantallas
pantallas = {
    "menu": crear_menu_principal,
    "juego": ventana_juego,
    "puntuacion": ventana_puntuacion,
    "inicio": crear_inicio_juego,
    "final": crear_final,
}

# Función que ejecuta la pantalla actual
def ejecutar_pantalla(pantalla_actual):
    funcion = pantallas.get(pantalla_actual)
    if funcion:
        return funcion()

# Bucle principal
def main():
    pygame.init()
    pantalla_actual = "menu"
    while pantalla_actual != "salir":
        pantalla_actual = ejecutar_pantalla(pantalla_actual)
    pygame.quit()

main()