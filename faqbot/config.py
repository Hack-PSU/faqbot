"""Main configuration file. All secrets are read from environment variables."""
import os

"""
===== WEB SPECIFIC =====
"""

APP_NAME = os.environ.get("APP_NAME", "faqbot")
PORT = int(os.environ.get("PORT", 8114))
DEBUG = os.environ.get("DEBUG", "").lower() in ("true", "1", "yes")
SECRET = os.environ["SECRET"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

"""
===== MAIL SPECIFIC =====
"""

# IMAP server details (reading incoming emails).
IMAP_SERVER = [os.environ.get("IMAP_HOST", "imap.gmail.com")]
MAIL_USER = os.environ["MAIL_USER"]
MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
MAIL_BOX = os.environ.get("MAIL_BOX", '"[Gmail]/All Mail"')

# SMTP server details (sending emails via SendGrid).
SMTP_SERVER = [os.environ.get("SMTP_HOST", "smtp.sendgrid.net"), int(os.environ.get("SMTP_PORT", 465))]
SEND_MAIL_USER = os.environ.get("SEND_MAIL_USER", "apikey")
SEND_MAIL_PASSWORD = os.environ["SEND_MAIL_PASSWORD"]
MAIL_FROM = os.environ["MAIL_FROM"]

FOOTER = os.environ.get("FOOTER", """
<br><br> <i>~~ This was an automated message, please <a href="mailto:{from_addr}">email us</a> again if this didn't help! ~~</i>
""").format(from_addr=MAIL_FROM)

TRIGGERS = os.environ.get("TRIGGERS", "@faqbot,@fb").split(",")

# HackPSU API
HACKPSU_API_KEY = os.environ["HACKPSU_API_KEY"]
