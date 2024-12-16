import time
from datos import *

#Comodin tiempo, agrega 10 segundos al tiempo total
#Recibe como parametro el diccionario del juego, tiempo inicio, el incremento, el diccionario de mensajes y el mensaje comodin
#Retorna el mensaje dependiendo de la condición

def crear_comodin_tiempo(diccionario_juego, tiempo_inicio, incremento_tiempo, diccionario_mensajes, mensaje_comodin):
    tiempo_transcurrido = int(time.time() - tiempo_inicio)
    tiempo_restante = diccionario_juego["tiempo"] - tiempo_transcurrido

    # Verifica si el comodín está disponible
    if diccionario_juego["comodines_disponibles"] > 0 and diccionario_juego["comodin_tiempo_disponible"]:
        tiempo_restante += incremento_tiempo  
        diccionario_juego["tiempo"] = tiempo_restante
        mensaje = mensaje_comodin

        diccionario_juego["comodines_disponibles"] -= 1
        diccionario_juego["comodin_tiempo_disponible"] = False

    else:
        if diccionario_juego["comodin_tiempo_disponible"] == False:
            mensaje = diccionario_mensajes['mensaje_error']

    return mensaje

#Comodin vida extra, 1 vida extra
#Recibe como parametro el diccionario del juego, el diccionario de mensajes y el mensaje comodin
#Retorna el mensaje dependiendo de la condición
def crear_comodin_vida(diccionario_juego, diccionario_mensajes, mensaje_comodin):
    if diccionario_juego['comodines_disponibles'] > 0 and diccionario_juego['comodin_vida_disponible']:
        diccionario_juego['vidas'] += 1
        diccionario_juego['comodines_disponibles'] -= 1  
        diccionario_juego['comodin_vida_disponible'] = False
        mensaje = mensaje_comodin
    else:
        if diccionario_juego['comodin_vida_disponible'] == False:
            mensaje = diccionario_mensajes['mensaje_error']

    return mensaje

#Comodin congelacion, congela el tiempo por 10 segundos
#Recibe como parametro el diccionario del juego, el diccionario de mensajes y el mensaje comodin
#Retorna el mensaje dependiendo de la condición
def activar_comodin_congelacion(diccionario_juego, diccionario_mensajes, mensaje_comodin):
    if diccionario_juego['comodines_disponibles'] > 0:
        diccionario_juego['comodines_disponibles'] -= 1
        diccionario_juego['tiempo_congelado'] = True  
        diccionario_juego['tiempo_restante_congelacion'] = diccionario_juego["duracion_congelacion"]
        diccionario_juego['comodin_congelacion_disponible'] = False
        mensaje = mensaje_comodin
    else:
        if diccionario_juego['comodin_congelacion_disponible'] == False:
            mensaje = diccionario_mensajes['mensaje_error']
    return mensaje

#Esta función gestiona el tiempo congelado, utilizando el .get que accede al valor de una llave de un diccionario, si no existe, por default devuelve "None" o el valor que uno le ponga (En este caso, False). Verifica si el tiempo está congelado
#Recibe como parametro el diccionario de juego
#En este caso no devuelve nada, soolo printea un mensaje, siento la unica funcion que se printea ya que si retorna algo, rompe.
def gestionar_tiempo_congelado(diccionario_juego):
    if diccionario_juego.get("tiempo_congelado", False):
        diccionario_juego["tiempo_restante_congelacion"] -= 1
        if diccionario_juego["tiempo_restante_congelacion"] <= 0:
            diccionario_juego["tiempo_congelado"] = False
            print("El tiempo ha vuelto a correr.")

#Esta función genera los mensajes de los comodines, dependiendo del comodin, se muestra un mensaje.
#parametro_extra_uno y parametro_extra_dos  son utilizados para pasar información adicional
# que varía dependiendo de la acción del comodín.
#Parametro_uno es obligatorio en todos los casos ya que alacena mensajes clave de los comodines, 
#el numero dos, no, solo se utiliza en el tiempo
#recibe la accion, el parametro extra y como opcional el parametro dos.
#Retorna un mensaje dependiendo del caso
def generar_mensaje_comodin(accion, parametro_extra_uno, parametro_extra_dos=None):
    match accion:  
        case "vida":    
            mensaje = f"¡Comodín usado! Vida extra: 1. Vidas totales: {parametro_extra_uno}."
        case "tiempo":
                # Aseguramos que el tiempo total se muestre como un entero
            tiempo_total = int(parametro_extra_uno)  # Convertimos a entero
            mensaje = f"¡Comodín usado! Tiempo extra: {parametro_extra_dos} segundos. Tiempo total: {tiempo_total}."
        case "congelacion":
            mensaje = f"¡Comodín de congelación activado! Tiempo congelado por {parametro_extra_uno} segundos."
        
    return mensaje
