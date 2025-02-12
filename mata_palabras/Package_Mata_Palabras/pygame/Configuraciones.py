import pygame

def ajustar_volumen(eventos: any, volumen: int)-> tuple:
    """Crea la configuracion del volumen, para subirlo y bajarlo con el teclado

    Args:
        eventos (any): Los eventos
        volumen (int): El volumen

    Returns:
        tuple: Devuelve el volumen "nuevo" y muestra el icono del volumen
    """
    mostrar_icono = False
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                volumen += 0.1
                if volumen > 1.0:  # No puede exceder el volumen máximo
                    volumen = 1.0
                pygame.mixer.music.set_volume(volumen)
                mostrar_icono = True
            elif evento.key == pygame.K_DOWN:
                volumen -= 0.1
                if volumen < 0.0:  # No puede ser menor que el volumen mínimo
                    volumen = 0.0
                pygame.mixer.music.set_volume(volumen)
                mostrar_icono = True

    return volumen, mostrar_icono

def mostrar_icono_volumen(ventana: str, imagen_icono:str, mostrar_icono:str):
    """Muestra el icono del volumen

    Args:
        ventana (str): La ventana.
        imagen_icono (str): Imagen del icono.
        mostrar_icono (str): El icono en si.
    """
    if mostrar_icono:
        ventana.blit(imagen_icono, (10, 10))