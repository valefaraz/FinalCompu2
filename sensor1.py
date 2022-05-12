import socket
import time
from datetime import datetime
import random
from rsa import decrypt
from simplecrypt import encrypt
from db import select_key

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000        # The port used by the server
count=0
key=select_key()
while True:
    clave ='sensor'
    id_sensor='1'                                           #Sensor de temperatura 1
    valor=str(round((random.uniform(-10, 50)),2))
    fecha = str(datetime.now())[0:19]
    print(valor)

    datos = clave + ' , ' + id_sensor + ' , ' + valor + ' , ' + fecha
    datos= encrypt(key,datos)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(datos)
        print(datos)
        time.sleep(1000)
        s.close()