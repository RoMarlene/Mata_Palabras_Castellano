import time
from Funciones import *
from archivos import *
from Comodines import *
# Importamos la función desde 'juego.py'

# Ruta relativa al archivo CSV
palabras_csv = "Palabras.csv"  

# Llamar a la función para obtener la lista de palabras
diccionario_palabras = obtener_lista_palabras(palabras_csv)

#Esta funcion almacena un diccionario con variables estaticas y que se actualizan, retorna el diccionario
def inicializar_variables()-> dict:
    diccionario_juego = {
        "vidas": 3,
        "puntaje": 0,
        "tiempo": 60,
        "comodin_tiempo_disponible": True,
        "comodin_vida_disponible": True,
        "comodin_congelacion_disponible": True,
        "comodines_disponibles": 3,
        "tiempo_inicio": time.time(),
        "duracion_congelacion": 10,
        "tiempo_congelado": False,
        "tiempo_restante_congelacion": 0,
        "incremento_tiempo": 10
    }

    return diccionario_juego


estado_variables = inicializar_variables()

#Diccionario con los mensajes
diccionario_mensajes = {
    "mensaje_error": "Este comodin ya ha sido usado",
    "mensaje_error_general": "Ya no tenés más comodines :("
}
