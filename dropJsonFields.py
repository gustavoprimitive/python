# -*- coding: utf-8 -*-
#Procesado de un fichero JSON para eliminar atributos
#Gustavo Tejerina

import json

#Ruta absoluta del fichero JSON de entrada
filePath = "/home/gustavo/lista_sensores.json"
#Array con los campos a eliminar
filedsToSkip = ["location_id", "sensor_id"]

with open(filePath, encoding = 'utf8') as json_file:
    data = json.load(json_file, encoding = 'utf8')
    #Eliminación de campos del JSON
    for record in data:
        for skipField in filedsToSkip:
            record.pop(skipField, None)

#Output
print(json.dumps(data, indent = 2, ensure_ascii = False))
