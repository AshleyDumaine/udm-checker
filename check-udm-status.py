#!/usr/local/bin/python3.10

import os
import argparse
from datetime import datetime
import sys
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service

URL='https://store.ui.com/collections/unifi-network-unifi-os-consoles/products/unifi-dream-machine'

parser = argparse.ArgumentParser(description='email if UDM is in stock')
parser.add_argument('--email', type=str)

args = parser.parse_args()

options = FirefoxOptions()
options.add_argument("--headless")
service = Service(f'{os.path.dirname(os.path.realpath(__file__))}/geckodriver')
driver = webdriver.Firefox(options=options, service=service)

driver.get(URL)

html = driver.page_source
driver.close()

soup = BeautifulSoup(html, 'html.parser')
status = soup.find(class_='comProduct__badge').getText()

now = datetime.now()
print(f'{now.strftime("%d/%m/%Y %H:%M:%S")} - {status}')

if status == "In Stock":
    msg = EmailMessage()
    msg['Subject'] = f'The Ubiquity Dream Machine is in stock!'
    msg['To'] = args.email
    msg.set_content(f'Handy link: {URL}')

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    # on you garbage google account, use https://www.google.com/settings/security/lesssecureapps
    s.login(os.environ['LOGIN'], os.environ['PASSWORD'])
    s.send_message(msg)
    s.quit()
