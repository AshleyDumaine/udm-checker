#!/usr/local/bin/python3.10

import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service

options = FirefoxOptions()
options.add_argument("--headless")
service = Service('./geckodriver')
driver = webdriver.Firefox(options=options, service=service)

driver.get("https://store.ui.com/collections/unifi-network-unifi-os-consoles/products/unifi-dream-machine")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
status = soup.find(class_='comProduct__badge').getText()
print(status)

driver.close()
