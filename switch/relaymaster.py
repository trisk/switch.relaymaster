"""
Support for RelayMaster relay control boards.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.relaymaster/
"""

import logging
import xml.etree.ElementTree as ET

import requests
import voluptuous as vol

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_URL, CONF_USERNAME, CONF_PASSWORD)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEVICE_CONFIG_ENDPOINT = '/ioconf.xml'
DEVICE_STATE_ENDPOINT = '/ajax.xml'
RELAY_TOGGLE_ENDPOINT = '/cgi/relays.cgi'
OUTPUT_NODE_REGEX = '^o[0-9]+$'
RELAY_NODE = 'r{}'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the relay board switches."""
    import re

    base_url = config.get(CONF_URL).rstrip('/')
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    endpoint = base_url + DEVICE_CONFIG_ENDPOINT
    session = requests.Session()
    session.auth = requests.auth.HTTPBasicAuth(username, password)
    response = None

    try:
        response = session.get(endpoint, timeout=10)
    except requests.exceptions.MissingSchema:
        _LOGGER.error("Missing resource or schema in configuration. "
                      "Add http:// to your URL")
        return False
    except requests.exceptions.ConnectionError:
        _LOGGER.error("No route to device at %s", base_url)
        return False

    if response.status_code != 200:
        _LOGGER.warning("Request error for %s: %s", endpoint, response.text)
        return False

    relays = []

    root = ET.fromstring(response.text)
    for child in root:
        if not re.match(OUTPUT_NODE_REGEX, child.tag):
            continue
        config = child.text.split(';')
        name = config[0]
        pair = (int(config[10]), int(config[11]))
        if pair[0] == 0:
            continue
        if pair[1] != 0:
            relays.append(RelayDevice(session, base_url, pair[0],
                                      name + ' A'))
            relays.append(RelayDevice(session, base_url, pair[1],
                                      name + ' B'))
        else:
            relays.append(RelayDevice(session, base_url, pair[0], name))

    add_devices(relays)


class RelayDevice(SwitchDevice):
    """Representation of a RelayMaster relay."""

    def __init__(self, session, base_url, number, name):
        """Initialize the switch."""
        self._session = session
        self._base_url = base_url
        self._number = number
        self._name = name
        self._state = None

    @property
    def name(self):
        """Return the name of the relay."""
        return self._name.replace(".", " ").title()

    @property
    def is_on(self):
        """Return true if relay is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Switch the relay on."""
        if self._state:
            return

        endpoint = self._base_url + RELAY_TOGGLE_ENDPOINT
        response = self._session.get(endpoint, timeout=10,
                                     params={'rel': self._number})
        if response.status_code != 200:
            _LOGGER.warning("Request error for %s: %s",
                            endpoint, response.text)
            return

        self._state = True

    def turn_off(self, **kwargs):
        """Switch the relay off."""
        if not self._state:
            return

        endpoint = self._base_url + RELAY_TOGGLE_ENDPOINT
        response = self._session.get(endpoint, timeout=10,
                                     params={'rel': self._number})
        if response.status_code != 200:
            _LOGGER.warning("Request error for %s: %s",
                            endpoint, response.text)
            return

        self._state = False

    def update(self):
        """Update the state of the relay."""
        endpoint = self._base_url + DEVICE_STATE_ENDPOINT
        response = None

        try:
            response = self._session.get(endpoint, timeout=10)
        except requests.exceptions.ConnectionError:
            _LOGGER.warning("No route to device %s", self._resource)
            return

        if response.status_code != 200:
            _LOGGER.warning("Request error for %s: %s",
                            endpoint, response.text)
            return

        root = ET.fromstring(response.text)
        for child in root:
            if child.tag == RELAY_NODE.format(self._number):
                self._state = int(child.text) == 1
                break
