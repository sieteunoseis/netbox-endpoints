# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-02-04

### Added
- Initial release
- EndpointType model for defining endpoint models (manufacturer + model)
- Endpoint model with:
  - MAC address (unique identifier)
  - Name, serial number, asset tag
  - Site and location
  - Primary IPv4/IPv6 (FK to IPAddress)
  - Connection type (wireless/wired)
  - SSID (wireless) or connected interface (wired)
  - Tenant, contact, platform
  - Status choices (active, offline, staged, decommissioned)
  - Tags and custom fields support
- List, detail, create, edit, delete views for both models
- Bulk import, edit, and delete support
- REST API endpoints
- Navigation menu with endpoints icon
- Dynamic URL registration for plugin tab integration
