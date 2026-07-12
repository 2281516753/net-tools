# Network Diagnostics Dashboard 📊

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-✓-000000?logo=flask)](https://flask.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-✓-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-✓-FF6384?logo=chartdotjs)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> [📖 中文版 / Chinese Version](README_CN.md)

Full-stack network diagnostics web app — Flask backend + responsive frontend, monitoring WSL system health and network connectivity.

## Features

| Feature | Description |
|---------|-------------|
| 📊 **System Status** | WSL host metrics (uptime, CPU, memory, disk) |
| 🌐 **Connectivity** | Ping & HTTP reachability to common sites |
| 🔌 **Port Scanner** | Check if a remote TCP port is open |
| 🕵️ **DNS Lookup** | Resolve domain names to IPs |
| 📡 **Traceroute** | Simulated traceroute with hop display |
| 🛡️ **Proxy Status** | Check if mihomo proxy is running |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python Flask |
| Frontend | HTML + Tailwind CSS + Chart.js |
| Platform | WSL2 (Ubuntu 26.04) |

## Quick Start

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5001
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/system` | GET | System metrics |
| `/api/connectivity` | GET | Site reachability |
| `/api/port-check` | POST | TCP port check `{host, port}` |
| `/api/dns-lookup` | POST | DNS resolution `{domain}` |
| `/api/proxy-status` | GET | Proxy status |

## Use Cases

- **Daily check**: System resources + network status at a glance
- **Troubleshooting**: Port scan + DNS lookup — diagnose in one page
- **WSL diagnostics**: Host metrics + proxy status for quick issue resolution

## Related Projects

| Project | Description |
|---------|-------------|
| [net-diag-html](https://github.com/2281516753/net-diag-html) | Browser-based network diagnostics |
| [net-auto](https://github.com/2281516753/net-auto) | Network automation toolkit |
| [cloud-lab](https://github.com/2281516753/cloud-lab) | Cloud infrastructure lab environment |
| [wsl-dev-setup](https://github.com/2281516753/wsl-dev-setup) | WSL2 dev environment setup |

## Author

**Wang Jiong (王炯)** — Network Engineering student.

[![GitHub](https://img.shields.io/badge/GitHub-2281516753-181717?logo=github)](https://github.com/2281516753)

## License

MIT