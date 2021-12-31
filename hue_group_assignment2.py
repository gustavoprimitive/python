# -*- coding: utf-8 -*-
#Gestión de usuarios de Hue: asignación de usuario a grupos y de permisos a grupos
#Gustavo Tejerina

import os
import sys
import re
import logging

dbName = "hue"

#Usage
def usage():
	print("\nUsage:")
	print("\tpython " + os.path.basename(__file__) + " -u <user> <groups>")
	print("\tpython " + os.path.basename(__file__) + " -a <app> <permission> <groups>\n")
	print("\tLos grupos deben estar separados por comas\n")
	return

#Ejecución de sentencia
def execPSQL(commandType, sql):
	skelPSQL = "psql -t -d " + dbName + " -c "
	try:
		log.debug("SQL:\t" + sql)
		if commandType == "show":
			sqlResult = os.popen(skelPSQL + '"' + sql + '"' + " 2>/dev/null").read()
			log.info("Sentencia ejecutada\t...OK")
			return sqlResult.split()
		else:
			os.system(skelPSQL + '"' + sql + '"' + " 2>/dev/null")
			log.info("Sentencia ejecutada\t...OK")
	except:
		log.error("No ha sido posible ejecutar la sentencia en PostgreSQL")
		sys.exit()
	
#Obtención de ID de usuario	
def getUserId(username):
	log.info("Obteniendo ID del usuario " + username)
	sql = "select id from auth_user where username = " + "'" + username + "'"
	return execPSQL("show", sql)
	
#Obtención de ID de grupo	
def getGroupId(groupname):
	log.info("Obteniendo ID del grupo " + groupname)
	sql = "select id from auth_group where name = " + "'" + groupname + "'"
	return execPSQL("show", sql)
	
#Obtención de los grupos de un usuario
def getUserGroupRel(userId):
	log.info("Obteniendo los nombres de los grupos del usuario con ID " + str(userId))
	sql = "select ag.name from auth_user_groups aug inner join auth_group ag on aug.group_id = ag.id where user_id = " + userId
	return execPSQL("show", sql)
	
#Obtención de ID de un un permiso de aplicación
def getHueId(app, permission):
	log.info("Obteniendo ID de permiso " + permission + " de la aplicacion " + app)
	sql = "select id from useradmin_huepermission where app = " + "'" + app + "'" + " and action = " + "'" + permission + "'"
	return execPSQL("show", sql)
	
#Obtención de los grupos que poseen un permiso de aplicación determinada
def getGroupAppRel(hueId):
	log.info("Obteniendo los nombres de los grupos asociados al permiso " + hueId)
	sql = "select ag.name from useradmin_grouppermission ug inner join auth_group ag on ug.group_id = ag.id where hue_permission_id = " + hueId
	return execPSQL("show", sql)

#Inserción de registro de asociación usuario/grupo	
def createUserGroupRel(userId, groupId):
	log.info("Generando la relacion entre el usuario " + userId + " y el grupo " + groupId)
	sql = "insert into auth_user_groups(user_id, group_id) values(" + userId + "," + groupId + ")"
	return execPSQL("exec", sql)

#Inserción de registro de asociación app/grupo		
def createGroupAppRel(groupId, hueId):	
	log.info("Generando la relacion entre el grupo " + groupId + " y el permiso " + hueId)
	sql = "insert into useradmin_grouppermission(hue_permission_id, group_id) values(" + hueId + "," + groupId + ")"
	return execPSQL("exec", sql)
	
#Logger
log = logging.getLogger("logs")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s \t %(levelname)s \t %(message)s","%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
log.addHandler(ch)
	
#Main
#Validación de argumentos
if len(sys.argv) < 4:
	usage()
	sys.exit()
else:
	if sys.argv[1] != "-u" and sys.argv[1] != "-a":
		usage()
		sys.exit()
	else:
		if sys.argv[1] == "-u" and len(sys.argv) > 4:
			usage()
			sys.exit()
		elif sys.argv[1] == "-a" and len(sys.argv) > 5:
			usage()
			sys.exit()
		else:
			print("")
			log.info("*** Comienzo de ejecucion de " + os.path.basename(__file__))

#Mapeo parámetros
option = sys.argv[1]
username = app = sys.argv[2]
if option == "-u":
	groups = sys.argv[3]
else:	
	permission = sys.argv[3]
	groups = sys.argv[4]

#Opción 1: asociación usuario a grupo(s)
if option == "-u":
	#Validación de usuario
	userId = getUserId(username)
	if str(userId) == "[]":
		log.error("No se ha encontrado en base de datos el usuario " + username)
		sys.exit()
	else:
		userId = str(userId[0])
		#Obtención de grupos actuales del usuario
		groupsName = getUserGroupRel(userId)
		#Recorrido de los grupos a asignar
		for group in groups.split(","):
			#Comprobación de existencia de grupo
			groupId = getGroupId(group)
			if str(groupId) == "[]":
				log.warn("No se ha encontrado en base de datos el grupo " + group)
			else:
				groupId = str(groupId[0])
				#Comprobación de si ya existe la asociación usuario/grupo
				if "'" + group + "'" in str(groupsName):
					log.warn("El usuario " + username + " ya tiene asignado el grupo " + group)
				else:
					#Generación de asociación usuario/grupo	
					log.info("El usuario " + username + " no tiene asignado el grupo " + group)
					createUserGroupRel(userId, groupId)
#Opción 2
else:
	#Validación de app
	hueId = getHueId(app, permission)[0]
	if str(hueId) == "[]":
		log.error("No se ha encontrado en base de datos el permiso " + permission + " para la app " + app)
		sys.exit()
	else:
		hueId = str(hueId[0])
		#Obtención de grupos actuales de la app
		groupsName = getGroupAppRel(hueId)
		#Recorrido de los grupos a asignar
		for group in groups.split(","):
			#Comprobación de existencia de grupo
			groupId = getGroupId(group)
			if str(groupId) == "[]":
				log.warn("No se ha encontrado en base de datos el grupo " + group)
			else:			
				groupId = str(groupId[0])
				#Comprobación de existencia de la asociación app/grupo
				if "'" + group + "'" in str(groupsName):
					log.warn("El grupo " + group + " ya tiene asignado el permiso " + permission + " de la app " + app)
				else:
					#Generación de asociación usuario/grupo	
					log.info("El grupo " + group + " no tiene asignado el permiso " + permission + " de la app " + app)
					createGroupAppRel(groupId, hueId)	
				
