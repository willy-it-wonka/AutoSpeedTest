import os
import shutil
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

SCREENSHOT_DIR = "./screenshots"


def delete_folder():
    if os.path.exists(SCREENSHOT_DIR):
        shutil.rmtree(SCREENSHOT_DIR)
        print("Deleted folder with old screenshots.")


def take_screenshot(driver):
    try:
        WebDriverWait(driver, 60).until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[1]/ul/li[1]/a'))
        )

        time.sleep(1)

        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
            print(f"Folder {SCREENSHOT_DIR} created.")

        screenshot_name = f"screenshot_{time.strftime('%d.%m.%Y_%H-%M-%S')}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
        driver.save_screenshot(screenshot_path)

        print(f"Screenshot saved: {screenshot_path}")

    except TimeoutException:
        print("The test has not been completed. Unable to take a screenshot.")
