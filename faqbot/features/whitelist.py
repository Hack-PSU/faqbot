"""This module handles the whitelist by checking
the HackPSU API for active organizers.
"""

from faqbot import app
from faqbot.web.auth import requires_auth
from faqbot.core.utils import get_menu
from faqbot.features.feature import Feature

from faqbot.core.store import gen_defaults, load_config, Store
from faqbot.config import HACKPSU_API_KEY, MAIL_USER

from flask import request, render_template, redirect, url_for
from email import message_from_bytes
from email.utils import parseaddr
import requests

DEFAULTS = {"enabled": True}

STORE = "whitelist"

gen_defaults(DEFAULTS, STORE)


def get_active_organizer_emails():
    """Fetch active organizer emails from the HackPSU API."""
    try:
        headers = {'x-api-key': HACKPSU_API_KEY}
        r = requests.get("https://apiv3.hackpsu.org/organizers", headers=headers, timeout=10)
        r.raise_for_status()
        organizers = r.json()
        return [o['email'].lower() for o in organizers if o.get('isActive')]
    except Exception as e:
        print("Failed to fetch organizers from HackPSU API:", e)
        return []


class Whitelist(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        pass

    @staticmethod
    def raw_callback(parsed, raw, reply_object):
        pass

    @staticmethod
    def get_name():
        return "Whitelist"

    @staticmethod
    def get_url():
        return "/whitelist"


def is_whitelisted(body):
    with Store(STORE) as s:
        if not s["enabled"]:
            return True

    return is_whitelisted_internal(body)


def is_whitelisted_internal(body):
    """Check if the sender is an active organizer via the HackPSU API
    or the configured bot email address.
    """
    if isinstance(body, str):
        body = body.encode('utf-8')

    parsed = message_from_bytes(body)
    from_address = parsed["From"]
    _, address = parseaddr(from_address)
    address = address.lower()

    # Always allow the bot's own email
    if address == MAIL_USER.lower():
        return True

    # Check against active organizers from HackPSU API
    active_emails = get_active_organizer_emails()
    return address in active_emails


# Web control panel render.
@app.route(Whitelist.get_url())
@requires_auth()
def whitelist_panel():
    config = load_config(STORE)
    active_organizers = get_active_organizer_emails()
    return render_template("whitelist.html", menu=get_menu(), c=config, organizers=active_organizers)


@app.route(Whitelist.get_url() + "/api/enable")
@requires_auth()
def enable_whitelist():
    with Store(STORE) as s:
        s["enabled"] = True
    return "OK"


@app.route(Whitelist.get_url() + "/api/disable")
@requires_auth()
def disable_whitelist():
    with Store(STORE) as s:
        s["enabled"] = False
    return "OK"
