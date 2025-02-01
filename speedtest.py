import time

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
BUTTON_NOT_FOUND_ERROR = "{} was not found while waiting."
SERVER_LOCATION = "Tokyo"
SELECT_SERVER_SUCCESS_MESSAGE = f"Selected {SERVER_LOCATION} server successfully."
RESELECTION_MESSAGE = f"Retrying selection of {SERVER_LOCATION} server..."
SELECT_SERVER_ERROR = f"Could not select {SERVER_LOCATION} server."

ACCEPT_XPATH = '//*[@id="onetrust-accept-btn-handler"]'
CHANGE_SERVER_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[4]/div/div[3]/div/div/div[4]/a'
SEARCH_SERVER_INPUT_XPATH = '//*[@id="host-search"]'
CHOSEN_SERVER_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[7]/div/div/div/div[3]/div/div/ul/li[3]/a'  # Tokyo - Contabo
START_TEST_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]'
PRIVACY_POLICY_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/a'


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


def open_server_selection(driver):
    click_if_present(driver, 5, By.XPATH, CHANGE_SERVER_XPATH)
    time.sleep(1)


def search_for_server(driver):
    search_input = WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, SEARCH_SERVER_INPUT_XPATH))
    )
    search_input.send_keys(SERVER_LOCATION)
    time.sleep(1)


def select_server_from_list(driver):
    try:
        WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, CHOSEN_SERVER_XPATH))
        ).click()
        print(SELECT_SERVER_SUCCESS_MESSAGE)
    except TimeoutException:
        print(SELECT_SERVER_ERROR)


def select_server(driver):
    open_server_selection(driver)
    search_for_server(driver)
    select_server_from_list(driver)


def start_speedtest(driver):
    click_if_present(driver, 1, By.XPATH, START_TEST_XPATH)


def close_privacy_policy(driver):
    click_if_present(driver, 1, By.XPATH, PRIVACY_POLICY_XPATH)


def run_speedtest():
    driver = run_firefox()
    try:
        open_speedtest_page(driver)
        accept_cookies(driver)
        select_server(driver)
        start_speedtest(driver)
        close_privacy_policy(driver)
        take_screenshot(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    run_speedtest()
