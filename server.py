from cmath import phase
from socket import socket
import socketserver
import os
import asyncio
import argparse
import sys
from urllib import request
import db
from string import Template
import tasks_celery


cantidad_sensores=4

def parcear(dato):
   try:
       encabezado = dato.decode().splitlines()[0]
       pedido = encabezado.split()
   except:
       pass
   return(pedido)

async def handle(reader, writer):
    
    data = await reader.read(100000)                                #Datos que recibe el servidor
    #print(data)
    
    if  data.decode()[0:6] == 'sensor':                             #Solicitud del sensor 
        print ('Dato recibido')
        db.insert(data.decode())

        ult_mediciones = db.select_valor(cantidad_sensores)
    
        print(ult_mediciones[0][2])
        #[(1, 'Temperatura', 12.96, datetime.datetime(2022, 4, 14, 20, 59, 56)), 
        #(2, 'Humedad', 25.0, datetime.datetime(2022, 4, 8, 12, 53, 28)), 
        #(3, 'PH', 13.0, datetime.datetime(2022, 4, 8, 12, 53, 35)), 
        #(4, 'Luminosidad', 1.0, datetime.datetime(2022, 4, 8, 12, 54, 31))]
        temperatura=[15,35] #rango permitido de temperatura
        humedad=[30,70]     #rango permitido de humedad
        ph=[5,6.5]          #rango permitido de ph
        #luminosidad=[]     #No se enviaran alertas en tiempo real de la luminosidad
        alerta=""
        for num in range(cantidad_sensores-1):

            if (ult_mediciones[num][1]) == "Temperatura":
                if float(ult_mediciones[num][2]) < temperatura[0]:
                    alerta= alerta + "\nMedicion de" +str(ult_mediciones[num][1])+" por DEBAJO del rango aceptable: "+str(ult_mediciones[num][2])
                    #print(alerta)

                elif float(ult_mediciones[num][2]) > temperatura[1]:
                    alerta= alerta + "\nMedicion de"+str(ult_mediciones[num][1])+" por ARRIBA del rango aceptable: "+str(ult_mediciones[num][2])
                    #print(alerta)
                else:
                    alerta=alerta + "\nTemperatura OK"
                    #print(alerta)

            elif (ult_mediciones[num][1]) == "Humedad":
                if float(ult_mediciones[num][2]) < humedad[0]:
                    alerta=alerta + "\nMedicion de " +str(ult_mediciones[num][1])+" por DEBAJO del rango aceptable: "+str(ult_mediciones[num][2])
                    #print(alerta)

                elif float(ult_mediciones[num][2]) > humedad[1]:
                    alerta=alerta + "\nMedicion de "+str(ult_mediciones[num][1])+" por ARRIBA del rango aceptable: "+str(ult_mediciones[num][2])
                    #print(alerta)
                else:
                    alerta=alerta + "\nHumedad OK"
                    #print(alerta)

            elif (ult_mediciones[num][1]) == "PH":
                if float(ult_mediciones[num][2]) < ph[0]:
                    alerta= alerta + "\nMedicion de" +str(ult_mediciones[num][1])+" por DEBAJO del rango aceptable: "+str(ult_mediciones[num][2])
                    #print(alerta)

                elif float(ult_mediciones[num][2]) > ph[1]:
                    alerta= alerta + "\nMedicion de "+str(ult_mediciones[num][1])+" por ARRIBA del rango aceptable: "+str(ult_mediciones[num][2])
                    #print(alerta)
                else:
                    alerta=alerta + "\nPH OK"
                    #print(alerta)
    
        tasks_celery.enviar_correo.delay(alerta)



    else:                                                                   #Solicitud web
        
        consulta=parcear(data)
        print(consulta)
        
        if consulta[0] == "GET":                                                                #Respuesta a  metodo GET
            if os.path.isfile(consulta[1].replace('/','')) == True or consulta[1]== '/':        #Respuesta si existe el archivo o /
                filein= open(os.getcwd() + '/index.html')
                src=Template(filein.read())

                ult_mediciones = db.select_valor(cantidad_sensores)
                #print(ult_mediciones)
                D={}
                for num in range(cantidad_sensores):
                    D['sensor'+str(num+1)]= ult_mediciones[num][0]
                    D['tipo'+str(num+1)]= ult_mediciones[num][1]
                    D['medicion'+str(num+1)]= ult_mediciones[num][2]
                    D['fecha'+str(num+1)]= ult_mediciones[num][3]
                #print(D)
                v_web= src.substitute(D)                                           
                path = os.getcwd() + '/filein.html'
                fd = open(path,'w')
                fd.writelines(v_web)
                fd.close()
                fd2=os.open(path, os.O_RDONLY)
                body = os.read(fd2,os.stat(path).st_size)
                os.close(fd2)
                respuesta= '200 OK'
                header = bytearray("HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html' 
                            +"\r\nContent-length:" + str(len(body)) + "\r\n\r\n",'utf8')

            elif os.path.isfile(consulta[1].replace('/','')) == False:                          #Respuesta si no existe el archivo
                path = os.getcwd() + '/error404.html'
                fd2=os.open(path, os.O_RDONLY)
                body = os.read(fd2,os.stat(path).st_size)
                os.close(fd2)
                respuesta= '404 Not Found'
                header = bytearray("HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html' 
                            +"\r\nContent-length:" + str(len(body)) + "\r\n\r\n",'utf8')
                
                
        else:                                                                                   #Respuesta si el metodo no esta permitido
            path = os.getcwd() + '/error405.html'
            fd2=os.open(path, os.O_RDONLY)
            body = os.read(fd2,os.stat(path).st_size)
            os.close(fd2)
            respuesta= '405 Method Not Allowed'
            header = bytearray("HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html' 
                        +"\r\nContent-length:" + str(len(body)) + "\r\n\r\n",'utf8')


        writer.write(header)                                                                        #Respondemos con la cabecera
        writer.write(body)                                                                          #Respondemos con el body
        writer.close()


async def main():
    server = await asyncio.start_server(
                    handle,
                    ['127.0.0.1', '::1'],
                    8000)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":

    asyncio.run(main())