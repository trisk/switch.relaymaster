---
layout: page
title: "RelayMaster Platforms"
description: "Instructions how to integrate RelayMaster boards with Home Assistant."
date: 2017-06-14
sidebar: true
comments: false
sharing: true
footer: true
---

RelayMaster platforms for Home Assistant
========================================
These components support Domotika home automation control boards running RelayMaster firmware that exposes `/ajax.xml` and `ioconf.xml`.

Work sponsored by Igor Guida.

The `relaymaster` switch platform allows you to control the relays of a Domotika control board running RelayMaster firmware.

To use your RelayMaster board with configured relays, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
switch:
  - platform: relaymaster
    url: http://IP_ADDRESS
    username: user
    password: secret
```

Configuration variables:

- **url** (*Required*): URL of the control board, e.g. `http://192.168.1.100`.
- **username** (*Required*): Username to log into the control board.
- **password** (*Required*): Password to log into the control board.

The `relaymaster` binary sensor platform allows you to read the digital inputs of a RelayMaster board.

To use your RelayMaster board with configured digital inputs, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
binary_sensor:
  - platform: relaymaster
    url: http://IP_ADDRESS
    username: user
    password: secret
```

Configuration variables:

- **url** (*Required*): URL of the control board, e.g. `http://192.168.1.100`.
- **username** (*Required*): Username to log into the control board.
- **password** (*Required*): Password to log into the control board.
- **max_number** (*Optional*): Maximum number of digital inputs on this board (Default: 12).
- **ignore_unused** (*Optional*): Skip inputs that have no name assigned (Default: True).

The `relaymaster` sensor platform allows you to read the analog inputs of a RelayMaster board.

To use your RelayMaster board with configured analog inputs, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: relaymaster
    url: http://IP_ADDRESS
    username: user
    password: secret
```

Configuration variables:

- **url** (*Required*): URL of the control board, e.g. `http://192.168.1.100`.
- **username** (*Required*): Username to log into the control board.
- **password** (*Required*): Password to log into the control board.
- **base_number** (*Optional*): The number of the last digital input before the analog inputs (Default: 12).
- **ignore_unused** (*Optional*): Skip inputs that have no name assigned (Default: True).

