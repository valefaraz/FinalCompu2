import socket
import time
from datetime import datetime
import random
from simplecrypt import encrypt
import ssl
import json

with open('s_config.json', "r") as j:
    config = json.load(j)
    HOST = config["host"]    # The server's hostname or IP address
    PORT = config["port"]    # The port used by the server
    key = config["key"]      # Key for encrypt

count = 0
while True:
    tipo = 'sensor'
    id_sensor = '1'  # Sensor de temperatura 1
    valor = str(round((random.uniform(-10, 50)), 2))
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
