import pymysql

connection = pymysql.connect(host="localhost",
                        user="valentin",
                        passwd="valentin",
                        database="scc")

id_sensor='1'
valor='19'
fecha='2022-01-23 23:30:00'
with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO mediciones (id_sensor, valor, fecha) VALUES (%s, %s,%s)"
        cursor.execute(sql, (id_sensor,valor,fecha))

    connection.commit()