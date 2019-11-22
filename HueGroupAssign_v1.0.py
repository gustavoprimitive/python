# -*- coding: utf-8 -*-

import os
import sys
import re
import logging
import psycopg2

dbName = "hue"
dbHost = "localhost"
dbPort = 5432

#Usage
def usage():
	print("\nUsage:")
	print("\tpython " + os.path.basename(__file__) + " -u <user> <groups>")
	print("\tpython " + os.path.basename(__file__) + " -a <app> <permission> <groups>\n")
	print("\tLos grupos deben estar separados por comas\n")
	return

#Conexión a PostgreSQL
def connPSQL(dbUser, dbPass, dbHost, dbPort, dbName):	
	try:
		log.info("Estableciendo conexion con la base de datos " + dbName + " de PostgreSQL")
		connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (dbHost, dbPort, dbUser.strip(), dbPass.strip(), dbName)
		conn = psycopg2.connect(connstr)
		cursor = conn.cursor()
		log.info("Estableciendo conexion con la base de datos " + dbName + " de PostgreSQL\t...OK")
	except:
		log.error("No ha sido posible establecer la conexion con PostgreSQL")
		sys.exit()
	return [cursor, conn]

#Ejecución de sentencia
def execPSQL(cursor, sql, recFetch):
	try:
		log.debug("SQL:\t" + sql)
		cursor.execute(sql)
		if recFetch == 1:
			sqlResult = cursor.fetchone()
		elif recFetch == 2:
			sqlResult = cursor.fetchall()
		else:
			sqlResult = ""
			conn.commit()
		log.info("Sentencia ejecutada\t...OK")
	except:
		log.error("No ha sido posible ejecutar la sentencia en PostgreSQL")
		sys.exit()
	return sqlResult

#Desconexión con PostgreSQL	
def closePSQL(cursor, conn):	
	log.info("Cerrando conexion con la base de datos " + dbName + " de PostgreSQL")
	if(conn):
		cursor.close()
		conn.close()
		log.info("Cerrando conexion con la base de datos " + dbName + " de PostgreSQL\t...OK")
	
#Obtención de ID de usuario	
def getUserId(username, cursor):
	log.info("Obteniendo ID del usuario " + username)
	sql = "select id from auth_user where username = " + "'" + username + "';"
	return execPSQL(cursor, sql, 1)
	
#Obtención de ID de grupo	
def getGroupId(groupname, cursor):
	log.info("Obteniendo ID del grupo " + groupname)
	sql = "select id from auth_group where name = " + "'" + groupname + "';"
	return execPSQL(cursor, sql, 1)
	
#Obtención de los nombres de los grupos de un usuario
def getUserGroupRel(userId, cursor):
	log.info("Obteniendo los nombres de los grupos del usuario con ID " + userId)
	sql = "select ag.name from auth_user_groups aug inner join auth_group ag on aug.group_id = ag.id where user_id = " + userId + ";"
	return execPSQL(cursor, sql, 2)
	
#Obtención de ID de un un permiso de aplicación
def getHueId(app, permission, cursor):
	log.info("Obteniendo ID de permiso " + permission + " de la aplicacion " + app)
	sql = "select id from useradmin_huepermission where app = " + "'" + app + "'" + " and action = " + "'" + permission + "'" + ";";
	return execPSQL(cursor, sql, 1)
	
#Obtención de los grupos que poseen un permiso de aplicación determinada
def getGroupAppRel(hueId, cursor):
	log.info("Obteniendo los nombres de los grupos asociados al permiso " + hueId + " de Hue")
	sql = "select ag.name from useradmin_grouppermission ug inner join auth_group ag on ug.group_id = ag.id where hue_permission_id = " + hueId + ";"
	return execPSQL(cursor, sql, 2)

#Inserción de registro de asociación usuario/grupo	
def createUserGroupRel(userId, groupId, cursor):
	log.info("Generando la relacion entre el usuario " + userId + " y el grupo " + groupId)
	sql = "insert into auth_user_groups(user_id, group_id) values(" + userId + "," + groupId + ");"
	return execPSQL(cursor, sql, 0)

#Inserción de registro de asociación permiso/grupo		
def createGroupAppRel(groupId, hueId, cursor):	
	log.info("Generando la relacion entre el grupo " + groupId + " y el permiso " + hueId + " de Hue")
	sql = "insert into useradmin_grouppermission(hue_permission_id, group_id) values(" + hueId + "," + groupId + ");"
	return execPSQL(cursor, sql, 0)
	
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

#Solicitud de credenciales y datos de conexión de PostgreSQL
print("\nIntroducir el nombre de usuario de PostgreSQL: ", end = "\n")
dbUser = input()
print("\nIntroducir la password del usuario " + dbUser + ": ", end = "\n")
dbPass = input()
print("")

#Conexión
c = connPSQL(dbUser, dbPass, dbHost, dbPort, dbName)
#Mapeo de objetos de conexión
cursor = c[0]
conn = c[1]

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
	userId = getUserId(username, cursor)
	if str(userId) == "None":
		log.error("No se ha encontrado en base de datos el usuario " + username)
		sys.exit()
	else:
		userId = str(userId[0])
		#Obtención de grupos actuales del usuario
		groupsName = getUserGroupRel(userId, cursor)
		#Recorrido de los grupos asignar
		for group in groups.split(","):
			#Comprobación de existencia de grupo
			groupId = getGroupId(group, cursor)
			if str(groupId) == "None":
				log.warn("No se ha encontrado en base de datos el grupo " + group)
			else:
				groupId = str(groupId[0])
				#Comprobación de si ya existe la asociación usuario/grupo
				if "'" + group + "'" in str(groupsName):
					log.warn("El usuario " + username + " ya tiene asignado el grupo " + group)
				else:
					#Generación de asociación usuario/grupo	
					log.info("El usuario " + username + " no tiene asignado el grupo " + group)
					createUserGroupRel(userId, groupId, cursor)
#Opción 2
else:
	#Validación de app
	hueId = getHueId(app, permission, cursor)
	if str(hueId) == "None":
		log.error("No se ha encontrado en base de datos el permiso " + permission + " para la app " + app)
		sys.exit()
	else:
		hueId = str(hueId[0])
		#Obtención de grupos actuales de la app
		groupsName = getGroupAppRel(hueId, cursor)
		#Recorrido de los grupos a asignar
		for group in groups.split(","):
			#Comprobación de existencia de grupo
			groupId = getGroupId(group, cursor)		
			if str(groupId) == "None":
				log.warn("No se ha encontrado en base de datos el grupo " + group)
			else:			
				groupId = str(groupId[0])
				#Comprobación de existencia de la asociación app/grupo
				if "'" + group + "'" in str(groupsName):
					log.warn("El grupo " + group + " ya tiene asignado el permiso " + permission + " de la app " + app)
				else:
					#Generación de asociación usuario/grupo	
					log.info("El grupo " + group + " no tiene asignado el permiso " + permission + " de la app " + app)
					createGroupAppRel(groupId, hueId, cursor)	

#Desconexión PSQL
closePSQL(cursor, conn)
