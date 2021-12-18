import socketserver
import os
import asyncio
import argparse
import sys


def handle(reader, writer):
    fd = os.open('/home/valentin/Escritorio/compu2/final/index.html', os.O_RDONLY)
    body = os.read(fd,os.stat('/home/valentin/Escritorio/compu2/final/index.html').st_size)
    os.close(fd)
    dic = {"ico": "image/vnd.svf", "txt": " text/plain", "jpg": " image/jpeg",
            "ppm": " image/x-portable-pixmap", "html": " text/html",
            "pdf": " application/pdf"}
    respuesta= '200 OK'
    header = bytearray("HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'html' 
                    +"\r\nContent-length:" + str(len(body)) + "\r\n\r\n",'utf8')       
    writer.write(header)
    writer.write(body)
    


async def main():
    server = await asyncio.start_server(
                    handle,
                    ['127.0.0.1', '::1'], 
                    8080)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


#if __name__ == "__main__":

asyncio.run(main())