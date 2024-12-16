from botones import crear_boton, dibujar
from Configuraciones import ajustar_volumen, mostrar_icono_volumen
from Datos_juego import datos, DIMENSIONES_PANTALLA, imagenes, sonidos, boton_sonido
from juego_pantalla import ventana_juego
from menu_principal import crear_menu_principal
from puntuacion import cargar_puntuaciones, ventana_puntuacion, mostrar_puntuaciones
from Inicio import crear_inicio_juego
from Final import crear_final

pantallas = {
    "menu": crear_menu_principal,
    "juego": ventana_juego,
    "puntuacion": ventana_puntuacion,
    "inicio": crear_inicio_juego,
    "final": crear_final
}

__all__ = [
    "crear_boton",
    "dibujar",
    "ajustar_volumen",
    "mostrar_icono_volumen",
    "datos",
    "DIMENSIONES_PANTALLA",
    "imagenes",
    "sonidos",
    "boton_sonido",
    "ventana_juego",
    "crear_menu_principal",
    "cargar_puntuaciones",
    "ventana_puntuacion",
    "mostrar_puntuaciones",
    "crear_inicio_juego",
    "pantallas"
]