import json

#Ruta absoluta del fichero JSON de entrada
filePath = "/home/gustavo/lista_sensores.json"
#Array con los campos a eliminar
filedsToSkip = ["location_id", "sensor_id"]

dataMod = {}
dataMod[filePath] = []
with open(filePath) as json_file:
    data = json.load(json_file)
    for record in data:
        for skipField in filedsToSkip:
            record.pop(skipField, None)
        dataMod[filePath].append(record)

print(dataMod)
with open(filePath + "_modified", 'w', encoding = 'utf8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)
