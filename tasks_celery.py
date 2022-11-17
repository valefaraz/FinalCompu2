from celery import Celery
import smtplib, ssl
from datetime import datetime
import json

app = Celery('tasks', broker='redis://localhost', backend='redis://localhost:6379')

@app.task
def enviar_correo(ult_mediciones,temperatura,humedad,ph,email_address,email_password,email_receiver,smtp_address,smtp_port):
  enviar=False
  alerta=''
  if (ult_mediciones[1]) == "Temperatura":
    if float(ult_mediciones[2]) < temperatura[0]:
        alerta = "\nMedicion de " +str(ult_mediciones[1])+" por DEBAJO del rango aceptable: "+str(ult_mediciones[2])
        #tasks_celery.enviar_correo.delay(alerta)
        enviar=True
    elif float(ult_mediciones[2]) > temperatura[1]:
        alerta= "\nMedicion de "+str(ult_mediciones[1])+" por ARRIBA del rango aceptable: "+str(ult_mediciones[2])
        #tasks_celery.enviar_correo.delay(alerta)
        enviar=True
    else:
        alerta = "\nTemperatura OK"
        
  elif (ult_mediciones[1]) == "Humedad":
      if float(ult_mediciones[2]) < humedad[0]:
          alerta = "\nMedicion de " +str(ult_mediciones[1])+" por DEBAJO del rango aceptable: "+str(ult_mediciones[2])
          #tasks_celery.enviar_correo.delay(alerta)
          enviar=True
      elif float(ult_mediciones[2]) > humedad[1]:
          alerta = "\nMedicion de "+str(ult_mediciones[1])+" por ARRIBA del rango aceptable: "+str(ult_mediciones[2])
          #tasks_celery.enviar_correo.delay(alerta)
          enviar=True
      else:
          alerta = "\nHumedad OK"
        
  elif (ult_mediciones[1]) == "PH":
      if float(ult_mediciones[2]) < ph[0]:
          alerta = "\nMedicion de " +str(ult_mediciones[1])+" por DEBAJO del rango aceptable: "+str(ult_mediciones[2])
          #tasks_celery.enviar_correo.delay(alerta)
          enviar=True
      elif float(ult_mediciones[2]) > ph[1]:
          alerta = "\nMedicion de "+str(ult_mediciones[1])+" por ARRIBA del rango aceptable: "+str(ult_mediciones[2])
          #tasks_celery.enviar_correo.delay(alerta)
          enviar=True
      else:
          alerta="\nPH OK"


  if enviar:

    #smtp_address = 'smtp.gmail.com'
    #smtp_port = 465
    fecha= datetime.today()
    msj="""Subject: Alerta de cultivo \n

    Fecha: %s 
    Alerta de Cultivo
    %s
    """ %(fecha,alerta)

    # conexion
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
      #login
      server.login(email_address, email_password)
      # envio del mail
      server.sendmail(email_address, email_receiver, msj)
  return alerta

#if __name__ == "__main__":
#    app.start()

