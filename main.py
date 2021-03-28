import csv
import json
import smtplib
import time
from jinja2 import Environment, FileSystemLoader

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('info.csv', 'r', encoding='UTF-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    data = [line for line in reader]

with open('config.json', 'r') as file:
    config = json.load(file)


def form_create(name):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    tm = env.get_template('main.html')
    msge = tm.render(name=name)

    return msge


login = config["login"]
password = config["password"]
host = config["server"]
delay = config["timer"]
subject = 'Voronezh State University'

server = smtplib.SMTP(host)
server.ehlo()
server.starttls()
server.login(login, password)

for key in data:
    text = form_create(key['name'])

    msg = MIMEMultipart()
    msg.attach(MIMEText(text, 'html', 'utf-8'))
    msg['Subject'] = subject
    msg['From'] = login
    msg['Reply-To'] = 'info@vsu.ru'

    server.sendmail(login, key['email'], msg.as_string())
    print('Сообщение отпралено на почту -> ', key['email'])
    time.sleep(0.5)
server.quit()
