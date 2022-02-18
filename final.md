# FinalCompu2
Sistema de control de cultivos
![COMPU2](https://user-images.githubusercontent.com/48955619/154610852-3bf93380-b62c-4053-93b6-0620184ccced.png)

La aplicación se basa en un servidor concurrente asincrónico y que recibe datos de los diferentes sensores, mediante el uso de sockets, que se encuentran midiendo parametros de un determinado cultivo, estos datos se analizán y luego se almacenan en una DB mysql.

El servidor atiende las solicitudes web, en la cual se muestra el estado actual de los cultivos e información de los históricos.

Dependiendo el tipo de cultivo que se está controlando, se conocen los rangos aceptables de los parametros medidos. Cuando un parametro se encuentra fuera del rango aceptable para dicho cultivo, el servidor enviá una alerta al correo del productor por telegram o correo, esto se manejará mediante una cola de tareas distribuidas

Se realiará despliegue en contenedores Docker.
