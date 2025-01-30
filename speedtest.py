from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from screenshot import take_screenshot

GECKODRIVER_PATH = "/snap/bin/geckodriver"
SPEEDTEST_URL = "http://www.speedtest.net"
ACCEPT_XPATH = '//*[@id="onetrust-accept-btn-handler"]'
START_TEST_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]'
PRIVACY_POLICY_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/a'
BUTTON_NOT_FOUND_ERROR = "{} was not found while waiting."


def run_firefox():
    options = Options()
    options.add_argument("-private-window")

    browser = webdriver.Firefox(service=Service(GECKODRIVER_PATH), options=options)
    browser.maximize_window()

    return browser


def open_speedtest_page(driver):
    driver.get(SPEEDTEST_URL)


def click_if_present(driver, timeout, by, xpath):
    try:
        button = WebDriverWait(driver, timeout).until(
            ec.element_to_be_clickable((by, xpath))
        )
        button.click()
    except (TimeoutException, NoSuchElementException):
        print(BUTTON_NOT_FOUND_ERROR.format(xpath))


def accept_cookies(driver):
    click_if_present(driver, 5, By.XPATH, ACCEPT_XPATH)


def start_speedtest(driver):
    click_if_present(driver, 1, By.XPATH, START_TEST_XPATH)


def close_privacy_policy(driver):
    click_if_present(driver, 1, By.XPATH, PRIVACY_POLICY_XPATH)


def run_speedtest():
    driver = run_firefox()
    try:
        open_speedtest_page(driver)
        accept_cookies(driver)
        start_speedtest(driver)
        close_privacy_policy(driver)
        take_screenshot(driver)
    finally:
        driver.quit()
