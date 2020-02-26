# -*- coding: utf-8 -*-
#Obtención de los valores de parámetros de BB.DD. de Cloudera a partir de llamada a la API

import os
import sys
import json

#URL base
urlBase = "http://localhost:7180"

#Version de la API
apiRelease = "v13"

#Petición a API a través de curl, sólo GET
def execCurl(url):
	headers = " -H 'Content-type: application/json' -H 'Accept-Charset: UTF-8'"
	cmdGet = "curl -k -sS -X GET -u " + "'" + userCDH + ":" + passCDH + "' " + urlBase + "/api/" + apiRelease + url + " 2>/dev/null"
	try:
		return json.loads(os.popen(cmdGet).read())
	except:
		print("No ha sido posible realizar la peticion " + url)
		sys.exit()

##Main
#Solicitud de credenciales de usuario administrador de Cloudera Manager
userCDH = raw_input("Introducir el nombre de usuario administrador de Cloudera Manager: ")
passCDH = raw_input("Introducir la password del usuario " + userCDH + ": ")

#Obtención y recorrido del JSON con la configuración y output de los parámetros
json = execCurl("/cm/deployment")
for n1 in json["clusters"]:
	for n2 in n1["services"]:
		data = 0
		print n2["displayName"]
		for n3 in n2["config"]["items"]:
			if "database" in n3["name"]:
				data += 1
				print "\t" + n3["name"] + ": " + n3["value"]
		for n4 in n2["roleConfigGroups"]:
			for n5 in n4["config"]["items"]:
				if "database" in n5["name"]:
					data += 1
					print "\t" + n5["name"] + ": " + n5["value"]	
		if data == 0:
			print "\tN/A"
for n1 in json["managementService"]["roleConfigGroups"]:
	data = 0
	print n1["displayName"]
	for n2 in n1["config"]["items"]:
		if "database" in n2["name"]:
			data += 1
			print "\t" + n2["name"] + ": " + n2["value"]
	if data == 0:
		print "\tN/A"

