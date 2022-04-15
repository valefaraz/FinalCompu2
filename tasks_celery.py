# Celery service example: task to multiply two numbers

from celery import Celery
import smtplib, ssl
from datetime import datetime
import json



app = Celery('tasks', broker='redis://localhost', backend='redis://localhost:6379')

@app.task
def enviar_correo(alerta):
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465
    with open("config.json", "r") as j:
      data =json.load(j)

    email_address = data["email_address"]
    email_password = data["email_password"]

    # destinatario y mensaje
    email_receiver = data["email_receiver"]
    fecha= datetime.today()
    msj="""
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


if __name__ == "__main__":
    app.start()

