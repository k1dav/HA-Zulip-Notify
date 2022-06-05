"""
Custom component for Home Assistant to enable sending messages via Zulip API.

Example configuration.yaml entry:

notify:
  - name: zulip_notification
    platform: notify_zulip
    site: 'PASTE_YOUR_ZULIP_URL_HERE'
    email: 'PASTE_YOUR_BOT_EMAIL_HERE'
    key: 'PASTE_YOUR_BOT_key_HERE'
    channel: 'PASTE_THE_CHANNEL_YOU_WANT_BOT_NOTIFY_HERE'  

With this custom component loaded, you can send messaged to zulip Notify.
"""

import logging
import voluptuous as vol
import requests


import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required("site"): cv.string,
        vol.Required("email"): cv.string,
        vol.Required("key"): cv.string,
        vol.Required("channel"): cv.string,
        vol.Required("topic"): cv.string,
    }
)


def get_service(hass, config, discovery_info=None):
    """Get the Line notification service."""
    site = config.get("site")
    email = config.get("email")
    key = config.get("key")
    channel = config.get("channel")
    topic = config.get("topic")
    return ZulipNotificationService(site, email, key, channel, topic)


class ZulipNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Line Messaging service."""

    def __init__(self, site, email, key, channel, topic):
        """Initialize the service."""
        self.site = site
        self.email = email
        self.key = key
        self.channel = channel
        self.topic = topic

    def send_message(self, message="", **kwargs):
        """Send some message."""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = f"type=stream&to={self.channel}&topic={self.topic}&content={message}"

        try:
            response = requests.post(
                f"{self.site}api/v1/messages",
                headers=headers,
                data=data,
                auth=(self.email, self.key),
            )
        except Exception as e:
            _LOGGER.error(str(e))
