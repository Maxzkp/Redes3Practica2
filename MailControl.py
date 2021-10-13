from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib

names = ['Ready', 'Set', 'Go']

def sendWarning(umbralSuperado, variableObservada, to):
	msg = MIMEMultipart()

	password = '2017630191'
	msg['From'] = 'saulcabrera.zk@gmail.com'
	msg['To'] = to
	
	if umbralSuperado == 0:
		msg['Subject'] = f'Uso de {variableObservada} mas alto de lo normal - Practica 2'
	elif umbralSuperado == 1:
		msg['Subject'] = f'Uso de {variableObservada} mas alto de lo recomendable - Practica 2'
	elif umbralSuperado == 2:
		msg['Subject'] = f'Uso de {variableObservada} en estado critico - Practica 2'
	with open(f'rrd/{variableObservada}usage.png', 'rb') as file:
		msg.attach(MIMEImage(file.read()))
	msg.attach(MIMEText('Enviado por Saul Cabrera Perez', 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(msg['From'], password)
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()

if __name__ == '__main__':
	sendWarning(0, 'CPU')