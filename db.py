import pymysql


def insert(data):
    connection = pymysql.connect(host="localhost",
                            user="valentin",
                            passwd="valentin",
                            database="scc")
    
    #sensor , 1 , 25 , 2022-01-27 20:50:55
    
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
    connection = pymysql.connect(host="localhost",
                            user="valentin",
                            passwd="valentin",
                            database="scc")
    result=[]
    with connection:
        with connection.cursor() as cursor:
            for i in range(cantidad_sensores):
                sql = "SELECT mediciones.valor,s.tipo FROM mediciones join sensores as s on mediciones.id_sensor=s.id where id_sensor=%s order by mediciones.id desc limit 1;"
                cursor.execute(sql,(str(i+1),))
                select = cursor.fetchone()
                result.append(select)
    return result

            #result=result.split(sep=', ')
            #print (result[2])
        #connection.commit()