# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python utility for updating OVH DynHost DNS records with the current public IP address. It's designed to be run as a standalone script or potentially as a scheduled task to keep dynamic DNS records synchronized.

## Architecture

The codebase is intentionally simple with a single-file architecture (`main.py`):

- **get_public_ip()**: Fetches the current public IP using external services (ipify.org with ifconfig.me as fallback)
- **update_dynhost()**: Performs the actual DynHost update via OVH's API using HTTP Basic Auth
- **load_config()**: Loads credentials from `.env` file using python-dotenv
- **Main execution**: Orchestrates the IP detection and DynHost update process

Configuration is managed through environment variables loaded from a `.env` file (not tracked in git):
- `DYNHOST_USERNAME`: DynHost identifier (format: domain.com-hostname)
- `DYNHOST_PASSWORD`: DynHost password from OVH
- `DYNHOST_HOSTNAME`: Full hostname to update (e.g., subdomain.domain.com)

## Development Commands

**Package Manager**: This project uses `uv` for dependency management (modern Python package manager).

**Run the script**:
```bash
uv run main.py
```

**Install dependencies**:
```bash
uv sync
```

**Add a new dependency**:
```bash
uv add package-name
```

## Configuration Setup

Before running, create a `.env` file in the project root with:
```
DYNHOST_USERNAME=your-domain.com-hostname
DYNHOST_PASSWORD=your-dynhost-password
DYNHOST_HOSTNAME=hostname.your-domain.com
```

## OVH DynHost API

The script uses OVH's DynHost update endpoint at `https://www.ovh.com/nic/update` with the DynDNS protocol. Response codes:
- `good [IP]`: Update successful
- `nochg [IP]`: IP unchanged, no update needed
- Other responses indicate errors (e.g., authentication failure, invalid hostname)
