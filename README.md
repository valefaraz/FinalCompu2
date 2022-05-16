# FinalCompu2

Sistema de control de cultivos
![COMPU2](https://user-images.githubusercontent.com/48955619/165187929-5846fffb-a5f6-44eb-9adf-dbf54c21a7a0.png)

La aplicación se basa en un servidor concurrente asincrónico que recibe datos de los diferentes sensores, mediante el uso de sockets, que se encuentran midiendo parametros de un determinado cultivo, estos datos se procesan y luego se almacenan en una DB mysql.

El servidor atiende las solicitudes web, para las cuales se responde el estado actual de los cultivos y gráficos informativos. El servidor menaja errores en las respuestas HTTP del tipo 404 Not Found y 405 Method Not Allowed.

Dependiendo el tipo de cultivo que se está controlando, se conocen los rangos aceptables de los parametros medidos. Cuando un parametro se encuentra fuera del rango aceptable para dicho cultivo, el servidor enviá una alerta al correo electronico del productor, esto se manejará mediante una cola de tareas distribuidas celery.

Los parametros de la configuracion de la db, el correo, rangos de las mediciones y configuraciones del sv se leen desde un archivo externo.

La simulacion de los sensores se realiza con 4 script de python para facilitar las pruebas pero se podria implementar sin ningun problema con arduino o raspberry y utilizar sensores reales.

Los elementos pricipales de la aplicacion son:
    1-Servidor asincronico con asyncio para atender peticiones de forma concurrente
    2-Celery, manejador de cola de tares, el sv delega la tarea de la verificacion de parametros y envio de mails
    3-Base de datos SQL (mysql) para almacenar informacion de los sensores y el historico de las mediciones
    4-Sensores simulados que envian datos al sv mediante sockets INET
    4-Interfaz web que muestra las mediciones en tiempo real y algunas graficas utiles para el productor. 