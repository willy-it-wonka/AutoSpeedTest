import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from screenshot import take_screenshot

GECKODRIVER_PATH = "/snap/bin/geckodriver"
SPEEDTEST_URL = "http://www.speedtest.net"

SERVER_LOCATION = "Tokyo"
SERVER_PROVIDER = "Contabo"

WELCOME_MESSAGE = "Specify the location and provider of the server (e.g. Tokyo Verizon). If the server is unavailable, or you enter incorrect data, the default one will be used: Tokyo Contabo.\n"
BUTTON_NOT_FOUND_ERROR = "{} was not found while waiting."
SELECT_SERVER_SUCCESS_MESSAGE = "Selected {} {} server successfully."
RESELECTION_MESSAGE = "Retrying selection of {} {} server..."
SELECTED_SERVER_ERROR = "Could not select server."
AVAILABLE_SERVERS_MESSAGE = "List of available servers: "
INVALID_DATA_MESSAGE = "This server is unavailable or incorrect data has been entered."

ACCEPT_XPATH = '//*[@id="onetrust-accept-btn-handler"]'
CHANGE_SERVER_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[4]/div/div[3]/div/div/div[4]/a'
SEARCH_SERVER_INPUT_XPATH = '//*[@id="host-search"]'
SERVER_LIST_XPATH = "//li/a"
START_TEST_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]'
PRIVACY_POLICY_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/a'


def get_user_server_choice():
    user_input = input(WELCOME_MESSAGE).strip()

    if user_input:
        user_data = user_input.split(maxsplit=1)
        if len(user_data) == 2 and len(user_data[0]) > 2 and len(user_data[1]) > 2:
            return user_data[0], user_data[1]

    return SERVER_LOCATION, SERVER_PROVIDER


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
        button = (WebDriverWait(driver, timeout).
                  until(ec.element_to_be_clickable((by, xpath))))
        time.sleep(1)
        button.click()
        time.sleep(1)
    except (TimeoutException, NoSuchElementException):
        print(BUTTON_NOT_FOUND_ERROR.format(xpath))


def accept_cookies(driver):
    click_if_present(driver, 5, By.XPATH, ACCEPT_XPATH)


def open_server_selection(driver):
    click_if_present(driver, 5, By.XPATH, CHANGE_SERVER_XPATH)


def get_available_servers(driver):
    server_list = driver.find_elements(By.XPATH, SERVER_LIST_XPATH)
    available_servers = [server.text for server in server_list if server.text.strip()]
    print(AVAILABLE_SERVERS_MESSAGE, available_servers)
    return available_servers


def search_for_server(driver):
    global SERVER_LOCATION, SERVER_PROVIDER

    search_input = (WebDriverWait(driver, 5)
                    .until(ec.element_to_be_clickable((By.XPATH, SEARCH_SERVER_INPUT_XPATH))))
    search_input.clear()
    search_input.send_keys(SERVER_LOCATION)
    time.sleep(1)

    available_servers = get_available_servers(driver)

    if not available_servers or not any(
            f"{SERVER_LOCATION} {SERVER_PROVIDER}" == server for server in available_servers):
        print(INVALID_DATA_MESSAGE)
        SERVER_LOCATION, SERVER_PROVIDER = "Tokyo", "Contabo"
        search_input.clear()
        search_input.send_keys(SERVER_LOCATION)
        time.sleep(1)


def select_server_from_list(driver, attempt_retry=True):
    server_xpath = f"//li[a/span[contains(text(), '{SERVER_LOCATION}')] and a/span[contains(text(), '{SERVER_PROVIDER}')]]/a"
    try:
        click_if_present(driver, 5, By.XPATH, server_xpath)
        print(SELECT_SERVER_SUCCESS_MESSAGE.format(SERVER_LOCATION, SERVER_PROVIDER))
    except StaleElementReferenceException:
        if attempt_retry:
            time.sleep(1)
            print(RESELECTION_MESSAGE.format(SERVER_LOCATION, SERVER_PROVIDER))
            select_server(driver, False)
    except TimeoutException:
        print(SELECTED_SERVER_ERROR)


def select_server(driver, attempt_retry=True):
    open_server_selection(driver)
    search_for_server(driver)
    select_server_from_list(driver, attempt_retry)


def start_speedtest(driver):
    click_if_present(driver, 1, By.XPATH, START_TEST_XPATH)


def close_privacy_policy(driver):
    click_if_present(driver, 1, By.XPATH, PRIVACY_POLICY_XPATH)


def run_speedtest():
    global SERVER_LOCATION, SERVER_PROVIDER
    SERVER_LOCATION, SERVER_PROVIDER = get_user_server_choice()

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
