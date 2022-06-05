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

import zulip

import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    ATTR_DATA,
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
    return LineNotificationService(site, email, key, channel, topic)


class LineNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Line Messaging service."""

    def __init__(self, site, email, key, channel, topic):
        """Initialize the service."""
        self.channel = channel
        self.topic = topic
        self.client = zulip.Client(site=site, email=email, key=key)

    def send_message(self, message="", **kwargs):
        """Send some message."""
        data = kwargs.get(ATTR_DATA, None)

        req = {
            "type": "stream",
            "to": self.channel,
            "topic": self.topic,
            "content": message,
        }
        self.client.send_message(req)
