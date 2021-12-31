# -*- coding: utf-8 -*-
#Pool de peticiones asíncronas de inserción de datos sobre API REST
#Gustavo Tejerina

import json
import requests
import datetime
import time
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor

#URL Elasticsearch
elastic = "http://localhost:9200"
#User
user = ""
pwd = ""
#Index name and data source for testing
testIndex = "test"
dataSource = "http://servicios.ine.es/wstempus/js/es/DATOS_TABLA/30838?tip=AM"
#dataSourceFile = '/home/gustavo/data.json'

#List of JSONs from public data source
def createRequests():
    return requests.get(dataSource, auth=HTTPBasicAuth(user, pwd)).json()

def createRequestsFromFile():
    with open(dataSourceFile) as json_file:
        jsonRequests = json.load(json_file)
    return jsonRequests

#Execute document index
def index(msg):
    r = requests.post(elastic + "/" + testIndex + "/_doc", data=json.dumps(msg),
                      headers={'content-type': 'application/json'}, auth=HTTPBasicAuth(user, pwd))
    return r.text

#Timestamp for output
def tmp():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f")

#Get the number of documents in index
def countIndex():
    try:
        return requests.get(elastic + "/" + testIndex + "/_count", auth=HTTPBasicAuth(user, pwd)).json()["count"]
    except:
        return 0

##Main
print(tmp() + "\tGenerating list of documents for indexing")
msgs = createRequests()
#msgs = createRequestsFromFile()
numRequests = len(msgs)
print(tmp() + "\tList created: " + str(numRequests) + " docs")

#Initial
iniIndexCount = countIndex()
iniTime = tmp()

#Pool
pool = ThreadPoolExecutor(max_workers=5000)
print(tmp() + "\tExecuting indexing")
#for request in pool.map(index, msgs):
#    print(tmp() + "\t" + request)
pool.map(index, msgs)

#Final
#time.sleep(1)
#finIndexCount = countIndex()
#finTime = tmp()
#print(tmp() + "\tIndexing executed: " + str(finIndexCount - iniIndexCount) + " docs, " + str(numRequests - (finIndexCount - iniIndexCount)) + " missed")
#print(tmp() + "\tIndexing executed: " + iniTime + " to " + finTime)