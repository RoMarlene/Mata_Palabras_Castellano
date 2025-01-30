import json
import csv

"""_summary_

Args:
    palabras_csv (str): Recibe el csv de las palabras pasado a una variable.

Returns:
    dict: Retorna dicho diccionario de palabras 
"""
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


"""_summary_

Args:
    nombre (str): Nombre que pondrá el usuario.
    puntaje (int): Puntaje del usuario.
    tiempo (int): El tiempo del usuario.
    vidas (int): Las vidas del usuario.
"""
def guardar_puntaje_json(nombre: str, puntaje: int, tiempo: int, vidas: int):
    datos = {
        "Nombre": nombre,
        "Puntaje": puntaje,
        "Tiempo": tiempo, 
        "Vidas": vidas
    }

    try:
        with open("Estadisticas.json", "r") as archivo:
            estadisticas = json.load(archivo)
    except:
        estadisticas = []
        
    estadisticas.append(datos)

    with open("Estadisticas.json", "w") as puntaje_file:
        json.dump(estadisticas, puntaje_file, indent=4)