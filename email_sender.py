import mimetypes
import os
import smtplib

from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "YOUR_GMAIL"
APP_PASSWORD = "APP_PASSWORD"
EMAIL_RECIPIENT = "EMAIL_RECIPIENT"

screenshot_folder = "./screenshots"

msg = EmailMessage()
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECIPIENT
msg["Subject"] = "Speed test result"
msg.set_content("Screenshots are in attachment.")


def send_email():
    if not os.path.exists(screenshot_folder):
        print("Folder does not exist!")
        return

    files = [f for f in os.listdir(screenshot_folder) if f.endswith(".png")]

    if not files:
        print("No PNG files found in the folder!")
        return

    for file in files:
        file_path = os.path.join(screenshot_folder, file)
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        with open(file_path, "rb") as f:
            msg.add_attachment(f.read(), maintype=mime_type.split('/')[0], subtype=mime_type.split('/')[1],
                               filename=file)

    print(f"Added {len(files)} files to email.")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, APP_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error while sending email: {e}")
