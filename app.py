"""Main file to run the entire faq-bot app.

This runs the webserver and the background listener thread
for incoming emails.
"""

from faqbot import app
from faqbot.config import PORT, DEBUG
from faqbot.core.mail import start_mail_thread

# Start the IMAP listener thread once on import.
# With gunicorn --preload, this runs in the master before forking.
start_mail_thread()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
