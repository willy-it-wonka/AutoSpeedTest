import os
import shutil

SCREENSHOT_DIR = "./screenshots"


def delete_folder():
    if os.path.exists(SCREENSHOT_DIR):
        shutil.rmtree(SCREENSHOT_DIR)
        print("Deleted folder with old screenshots.")


def take_screenshot():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
        print(f"Folder {SCREENSHOT_DIR} created.")
