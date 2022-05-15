import socket
import time
from datetime import datetime
import random
from simplecrypt import encrypt
import json

#HOST = '127.0.0.1'  # The server's hostname or IP address
#PORT = 8000        # The port used by the server
with open('s_config.json', "r") as j:
    config = json.load(j)
    HOST = config["host"]    # The server's hostname or IP address
    PORT = config["port"]    # The port used by the server
    key = config["key"]      # Key for encrypt

count=0
while True:
    tipo ='sensor'
    id_sensor='2'                                           #Sensor de humedad 1
    valor=str(round((random.uniform(10, 90)),2))            #porcentaje del 10% al 90
    fecha = str(datetime.now())[0:19]
    print(valor)

    datos = tipo + ' , ' + id_sensor + ' , ' + valor + ' , ' + fecha
    datos = encrypt(key, datos)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(datos)
        print(datos)
        time.sleep(1000)
        s.close()