import time
from archivos import *
#from Datos import *
from Comodines import *
from os import system
from Funciones import *

#inicializamos variables y banderas
vidas = 3
puntaje = 0
tiempo = 60
comodin_tiempo = False
# Ruta relativa al archivo CSV
palabras_csv = "Palabras.csv"  # Sube un nivel desde la carpeta actual para acceder al archivo

# Llamar a la función para obtener la lista de palabras
diccionario_palabras = obtener_lista_palabras(palabras_csv)

def crear_juego(vidas: int, puntaje: int, tiempo: int): 
    comodin_tiempo_disponible = True
    comodin_vida_disponible = True
    comodin_congelacion_disponible = True
    duracion_congelacion = 10
    comodines_disponibles = 3
    incremento_tiempo = 10


    tiempo_inicio = time.time()
    tiempo_restante = tiempo  
    while vidas > 0 and tiempo_restante > 0:

        tiempo_actual = time.time()  
        tiempo_usado = tiempo_actual - tiempo_inicio  
        tiempo_restante = tiempo - tiempo_usado 
       # tiempo_usado = tiempo - tiempo_restante  # Calcula el tiempo real transcurrido

        if tiempo_restante <= 0:
            print("¡Se acabó el tiempo!")
            break
        #system('cls') 
        print(f"Vidas: {vidas} | Puntaje: {puntaje} | Tiempo restante: {tiempo_restante} segundos")
        print(f"Comodines disponibles: {comodines_disponibles}")

        # tiempo_restante += tiempo_inicio - tiempo_total # Esto debería actualizar tiempo_restante
        palabra_actual = obtener_palabra(int(tiempo_restante), diccionario_palabras)
        print(f"Escribí esta palabra: {palabra_actual['Palabra']}")

        entrada_usuario = input("""Tu respuesta: 
        (O escribí "T" para obtener Tiempo extra,
        "V" para vidas extras o "C" para congelar el tiempo): """).strip().lower()

        if entrada_usuario == "t":  # Comodín para tiempo extra
            if comodin_tiempo_disponible:
                tiempo_restante += incremento_tiempo
                comodin_tiempo_disponible = False
                print(f"¡Tiempo extra añadido! Tiempo restante: {int(tiempo_restante)} segundos.")
            else:
                print("Ya usaste el comodín de tiempo.")  # Mensaje cuando ya no hay comodines disponibles
                continue
    
            # time.sleep(1)  # Pausa antes de continuar con la siguiente palabra
            # continue  
        elif entrada_usuario == "v":  # Comodín para vidas extras
            if comodin_vida_disponible:
                vidas += 1
                comodin_vida_disponible = False
                print(mensaje)
            else:
                print("Ya usaste el comodín de vidas.")
            continue


        elif entrada_usuario == "c":  # Comodín para congelar el tiempo
            if comodin_congelacion_disponible:
                tiempo_inicio, comodines_disponibles, mensaje = crear_comodin_congelacion(tiempo_inicio, comodines_disponibles, duracion_congelacion)
                comodin_congelacion_disponible = False
                print(mensaje)
            else:
                print(comodin_usado_mensaje())  # Mensaje cuando ya no hay comodines disponibles
            continue

        # Si no es un comodín, se espera una palabra
        palabra_valida = ingresar_y_validar_palabra(diccionario_palabras, entrada_usuario)

        if palabra_valida:  # Si la palabra es válida, mostramos el mensaje de "Correcto"
            print("¡Correcto!")
            puntaje = calcular_puntaje(diccionario_palabras, puntaje, palabra_actual['Palabra'])
            print(f"Puntaje actual: {puntaje}")
            time.sleep(1)  # Pausa antes de continuar con la siguiente palabra

        else:  # Si la palabra no es válida, mostramos el mensaje de "Incorrecto"
            print("¡Incorrecto!")  # Mensaje para palabras incorrectas
            mensaje, vidas = restar_vidas(vidas)  # Restar vidas si la palabra es incorrecta
            print(mensaje)  # Mostrar el mensaje del restado de vidas

            # Si no quedan vidas, termina el juego
            if vidas == 0:
                time.sleep(1)  # Pausa antes de salir
                break  # Salir del ciclo si se quedan sin vidas

        time.sleep(1)  # Pausa antes de mostrar la siguiente palabra

    # Aquí guardamos el puntaje, el tiempo real usado y las vidas
    nombre = input("Ingresá tu nombre para guardar el puntaje: ")
    guardar_puntaje_json(nombre, puntaje, tiempo_usado, vidas)
    print("¡Nombre guardado! Gracias por jugar. :)")

system('pause')
system('cls')




