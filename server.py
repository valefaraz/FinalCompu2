import os
import asyncio
import argparse
from time import time
import db
from string import Template
import tasks_celery
import json


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
        id_sensor = data.decode()[9:10]
        ult_mediciones=db.select_ultimo(id_sensor)

        #[(1, 'Temperatura', 12.96, datetime.datetime(2022, 4, 14, 20, 59, 56)), 
        #(2, 'Humedad', 25.0, datetime.datetime(2022, 4, 8, 12, 53, 28)), 
        #(3, 'PH', 13.0, datetime.datetime(2022, 4, 8, 12, 53, 35)), 
        #(4, 'Luminosidad', 1.0, datetime.datetime(2022, 4, 8, 12, 54, 31))]
        #temperatura=[15,35] #rango permitido de temperatura
        #humedad=[30,70]     #rango permitido de humedad
        #ph=[5,6.5]          #rango permitido de ph
        with open(args.config, "r") as j:
            config =json.load(j)
            email_address = config["email_address"]
            email_password = config["email_password"]
            email_receiver = config["email_receiver"]
            temperatura=config["temperatura"]
            humedad=config["humedad"]
            ph=config["ph"]

        alerta=tasks_celery.enviar_correo(ult_mediciones,temperatura,humedad,ph,email_address,email_password,email_receiver)
        print(alerta)
        
    else:                                                                   #Solicitud web
        
        consulta=parcear(data)
        print(consulta)
        cantidad_sensores=4
        if consulta[0] == "GET":                                                                #Respuesta a  metodo GET
            if os.path.isfile(consulta[1].replace('/','')) == True or consulta[1]== '/':        #Respuesta si existe el archivo o /
                filein= open(os.getcwd() + '/index.html')
                src=Template(filein.read())

                ult_mediciones = db.select_ultimos_valores(cantidad_sensores)
                #print(ult_mediciones)
                
                D={}
                with open(args.config, "r") as j:
                    config =json.load(j)
                    D["time_reload"]=config["time_reload"]
                ultimos_lux= db.select_lux()
                ultimos_ph=db.select_ph()
                ultimos_humedad = db.select_humedad()

                for x in range(len(ultimos_lux)):
                    D["medicion_lux"+str(x)]=ultimos_lux[x][2]
                    D["fecha_lux"+str(x)]=ultimos_lux[x][3].date().day
                for x in range(len(ultimos_ph)):
                    D["medicion_ph"+str(x)]=ultimos_ph[x][2]
                    D["fecha_ph"+str(x)]=ultimos_ph[x][3].date().day
                for x in range(len(ultimos_humedad)):
                    D["medicion_h"+str(x)]=ultimos_humedad[x][2]
                    D["fecha_h"+str(x)]=str(ultimos_humedad[x][3].hour)
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

async def main(ipv4,port,ipv6):
    server = await asyncio.start_server(
                    handle,
                    [ipv4, ipv6],
                    port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(usage="./server.py [-h] -p PORT -c /config.json")
    parser.add_argument("-c", "--config", type=str, default=os.getcwd()+"/config.json", help="/home/../..")
    parser.add_argument("-p", "--port", type=int, default=False, help="Puerto")
    args = parser.parse_args()

    with open(args.config, "r") as j:
        print(args.config)
        config =json.load(j)
    if args.port != False:        
        port=args.port    
    else:
        port=config["port_sv"]
    
    ipv4=config["ip4_sv"]
    ipv6=config["ip6_sv"]

    
    if port > 65535 or port < 1023 :
        print("No tiene permisos para ocupar este puerto o NO existe-->default puerto 5000")
        port=8000
    asyncio.run(main(ipv4,port,ipv6))