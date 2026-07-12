# NetScope 🌐

[![HTML5](https://img.shields.io/badge/HTML5-✓-E34F26?logo=html5)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-✓-F7DF1E?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> [📖 中文版 / Chinese Version](README_CN.md)

Browser-based network diagnostics dashboard — dark mode, history recording, zero dependencies, works on GitHub Pages.

**[🔗 Live Demo](https://2281516753.github.io/net-diag-html/)**

## Features

| Feature | Description |
|---------|-------------|
| 📍 **IP Info** | Public IP, ISP, ASN, geolocation |
| 📶 **Connectivity** | Multi-site latency check (Baidu, GitHub, Google, Cloudflare) |
| 🔍 **DNS Lookup** | Cloudflare DNS-over-HTTPS based resolution |
| 📋 **HTTP Headers** | Inspect target URL response headers |
| 🗺️ **Traceroute** | Simulated traceroute with hop animation |
| 🌙 **Dark Mode** | Light/Dark theme toggle with localStorage persistence |
| 📜 **History** | Recent activity recording (DNS/Port/Headers/Trace) |
| 🔄 **Auto-Refresh** | Configurable connectivity auto-refresh (30s-5min) |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Vanilla HTML/CSS/JS, zero deps |
| DNS | Cloudflare DNS-over-HTTPS API |
| Geolocation | ip-api.com |
| Theme | CSS custom properties + localStorage |
| History | localStorage |

## Quick Start

```bash
# Open directly in browser
open index.html

# Or local server
python -m http.server 8080
```

## Use Cases

- **Daily check**: IP, ISP, multi-site latency at a glance
- **Troubleshooting**: DNS + HTTP headers + latency — all in one page
- **Cross-platform**: Works on any device with a browser
- **Portfolio**: Pure frontend project showcasing API integration

## Related Projects

| Project | Description |
|---------|-------------|
| [net-diag-demo](https://github.com/2281516753/net-diag-demo) | Full-stack Flask network diagnostics |
| [net-auto](https://github.com/2281516753/net-auto) | Network automation toolkit |
| [cloud-lab](https://github.com/2281516753/cloud-lab) | Cloud infrastructure lab environment |

## Author

**Wang Jiong (王炯)** — Network Engineering student.

[![GitHub](https://img.shields.io/badge/GitHub-2281516753-181717?logo=github)](https://github.com/2281516753)

## License

MIT