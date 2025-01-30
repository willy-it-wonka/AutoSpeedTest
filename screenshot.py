import os
import shutil
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

SCREENSHOT_DIR = "./screenshots"
ELEMENT_AFTER_TEST_XPATH = '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[1]/ul/li[1]/a'
FOLDER_CREATED_MESSAGE = "Folder {} created."
SCREENSHOT_SAVED_MESSAGE = "Screenshot saved: {}"
TIMEOUT_ERROR = "The test has not been completed. Unable to take a screenshot."


def setup_screenshot_folder():
    shutil.rmtree(SCREENSHOT_DIR, ignore_errors=True)
    os.makedirs(SCREENSHOT_DIR)
    print(FOLDER_CREATED_MESSAGE.format(SCREENSHOT_DIR))


def take_screenshot(driver):
    try:
        WebDriverWait(driver, 90).until(
            ec.visibility_of_element_located(
                (By.XPATH, ELEMENT_AFTER_TEST_XPATH))
        )

        time.sleep(1)

        screenshot_name = f"screenshot_{time.strftime('%d.%m.%Y_%H-%M-%S')}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
        driver.save_screenshot(screenshot_path)
        print(SCREENSHOT_SAVED_MESSAGE.format(screenshot_path))

    except TimeoutException:
        print(TIMEOUT_ERROR)
