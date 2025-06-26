import os

from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = "1klikhelp@gmail.com"
EMAIL_FROM_NAME = "IKlik Support"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")