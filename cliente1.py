import socket
import time
obj = socket.socket()
 
#Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.connect(("localhost", 8080))
print("Conectado al servidor")
 
#Creamos un bucle para retener la conexion
while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    #mens = input("Mensaje desde Cliente a Servidor >> ")
    time.sleep(2)
    #Con el método send, enviamos el mensaje
    obj.send(b"5")
