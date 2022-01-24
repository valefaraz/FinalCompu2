import socket
import time

#socket = socket.socket()

#socket.connect(("localhost", 8080))
#print("Conectado al servidor") 
#Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto

 
#Creamos un bucle para retener la conexion
#while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    #mens = input("Mensaje desde Cliente a Servidor >> ")

#    time.sleep(5)
    #Con el método send, enviamos el mensaje

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server
count=0
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(b'10')
        time.sleep(2)
        s.close()
        count = count+1
        print(count)
#while True:

#   socket.sendall(b"10")
#   time.sleep(2)
#   print("ok")




