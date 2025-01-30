from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
options.add_argument("-private-window")

driver = webdriver.Firefox(service=Service("/snap/bin/geckodriver"), options=options)

driver.get("http://www.speedtest.net")
