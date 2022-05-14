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

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.verify_mode = ssl.CERT_REQUIRED
#context.check_hostname = True
# context.load_default_certs()


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
        #ssl_sock = context.wrap_socket(s, server_hostname='localhost')
        #ssl_sock.connect((HOST, PORT))
        # ssl_sock.send(datos)
        s.connect((HOST, PORT))
        s.send(datos)
        print(datos)
        time.sleep(1000)
        s.close()
        # ssl_sock.close()
