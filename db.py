import pymysql
import json

def insert(data):
    with open("config.json", "r") as j:
        config =json.load(j)
    connection = pymysql.connect(host=config["host"],
                        user=config["user"],
                        passwd=config["pass"],
                        database=config["name"])
    lista=data.split(sep=' , ')
    id_sensor=lista[1]
    valor=lista[2]
    fecha=lista[3]
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO mediciones (id_sensor, valor, fecha) VALUES (%s, %s,%s)"
            cursor.execute(sql, (id_sensor,valor,fecha))
            connection.commit()

def select_valor(cantidad_sensores):
    with open("config.json", "r") as j:
        config =json.load(j)
    connection = pymysql.connect(host=config["host"],
                        user=config["user"],
                        passwd=config["pass"],
                        database=config["name"])
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