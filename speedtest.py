from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

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


def click_if_present(by, xpath, timeout):
    try:
        button = WebDriverWait(driver, timeout).until(
            ec.element_to_be_clickable((by, xpath))
        )
        button.click()
    except (TimeoutException, NoSuchElementException):
        print(f"{xpath} was not found while waiting.")


open_speedtest_page()
