import time
from archivos import *
from datos import *
from Comodines import *
from os import system
from Funciones import *

#Funcion del juego
def crear_juego():
    estado_variables = inicializar_variables()
    estado_variables["tiempo_inicio"] = time.time()

    while estado_variables["vidas"] > 0:
        system('cls')

        tiempo_usado = int(time.time() - estado_variables["tiempo_inicio"])  # Tiempo total transcurrido

        gestionar_tiempo_congelado(estado_variables)

        if estado_variables["tiempo_congelado"] == False:
            tiempo_usado = int(time.time() - estado_variables["tiempo_inicio"])  # Tiempo total transcurrido
            if estado_variables["tiempo"] - tiempo_usado > 0:
                estado_variables["tiempo"] -= tiempo_usado
            else:
                estado_variables["tiempo"] = 0

        # Actualiza la hora de inicio para la siguiente iteración
        estado_variables["tiempo_inicio"] = time.time()



        print(f"Vidas: {estado_variables['vidas']} | Puntaje: {estado_variables['puntaje']} | Tiempo restante: {estado_variables['tiempo']} segundos")
        print(f"Comodines disponibles: {estado_variables['comodines_disponibles']}")

        # Obtener palabra actual
        palabra_actual = obtener_palabra(estado_variables["tiempo"], diccionario_palabras)
        print(f"Escribí esta palabra: {palabra_actual['Palabra']}")

        # Entrada del usuario
        entrada_usuario = input("""Tu respuesta: 
        (O escribí "T" para obtener Tiempo extra,
        "V" para vidas extras o "C" para congelar el tiempo ): """).strip().lower()

        match entrada_usuario:
            case "t":  
                mensaje_tiempo = generar_mensaje_comodin("tiempo", estado_variables["tiempo"], estado_variables["incremento_tiempo"])

                mensaje_resultado = crear_comodin_tiempo(estado_variables,  
                estado_variables["tiempo_inicio"],  
                estado_variables["incremento_tiempo"],
                diccionario_mensajes,  
                mensaje_tiempo) 
                
                print(mensaje_resultado)
                time.sleep(1)
                continue

            case "v":  
                mensaje_vidas = generar_mensaje_comodin("vida", estado_variables["vidas"] +1)
                mensaje_comodin_vidas = crear_comodin_vida(estado_variables, diccionario_mensajes, mensaje_vidas)
                print(mensaje_comodin_vidas)
                time.sleep(1)
                continue

            case "c":  
                mensaje_congelacion = generar_mensaje_comodin("congelacion", estado_variables["duracion_congelacion"])
                mensaje_comodin_congelacion = activar_comodin_congelacion(estado_variables, diccionario_mensajes, mensaje_congelacion)
                print(mensaje_comodin_congelacion)
                time.sleep(1)
                continue

            case _:  
                palabra_valida = ingresar_y_validar_palabra(diccionario_palabras, entrada_usuario)
                if palabra_valida:
                    # Palabra válida
                    estado_variables["puntaje"] = calcular_puntaje(diccionario_palabras, estado_variables["puntaje"], entrada_usuario)
                    print("¡Correcto!")
                else:
                    mensaje, estado_variables["vidas"] = restar_vidas(estado_variables["vidas"])
                    print(mensaje)

        time.sleep(1)
        if estado_variables['comodines_disponibles'] == 0:
            mensaje = diccionario_mensajes['mensaje_error_general']
            time.sleep(1)  
            break
        if estado_variables['vidas'] == 0:
                time.sleep(1)  
                break

        if estado_variables['tiempo'] == 0:
            print("¡Se acabó el tiempo!")
            break
    #Después de terminar el juego, preguntar si el jugador desea jugar de nuevo
    nombre = input("Ingresá tu nombre para guardar el puntaje: ")
    guardar_puntaje_json(nombre, estado_variables["puntaje"], estado_variables["tiempo"], estado_variables["vidas"])

        #Mostrar estadísticas finales
    mostrar_estadistica = f"Nombre: {nombre},\nPuntaje: {estado_variables['puntaje']},\nTiempo: {estado_variables['tiempo']} segundos,\nVidas: {estado_variables['vidas']}" #Guardar estadísticas
    print(f"¡Nombre guardado! Gracias por jugar. :)\n{mostrar_estadistica}")
    seguir = input("¿Deseas jugar otra vez? (si/no): ").strip().lower() 
    if seguir == "si":
        crear_juego()  # Llamada recursiva para volver a empezar el juego
            #Guardar estadísticas

        #Pausar y limpiar pantalla
        system('pause')
        system('cls')

