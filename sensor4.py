import socket
import time
from datetime import datetime
import random

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000        # The port used by the server
count=0

while True:
    clave ='sensor'
    id_sensor='4'                                           #Sensor de Iluminancia
    valor=str(round((random.uniform(100, 2000)),2))         #lux=lumen /m²
    fecha = str(datetime.now())[0:19]
    print(valor)

    datos = clave + ' , ' + id_sensor + ' , ' + valor + ' , ' + fecha
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(datos.encode())
        time.sleep(86400)
        s.close()