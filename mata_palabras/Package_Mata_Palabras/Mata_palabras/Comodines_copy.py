import time
from datos import *
#Comodin tiempo, agrega 10 segundos al tiempo total
#Recibe como parametro los comodines disponibles, el tiempo total y el incremento tiempo
#Retorna una tupla que contiene los comodines disponibles, tiempo total y el mensaje
def crear_comodin_tiempo(diccionario_juego: dict, tiempo_inicio: int, incremento_tiempo: int)-> str:
    tiempo_transcurrido = int(time.time() - tiempo_inicio)
    tiempo_restante = diccionario_juego["tiempo"] - tiempo_transcurrido
    
    # Verifica si el comodín está disponible
    if diccionario_juego["comodines_disponibles"] > 0 and diccionario_juego["comodin_tiempo_disponible"]:
        tiempo_restante += incremento_tiempo  # Agregar tiempo extra
        diccionario_juego["comodines_disponibles"] -= 1  # Reducir comodines disponibles
        diccionario_juego["comodin_tiempo_disponible"] = False  # Marcar como usado

        mensaje = f"¡Comodín usado! Tiempo extra: {incremento_tiempo} segundos. | Tiempo restante: {tiempo_restante} segundos."
    else:
        # Mensajes diferentes dependiendo de la disponibilidad de comodines
        if diccionario_juego["comodin_tiempo_disponible"] == False:
            mensaje = "¡Ya has usado este comodín!"
        else:
            mensaje = "No hay comodines disponibles :("
    # Actualiza el tiempo restante en el diccionario
    diccionario_juego["tiempo"] = tiempo_restante
    return mensaje


def crear_comodin_vida(diccionario_juego: dict)-> str:
    if diccionario_juego['comodines_disponibles'] > 0 and diccionario_juego['comodin_vida_disponible']:
        diccionario_juego['vidas'] += 1  # Incrementar vidas
        diccionario_juego['comodines_disponibles'] -= 1  # Reducir comodines disponibles
        diccionario_juego['comodin_vida_disponible'] = False
        mensaje = f"¡Comodín usado! Vida obtenida: 1 | vidas actuales: {diccionario_juego['vidas']}"
    else:
        if diccionario_juego['comodin_vida_disponible'] == False:
            mensaje = "¡Ya has usado este comodín!"
        else:
            mensaje = "No hay comodines disponibles :("

    return mensaje

#

def activar_comodin_congelacion(diccionario_juego: dict):
    if diccionario_juego['comodines_disponibles'] > 0:
        diccionario_juego['comodines_disponibles'] -= 1  # Reducir comodines disponibles
        diccionario_juego['tiempo_congelado'] = True  # Activar congelación del tiempo
        diccionario_juego['tiempo_restante_congelacion'] = diccionario_juego["duracion_congelacion"]  # Duración del congelamiento
        diccionario_juego['comodin_congelacion_disponible'] = False
        mensaje = f"¡Tiempo congelado por {diccionario_juego['duracion_congelacion']} segundos!"
    else:
        if diccionario_juego['comodin_congelacion_disponible'] == False:
            mensaje = "¡Ya has usado este comodín!"
        else:
            mensaje = "No hay comodines disponibles :("

    
    return mensaje

def gestionar_tiempo_congelado(diccionario_juego: dict):
    if diccionario_juego.get("tiempo_congelado", False):  # Verificar si el tiempo está congelado
        diccionario_juego["tiempo_restante_congelacion"] -= 1  # Reducir el tiempo de congelación
        if diccionario_juego["tiempo_restante_congelacion"] <= 0:
            diccionario_juego["tiempo_congelado"] = False  # Desactivar la congelación
            print("El tiempo ha vuelto a correr.")