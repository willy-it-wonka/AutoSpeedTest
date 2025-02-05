import mimetypes
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

SCREENSHOT_DIR = "./screenshots"
EMAIL_SUBJECT = "Speedtest report"
EMAIL_CONTENT = "Screenshots are in attachment.\n\nCode: https://github.com/willy-it-wonka/AutoSpeedTest"
FOLDER_NOT_EXIST_MESSAGE = "Folder does not exist!"
FILES_NOT_EXIST_MESSAGE = "No PNG files found in the folder!"
FILES_ADDED_MESSAGE = "Added {} files to email."
EMAIL_INPUT_MESSAGE = "Enter the e-mail address of the report recipient.\n"
EMAIL_SENT_MESSAGE = "Email sent successfully to {}"
EMAIL_NOT_PROVIDED_ERROR = "No email address was provided. Sending has been canceled."
EMAIL_SENDING_ERROR = "Error while sending email: {}"

load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def get_screenshot_files():
    if not os.path.isdir(SCREENSHOT_DIR):
        print(FOLDER_NOT_EXIST_MESSAGE)
        return []

    files = [f for f in os.listdir(SCREENSHOT_DIR) if f.endswith(".png")]

    if not files:
        print(FILES_NOT_EXIST_MESSAGE)
        return []

    return files


def add_attachments_to_email(msg, files):
    for file in files:
        file_path = os.path.join(SCREENSHOT_DIR, file)
        mime_type, _ = mimetypes.guess_type(file_path)  # Recognizes the file type.
        mime_type = mime_type or "application/octet-stream"  # Means unknown file type.

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype=mime_type.split('/')[0],  # maintype e.g. "image"
                subtype=mime_type.split('/')[1],  # subtype e.g. "png"
                filename=file
            )

    print(FILES_ADDED_MESSAGE.format(len(files)))


def send_email():
    files = get_screenshot_files()
    if not files:
        return

    email_recipient = input(EMAIL_INPUT_MESSAGE).strip()
    if not email_recipient:
        print(EMAIL_NOT_PROVIDED_ERROR)
        return

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = email_recipient
    msg["Subject"] = EMAIL_SUBJECT
    msg.set_content(EMAIL_CONTENT)

    add_attachments_to_email(msg, files)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, APP_PASSWORD)
            server.send_message(msg)
        print(EMAIL_SENT_MESSAGE.format(email_recipient))
    except Exception as e:
        print(EMAIL_SENDING_ERROR.format(e))
