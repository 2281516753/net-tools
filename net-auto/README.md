# Net-Auto 🔧

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Tests](https://img.shields.io/badge/Tests-pytest-orange)](https://docs.pytest.org/)
[![Packaging](https://img.shields.io/badge/packaging-pyproject.toml-3776AB?logo=python)](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

> [📖 中文版 / Chinese Version](README_CN.md)

Network automation toolkit — config backup, ping monitoring, subnet calculation, and port scanning. Now with a unified CLI and JSON output.

## Features

| Tool | Description |
|------|-------------|
| **Config Backup** | Batch backup switch/router configs via SSH |
| **Ping Monitor** | Multi-target ICMP monitoring with latency tracking |
| **Subnet Calculator** | CIDR calculator: IP range, broadcast, wildcard mask |
| **Port Scanner** | TCP connect scan with service fingerprinting |

## Quick Start

```bash
git clone https://github.com/2281516753/net-auto.git
cd net-auto
pip install -r requirements.txt
```

Or install in development mode (recommended):
```bash
pip install -e .
```

## Usage

### Unified CLI (Recommended)

```bash
# Config Backup
python cli.py backup --hosts devices.json --output ./backups/

# Ping Monitor (interactive)
python cli.py ping --targets 8.8.8.8,1.1.1.1,192.168.1.1 --interval 5

# Ping Monitor (one-shot with JSON)
python cli.py ping --targets 8.8.8.8,1.1.1.1 --count 3 --json

# Subnet Calculator
python cli.py subnet 192.168.1.0/24
python cli.py subnet 10.0.0.0/8 --json

# Port Scanner
python cli.py scan --host 192.168.1.1 --ports 22,80,443
python cli.py scan --host 10.0.0.1 --ports 1-1024 --json
```

### Individual Scripts

```bash
# Config Backup
python backup.py --hosts devices.json --output ./backups/

# Ping Monitor
python pingmon.py --targets 8.8.8.8,1.1.1.1 --interval 5

# Subnet Calculator
python subnet.py 192.168.1.0/24

# Port Scanner
python scanner.py --host 192.168.1.1 --ports 22,80,443,3389
```

### JSON Output Mode

All commands support `--json` for machine-readable output:

```bash
$ python cli.py subnet 192.168.1.0/24 --json
{
  "cidr": "192.168.1.0/24",
  "network": "192.168.1.0",
  "broadcast": "192.168.1.255",
  "total_addresses": 256,
  "usable_hosts": 254,
  ...
}
```

### Logging

```bash
python cli.py scan --host 10.0.0.1 --log-level DEBUG
```

## Project Structure

```
net-auto/
├── cli.py             # Unified CLI entry point
├── pyproject.toml      # Modern Python packaging (PEP 621)
├── backup.py          # Configuration backup (SSH)
├── pingmon.py         # Ping monitoring
├── subnet.py          # Subnet calculator
├── scanner.py         # Port scanner
├── setup.py           # pip install support
├── devices.json       # Device inventory template
├── requirements.txt   # Dependencies
└── tests/             # pytest test suite
    └── test_cli.py
```

## Requirements

- Python 3.10+
- `paramiko` (SSH backup)
- `colorama` (colored output)

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Use Cases

- **Batch backup**: SSH into 50+ devices, export configs, archive by timestamp
- **Link monitoring**: Continuous ping to multiple targets, pinpoint packet loss
- **Subnet planning**: CIDR calculator for multi-VLAN office network planning
- **Security audit**: Scan entire subnet, find exposed services

## Related Projects

| Project | Description |
|---------|-------------|
| [cloud-lab](https://github.com/2281516753/cloud-lab) | Cloud infrastructure lab environment |
| [wsl-dev-setup](https://github.com/2281516753/wsl-dev-setup) | WSL2 dev environment one-click setup |
| [net-diag-html](https://github.com/2281516753/net-diag-html) | Browser-based network diagnostics |
| [net-diag-demo](https://github.com/2281516753/net-diag-demo) | Full-stack network diagnostics dashboard |

## Author

**Wang Jiong (王炯)** — Network Engineering student, cloud computing career path.

[![GitHub](https://img.shields.io/badge/GitHub-2281516753-181717?logo=github)](https://github.com/2281516753)

## License

MIT
