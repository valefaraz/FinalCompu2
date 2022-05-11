import pymysql
import json

def conexion():
    with open("config.json", "r") as j:
        config =json.load(j)
    connection = pymysql.connect(host=config["host"],
                        user=config["user"],
                        passwd=config["pass"],
                        database=config["name"])
    return connection

def insert(data):
    connection = conexion()
    lista=data.split(sep=' , ')
    id_sensor=lista[1]
    valor=lista[2]
    fecha=lista[3]
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO mediciones (id_sensor, valor, fecha) VALUES (%s, %s,%s)"
            cursor.execute(sql, (id_sensor,valor,fecha))
            connection.commit()

def select_ultimos_valores(cantidad_sensores):
    connection = conexion()
    result=[]
    with connection:
        with connection.cursor() as cursor:
            for i in range(cantidad_sensores):
                sql= 'SELECT s.id,s.tipo,mediciones.valor,mediciones.fecha FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=%s order by mediciones.id desc limit 1;'
                #sql = "SELECT mediciones.valor,s.tipo FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=%s order by mediciones.id desc limit 1;"
                cursor.execute(sql,(str(i+1),))
                select = cursor.fetchone()
                result.append(select)
    return result

def select_ultimo(id):
    connection = conexion()
    with connection:
        with connection.cursor() as cursor:
            sql= 'SELECT s.id,s.tipo,mediciones.valor,mediciones.fecha FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=%s order by mediciones.id desc limit 1;'
            cursor.execute(sql,(str(id),))
            select = cursor.fetchone()
    return select

def select_lux():
    connection = conexion()
    with connection:
        with connection.cursor() as cursor:
            #sql= 'SELECT s.id,s.tipo,mediciones.valor,mediciones.fecha FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=4 and mediciones.fecha <= NOW() AND mediciones.fecha >= date_add(NOW(), INTERVAL -7 DAY);'            
            sql= 'SELECT s.id,s.tipo,mediciones.valor,mediciones.fecha FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=4 ORDER BY mediciones.id desc LIMIT 7;'            
            
            cursor.execute(sql)
            select = cursor.fetchall()
    return select

def select_ph():
    connection = conexion()
    with connection:
        with connection.cursor() as cursor:
            sql= 'SELECT s.id,s.tipo,mediciones.valor,mediciones.fecha FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=3 ORDER BY mediciones.id desc LIMIT 7;'            
            cursor.execute(sql)
            select = cursor.fetchall()
    return select

def select_humedad():
    connection = conexion()
    with connection:
        with connection.cursor() as cursor:
            sql= 'SELECT s.id,s.tipo,mediciones.valor,mediciones.fecha FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=2 order by mediciones.id desc limit 100;'            
            cursor.execute(sql)
            select = cursor.fetchall()
    return select