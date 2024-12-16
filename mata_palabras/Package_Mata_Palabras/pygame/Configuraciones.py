import pygame

# Función para controlar el volumen
#Recibe los eventos, el volumen y la imagen del icono
#Devuelve una tupla de volumen y mostrar_icono
def ajustar_volumen(eventos: any, volumen: int, imagen_icono: str)-> tuple:
    mostrar_icono = False
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:  # Flecha arriba
                volumen += 0.1
                if volumen > 1.0:  # No puede exceder el volumen máximo
                    volumen = 1.0
                pygame.mixer.music.set_volume(volumen)
                mostrar_icono = True
            elif evento.key == pygame.K_DOWN:  # Flecha abajo
                volumen -= 0.1
                if volumen < 0.0:  # No puede ser menor que el volumen mínimo
                    volumen = 0.0
                pygame.mixer.music.set_volume(volumen)
                mostrar_icono = True

    return volumen, mostrar_icono

#Esta funcion devuelve el icono del volumen cuando es necesario.
#Recibe la ventana, la imagen del icono y el icono.
def mostrar_icono_volumen(ventana: str, imagen_icono:str, mostrar_icono:str):
    if mostrar_icono:
        ventana.blit(imagen_icono, (10, 10))
