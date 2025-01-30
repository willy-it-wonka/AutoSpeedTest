import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

GECKODRIVER_PATH = "/snap/bin/geckodriver"
ACCEPT_XPATH = '//*[@id="onetrust-accept-btn-handler"]'
START_TEST_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]'
PRIVACY_POLICY_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/a'


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


def accept_cookies():
    click_if_present(By.XPATH, ACCEPT_XPATH, 5)


def start_speedtest():
    click_if_present(By.XPATH, START_TEST_XPATH, 1)


def close_privacy_policy():
    click_if_present(By.XPATH, PRIVACY_POLICY_XPATH, 1)


open_speedtest_page()

try:
    accept_cookies()
    start_speedtest()
    close_privacy_policy()
    time.sleep(90)  # TODO: screenshot
finally:
    driver.quit()
