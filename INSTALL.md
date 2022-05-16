1- Clonar repositorio con el codigo del servidor
    git clone https://github.com/valefaraz/FinalCompu2.git
2- Instalar y configurar DB
    En este caso se uso mysql y se desplego el servicion con docker-compose
    sudo docker-compose up
    sudo docker-compose exec database bash  //ingresar a la terminal del contenedor, databases es el nombre del servicio
    sudo docker-compose start // levantar servicio mysql
3-Instalar librerias y dependencias
    sudo apt-get install python3.8
    pip install -r requirements.txt
4-Levantar Redis y Celery
    sudo docker run -p 6379:6379 redis
    celery -A tasks_celery worker --loglevel=info -c 2
5- Agregar las configuraciones a config.json
    Ej:
        "name": "namedb",
        "user": "1234",
        "pass": "1234",
        "host":"localhost",
        "port":3306,

        "email_receiver": "mailquerecibe@gmail.com",
        "email_address": "mailqueenvia@gmail.com",
        "email_password": "1234",

        "ip4_sv": "127.0.0.1",
        "ip6_sv": "::1",
        "port_sv":8000,

        "temperatura":[15,35],  # Rangos permitido de los parametros
        "humedad":[30,70],      
        "ph":[5,6.5],           

        "time_reload":50000
6- Levantar servidor
    python3 server.py -c /home/valentin/Escritorio/compu2/final/config.json -p 5000

    Nota: Si no se pasa la ruta del archivo config buscara el archivo en la misma ruta donde se encuentra parado y si no especifica puerto usara el de config
