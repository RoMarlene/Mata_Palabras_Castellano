import time
from archivos import *
from datos import *
from Comodines import *
from os import system
from Funciones import *

# Ruta relativa al archivo CSV
palabras_csv = "Palabras.csv"  # Sube un nivel desde la carpeta actual para acceder al archivo

# Llamar a la función para obtener la lista de palabras
diccionario_palabras = obtener_lista_palabras(palabras_csv)

def usar_comodin(entrada_usuario, comodin_tiempo_disponible, comodin_vida_disponible, comodin_puntaje_disponible, 
                vidas, puntaje, tiempo_restante, incremento_tiempo, palabra_actual, tiempo_inicio):
    match entrada_usuario:
        case "t":
            if comodin_tiempo_disponible:
                # Generar mensaje y usar el comodín
                mensaje_comodin = generar_mensaje_comodin("tiempo", tiempo_restante, incremento_tiempo, comodin_usado=False)
                print(f"Tiempo restante antes del comodín: {tiempo_restante}")  # Debug
                comodines_disponibles, tiempo_restante, mensaje = crear_comodin_tiempo(comodines_disponibles, tiempo_restante, incremento_tiempo, mensaje_comodin, comodin_usado=False)
                print(f"Tiempo restante después del comodín: {tiempo_restante}")  # Debug
                tiempo_inicio = time.time()
                comodin_tiempo_disponible = False  # Desactivar el comodín de tiempo
                se_uso_comodin = True
                print(mensaje_comodin)
            else:
                mensaje_error = generar_mensaje_comodin("tiempo", tiempo_restante, incremento_tiempo, comodin_usado=True)
                print(mensaje_error)
        case "v":
            if comodin_vida_disponible:
                mensaje_comodin = generar_mensaje_comodin("vida", vidas + 1, comodin_usado=False)
                vidas, comodines_disponibles, mensaje = crear_comodin_vida(comodines_disponibles, vidas, mensaje_comodin)
                comodin_vida_disponible = False  # Desactivar el comodín de vida
                se_uso_comodin = True
                print(mensaje)
            else:
                mensaje_error_vida = generar_mensaje_comodin("vida", vidas + 1, comodin_usado=True)
                print(mensaje_error_vida)
        case "c":
            if comodin_puntaje_disponible:
                categoria = obtener_categoria(palabra_actual["Palabra"], diccionario_palabras)
                puntaje_extra = calcular_puntaje_extra(puntaje, comodin_puntaje_activado, categoria)
                mensaje_comodin = generar_mensaje_comodin("puntaje", 0, 0, comodin_usado=False)
                comodines_disponibles, puntaje, mensaje_comodin, comodin_puntaje_activado = crear_comodin_puntaje(comodines_disponibles, puntaje, mensaje_comodin, comodin_puntaje_activado, palabra_actual['Palabra'], diccionario_palabras, puntaje_extra)
                comodin_puntaje_disponible = False  # Desactivar el comodín de puntaje
                se_uso_comodin = True
                print(mensaje_comodin)
            else:
                mensaje_error_puntaje = generar_mensaje_comodin("puntaje", 0, 0, comodin_usado=True)
                print(mensaje_error_puntaje)
        case _:
            # Nunca debería llegar aquí, pero lo manejamos por seguridad.
            print("Entrada inválida para comodín.")
    return se_uso_comodin, comodin_tiempo_disponible, comodin_puntaje_disponible, comodin_vida_disponible, comodines_disponibles, vidas, puntaje, tiempo_restante

def crear_juego(vidas: int, puntaje: int, tiempo: int):
    # Declaramos las variables y banderas
    comodin_tiempo_disponible = True
    comodin_vida_disponible = True
    comodin_puntaje_disponible = True
    comodines_disponibles = 3
    incremento_tiempo = 10
    tiempo_inicio = time.time()
    se_uso_comodin = False

    while vidas > 0:

        tiempo_restante = crear_temporizador(tiempo_inicio, tiempo)
        tiempo_usado = tiempo - tiempo_restante  # Calcula el tiempo real transcurrido

        if tiempo_restante <= 0:
            print("¡Se acabó el tiempo!")
            tiempo_usado = 0  # O puedes actualizar el tiempo de alguna forma si es necesario
            break

        system('cls') 
        print(f"Vidas: {vidas} | Puntaje: {puntaje} | Tiempo restante: {tiempo_restante} segundos")
        print(f"Comodines disponibles: {comodines_disponibles}")

        palabra_actual = obtener_palabra(tiempo_restante, diccionario_palabras)
        print(f"Escribí esta palabra: {palabra_actual['Palabra']}")

        entrada_usuario = input("""Tu respuesta: 
        (O escribí "T" para obtener Tiempo extra,
        "V" para vidas extras o "C" para multiplicar puntaje de una palabra): """).strip().lower()


        palabra_valida = ingresar_y_validar_palabra(diccionario_palabras, entrada_usuario)

        print(f"Entrada usuario: {entrada_usuario}")
        print(f"Palabra correcta: {palabra_actual['Palabra'].lower()}")

        if entrada_usuario == "T" or entrada_usuario == "V" or entrada_usuario == "C":  # Si el usuario intenta usar un comodín
            if comodines_disponibles == 0:
                mostrar_comodin()
                continue
            else:
                se_uso_comodin = usar_comodin(entrada_usuario, comodin_tiempo_disponible, comodin_vida_disponible, comodin_puntaje_disponible, 
                vidas, puntaje, tiempo_restante, incremento_tiempo, palabra_actual, tiempo_inicio) # ACÁ PONES LOS PARÁMETROS NECESARIOS
                time.sleep(1)

        if palabra_valida:
            # Palabra válida
            print("¡Correcto!")
            puntaje = calcular_puntaje(diccionario_palabras, puntaje, palabra_actual['Palabra'])
            print(f"Puntaje actual: {puntaje}")  # Mostrar el puntaje actualizado
            time.sleep(1)
        elif se_uso_comodin:
            # Comodines
            comodin_tiempo_disponible, comodin_puntaje_disponible, comodin_vida_disponible, 
            comodines_disponibles, vidas, puntaje, tiempo_restante = usar_comodin(entrada_usuario, comodin_tiempo_disponible, comodin_vida_disponible, 
                                                                    comodin_puntaje_disponible, 
vidas, puntaje, tiempo_restante, incremento_tiempo, palabra_actual, tiempo_inicio) # FALTA PARÁMETROS
            se_uso_comodin = False
        else:
            # Entrada incorrecta y no es un comodín
            print("¡Incorrecto!")
            mensaje, vidas = restar_vidas(vidas)
            print(mensaje)
            time.sleep(1)

            if vidas == 0:
                print("¡Perdiste alpiste! Te quedaste sin vidas, termina el juego.")

    # Aquí guardamos el puntaje, el tiempo real usado y las vidas
    nombre = input("Ingresá tu nombre para guardar el puntaje: ")
    guardar_puntaje_json(nombre, puntaje, tiempo_usado, vidas)
    mostrar_estadistica = f"Nombre: {nombre},\n Puntaje: {puntaje},\n Tiempo: {tiempo_usado},\n Vidas: {vidas}"
    print(f"¡Nombre guardado! Gracias por jugar. :)\n {mostrar_estadistica}")

system('pause')
system('cls')