from socket import socket
import socketserver
import os
import asyncio
import argparse
import sys
import db
from string import Template

filein= open(os.getcwd() + '/index.html')
src=Template(filein.read())

cantidad_sensores=2

async def handle(reader, writer):
    
    data = await reader.read(100000)                                #Datos que recibe el servidor
    print(data)
    
    if  data.decode()[0:6] == 'sensor':                             #Solicitud del sensor 
        print ('Dato recibido')
        db.insert(data.decode())
    

    else:                                                           #Solicitud web
        ult_mediciones = db.select_valor(cantidad_sensores)
        D={}
        for num in range(cantidad_sensores):
            D['sensor'+str(num+1)]= ult_mediciones[num][0]
            D['tipo'+str(num+1)]= ult_mediciones[num][1]
            D['medicion'+str(num+1)]= ult_mediciones[num][2]
            D['fecha'+str(num+1)]= ult_mediciones[num][3]
        v_web= src.substitute(D)                                           


        path = os.getcwd() + '/filein.html'
        fd = open(path,'w')
        fd.writelines(v_web)
        fd.close()

        fd2=os.open(path, os.O_RDONLY)
        body = os.read(fd2,os.stat(path).st_size)
        #print(body)
        os.close(fd2)
        respuesta= '200 OK'
        header = bytearray("HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html' 
                    +"\r\nContent-length:" + str(len(body)) + "\r\n\r\n",'utf8')

        writer.write(header)
        writer.write(body)
        #await writer.drain()
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






    '''if str(control[1]) == 'Temperatura':
            if int(control[0]) < 10:
                print('Temperatura muy baja')
                None #Temperatura muy baja
            if int(control[0]) > 30:
                print('Temperatura muy Alta')
                None #Temperatura muy Alta
                
        elif str(control[1]) == 'Humedad':
            if int(control[0]) < 10:
                print('Muy Seco')
                None #Muy Seco
            if int(control[0]) > 30:
                print('Muy Humedo')
                None #Muy Humedo    '''