import smtplib, ssl
from datetime import datetime
import json

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
Valor critico detectado
""" %(fecha)

# conexion
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
  #login
  server.login(email_address, email_password)
  # envio del mail
  server.sendmail(email_address, email_receiver, msj)