import json
import csv

#Esta función crea el archivo "Palabras.csv" y guarda las palabras.
#Recibe como parametro el diccionario de palabras.

def obtener_lista_palabras(palabras_csv: str) -> dict:
    diccionario_palabras = {
        "Faciles": {"Palabras": [], "Puntaje": 5},
        "Medias": {"Palabras": [], "Puntaje": 10},
        "Dificiles": {"Palabras": [], "Puntaje": 15}
    }

    try:
        with open(palabras_csv, mode='r', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo)
            es_primera_linea = True 
            
            for fila in lector_csv:
                if es_primera_linea:
                    es_primera_linea = False
                    continue  
                
                categoria = fila[0].strip()
                palabra = fila[1].strip()
                
                if categoria == 'Facil':
                    diccionario_palabras['Faciles']['Palabras'].append(palabra)
                elif categoria == 'Media':
                    diccionario_palabras['Medias']['Palabras'].append(palabra)
                elif categoria == 'Dificil':
                    diccionario_palabras['Dificiles']['Palabras'].append(palabra)

    except:
        print(f"Error: El archivo {palabras_csv} no se encontró.")

    return diccionario_palabras

#Esta función crea el archivo "Estadisticas.csv" y guarda el nombre, el puntaje, el tiempo y las vidas.
#Recibe como parametro los nombres, el puntaje, el tiempo y las vidas
def guardar_puntaje_json(nombre: str, puntaje: int, tiempo: int, vidas: int):
    datos = {
        "Nombre": nombre,
        "Puntaje": puntaje,
        "Tiempo": tiempo, 
        "Vidas": vidas
    }
    # usamos el try except , leemos el archivo y lo cargamos
    #  en el except devolvemos una lista vacia
    try:
        with open("Estadisticas.json", "r") as archivo:
            estadisticas = json.load(archivo)
    except:
        estadisticas = []
        
    estadisticas.append(datos)

# Leemos o creamos el archivo estadistica.json 
#  y con el dump escribimos directamente sobre el archivo
    with open("Estadisticas.json", "w") as puntaje_file:
        json.dump(estadisticas, puntaje_file, indent=4)