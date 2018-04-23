#script para envio de correo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(toaddr_var,body_var):

    fromaddr = "$email_source"
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr_var
    msg["Subject"] = "Cuenta Creada Satisfactoriamente!!"
    body = body_var
    msg.attach(MIMEText(body,"plain"))
    #configuracion del server de smtp
    server = smtplib.SMTP("smtp.office365.com",587)
    #server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    #correo y contrasena del correo donde se enviaran emails
    server.login("$email_source","$pasword_email")
    text = msg.as_string()
    server.sendmail(fromaddr,toaddr_var,text)
    return

