from selenium import webdriver
from selenium.webdriver.firefox.service import Service

driver = webdriver.Firefox(service=Service("/snap/bin/geckodriver"))

driver.get("http://www.speedtest.net")
