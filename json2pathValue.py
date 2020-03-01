# -*- coding: utf-8 -*-

import json
import os
import sys
import pandas as pd

#Iteración de claves y objetos y generación de diccionario path/valor
def flattenJSON(json):
    out = {}
    def flatten(json, name = ''):
        if type(json) is dict:
            #Recorrido de las claves del JSON en cada nivel de subordinación
            for key in json:
                #Llamada recursiva en la que "json" se corresponde con el valor de la clave y, si es un array se recorrerá
                flatten(json[key], name + key + '/')
        #Recorrido de array del JSON
        elif type(json) is list:
            i = 0
            for key in json:
                #Llamada recursiva en la que "json" se corresponde con el contenido de la posición "i" del array
                flatten(key, name + str(i) + '/')
                i += 1
        else:
            #Si el valor de "json" no se corresponde con una estructura JSON o un array del JSON, se almacena en la variable de salida (path + valor)
            out[name[:-1]] = json
    flatten(json)
    return out

#Main
#Lectura de fichero
if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as jsonFile:
        jsonData = json.load(jsonFile)
else:
    print("No existe el fichero " + sys.argv[1])

#Recorrido de los paths y valores del JSON
print("")
for key, value in flattenJSON(jsonData).items():
    print(key + ": " + str(value))

#Generacióon de dataframe con los datos del dict: cada nivel del path es una columna
df = pd.DataFrame(flattenJSON(jsonData).items(), columns = ['Path', 'Value'])
dfValue = df['Value']
df = pd.DataFrame(df.Path.str.split('/', expand = True))
df["Value"] = dfValue