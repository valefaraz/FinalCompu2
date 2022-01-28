from socket import socket
import socketserver
import os
import asyncio
import argparse
import sys
import db

async def handle(reader, writer):
    
    '''dic = {"ico": "image/vnd.svf", "txt": " text/plain", "jpg": " image/jpeg",
            "ppm": " image/x-portable-pixmap", "html": " text/html",
            "pdf": " application/pdf"}'''

    data = await reader.read(100000)

    print(data)
    
    if  data.decode()[0:6] == 'sensor':                         #Datos del sensor 
        print ('Dato recibido')
        db.insert(data.decode())

    else:                                                        #Solicitud web
        path = os.getcwd() + '/index.html'
        fd = os.open(path, os.O_RDONLY)
        body = os.read(fd,os.stat(path).st_size)
        os.close(fd)
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