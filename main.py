import subprocess
import time

from email_sender import send_email
from screenshot import setup_screenshot_folder

NUM_TESTS = 5
WAIT_TIME = 10
RUN_TEST_MESSAGE = "Run speedtest {}/{}..."
WAITING_MESSAGE = "Waiting {} seconds before the next test...\n"
FINAL_MESSAGE = "All tests finished."


def run_speed_tests():
    setup_screenshot_folder()

    for i in range(NUM_TESTS):
        print(RUN_TEST_MESSAGE.format(i + 1, NUM_TESTS))
        subprocess.run(["python3", "speedtest.py"])

        if i < NUM_TESTS - 1:
            print(WAITING_MESSAGE.format(WAIT_TIME))
            time.sleep(WAIT_TIME)

    print(FINAL_MESSAGE)


if __name__ == "__main__":
    run_speed_tests()
    send_email()
