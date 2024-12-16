import pygame
from Datos_juego import imagenes, sonidos, DIMENSIONES_PANTALLA

def crear_inicio_juego():
    pygame.init()
    pygame.mixer.init()

    ventana_inicio = pygame.display.set_mode(DIMENSIONES_PANTALLA)
    pygame.display.set_caption("Inicio")

    imagen_inicio = pygame.image.load(imagenes["Fondo_inicio"])

    sonido_inicio = pygame.mixer.Sound(sonidos["sonido_inicio"])
    sonido_inicio.play(loops=-1)

    fuente_inicio = pygame.font.SysFont("Arial", 30)
    texto_inicio = fuente_inicio.render("Presiona ENTER para empezar el juego", True, (255, 255, 255))

    siguiente_pantalla = "inicio"

    bandera_inicio = True
    while bandera_inicio:
        ventana_inicio.blit(imagen_inicio, (0, 0))
        ventana_inicio.blit(texto_inicio, (183, 531))


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                siguiente_pantalla = "salir"
                bandera_inicio = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    siguiente_pantalla = "juego"
                    bandera_inicio = False
                    sonido_inicio.stop()

        pygame.display.update()


    return siguiente_pantalla