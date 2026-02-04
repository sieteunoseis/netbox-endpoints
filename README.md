# NetBox Endpoints Plugin

A NetBox plugin for managing wireless and wired endpoints (badges, phones, IoT devices) that don't fit the traditional Device model.

![NetBox Version](https://img.shields.io/badge/NetBox-4.0+-blue)
![Python Version](https://img.shields.io/badge/Python-3.10+-green)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI](https://img.shields.io/pypi/v/netbox-endpoints)](https://pypi.org/project/netbox-endpoints/)

## Overview

The Endpoints plugin provides dedicated models for mobile/endpoint devices that don't fit the traditional NetBox Device model:

- **Vocera badges** - Wireless communication badges
- **Cisco IP phones** - Desk phones, wireless phones
- **IoT devices** - Sensors, controllers, etc.
- **Tablets/mobile devices** - iPads, scanners, etc.

Unlike Devices, Endpoints:
- Don't require rack locations
- Have MAC address as primary identifier
- Support wireless (SSID) and wired (switch port) connections
- Track connection type and status independently

## Features

- **Endpoint Types** - Define endpoint models (like DeviceType but for endpoints)
- **Endpoints** - Track individual endpoint devices with:
  - MAC address (required, unique)
  - Name, serial number, asset tag
  - Site and location
  - Primary IPv4/IPv6 (FK to IPAddress)
  - Connection type (wireless/wired)
  - SSID (wireless) or connected interface (wired)
  - Tenant, contact, platform
  - Status (active, offline, staged, decommissioned)
  - Full tag and custom field support
- **Plugin Integration** - Other plugins can add tabs to endpoint detail pages
- **REST API** - Full API access at `/api/plugins/netbox-endpoints/`

## Requirements

- NetBox 4.0 or higher
- Python 3.10+

## Installation

### From PyPI (recommended)

```bash
pip install netbox-endpoints
```

### From Source

```bash
git clone https://github.com/sieteunoseis/netbox-endpoints.git
cd netbox-endpoints
pip install -e .
```

### Docker Installation

Add to your NetBox Docker requirements file:

```bash
# requirements-extra.txt
netbox-endpoints
```

## Configuration

Add the plugin to your NetBox configuration:

```python
# configuration.py or plugins.py

PLUGINS = [
    'netbox_endpoints',
]

PLUGINS_CONFIG = {
    'netbox_endpoints': {
        # No configuration required - endpoints are stored in NetBox
    }
}
```

## Usage

### Creating Endpoint Types

1. Navigate to **Plugins > Endpoints > Endpoint Types**
2. Click **Add**
3. Select manufacturer and enter model name
4. Optionally set default platform

### Creating Endpoints

1. Navigate to **Plugins > Endpoints > Endpoints**
2. Click **Add**
3. Enter MAC address (required)
4. Select endpoint type, site, and other details
5. Set connection type (wireless/wired)
6. For wireless: enter SSID
7. For wired: select connected interface

### API Access

```bash
# List endpoints
curl -X GET "https://netbox.example.com/api/plugins/netbox-endpoints/endpoints/" \
  -H "Authorization: Token $TOKEN"

# Create endpoint
curl -X POST "https://netbox.example.com/api/plugins/netbox-endpoints/endpoints/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mac_address": "00:11:22:33:44:55", "endpoint_type": 1, "site": 1}'
```

## Plugin Integration

Other plugins (like netbox-catalyst-center) can register tabs on Endpoint detail pages using the standard NetBox `@register_model_view` decorator.

## Development

### Setup

```bash
git clone https://github.com/sieteunoseis/netbox-endpoints.git
cd netbox-endpoints
pip install -e ".[dev]"
```

### Code Style

```bash
black netbox_endpoints/
isort netbox_endpoints/
flake8 netbox_endpoints/
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Support

If you find this plugin helpful, consider supporting development:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/automatebldrs)

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## Author

sieteunoseis
