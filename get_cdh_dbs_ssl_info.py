# -*- coding: utf-8 -*-
#Obtención de los valores de parámetros de BB.DD. y SSL de Cloudera a partir de llamada a la API

import os
import sys
import json

#URL base
urlBase = "https://localhost:7183"

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
#Servicios del cluster exceptuando CMS
for n1 in json["clusters"]:
	print "\nCluster: " + n1["displayName"]
	for n2 in n1["services"]:
		dataDB = dataSSL = 0
		print "Servicio: " + n2["displayName"]
		for n3 in n2["config"]["items"]:
			if "database" in n3["name"]:
				if dataDB == 0:
					print "\t- Database"
				dataDB += 1
				print "\t\t" + n3["name"] + ": " + n3["value"]
			if "ssl" in n3["name"]:
				if dataSSL == 0:
					print "\t- SSL"
				dataSSL += 1
				print "\t\t" + n3["name"] + ": " + n3["value"]
		for n4 in n2["roleConfigGroups"]:
			for n5 in n4["config"]["items"]:
				if "database" in n5["name"]:
					if dataDB == 0:
						 print "\t- Database"
					dataDB += 1
					print "\t\t" + n5["name"] + ": " + n5["value"]
				if "ssl" in n5["name"]:
					if dataSSL == 0:
						print "\t- SSL"
					dataSSL += 1
				 	print "\t\t" + n5["name"] + ": " + n5["value"]
		if dataDB + dataSSL == 0:
			print "\tN/A"
#Servicio CMS
for n1 in json["managementService"]["roleConfigGroups"]:
	dataDB = 0
	print "Rol: " + n1["displayName"]
	for n2 in n1["config"]["items"]:
		if "database" in n2["name"]:
			if dataDB == 0:
				print "\t- Database"
			dataDB += 1
			print "\t\t" + n2["name"] + ": " + n2["value"]
	if dataDB == 0:
		print "\tN/A"
print "Servicio: " + json["managementService"]["name"]
if len(json["managementService"]["config"]["items"]) > 0:
	print "\t- SSL"
for n1 in json["managementService"]["config"]["items"]:
	dataSSL = 0
	if "ssl" in n1["name"]:
		dataSSL += 1
		print "\t\t" + n1["name"] + ": " + n1["value"]
if dataSSL == 0:
	print "\tN/A"
#Roles de CMS
for n1 in json["managementService"]["roles"]:
	dataSSL = 0
	print "Rol: " + n1["name"]
	for n2 in n1["config"]["items"]:
		if "ssl" in n2["name"]:
			if dataSSL == 0:
				print "\t- SSL"
			dataSSL += 1
			print "\t\t" + n2["name"] + ": " + n2["value"]
	if dataSSL == 0:
		print "\tN/A"

