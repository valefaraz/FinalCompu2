import pymysql


def insert(data):
    connection = pymysql.connect(host="localhost",
                            user="valentin",
                            passwd="valentin",
                            database="scc")
    #sensor , 1 , 25 , 2022-01-27 20:50:55
    lista=data.split(sep=' , ')
    #print(lista)
    id_sensor=lista[1]
    valor=lista[2]
    fecha=lista[3]

    #print(id_sensor)
    #print(valor)
    #print(fecha)
    
    
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO mediciones (id_sensor, valor, fecha) VALUES (%s, %s,%s)"
            cursor.execute(sql, (id_sensor,valor,fecha))
    
        connection.commit()