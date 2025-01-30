from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

GECKODRIVER_PATH = "/snap/bin/geckodriver"


def run_firefox():
    options = Options()
    options.add_argument("-private-window")

    browser = webdriver.Firefox(service=Service(GECKODRIVER_PATH), options=options)
    browser.maximize_window()

    return browser


driver = run_firefox()


def open_speedtest_page():
    driver.get("http://www.speedtest.net")


open_speedtest_page()
