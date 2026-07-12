# Network Diagnostics Dashboard 📊 网络诊断仪表盘

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-✓-000000?logo=flask)](https://flask.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-✓-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-✓-FF6384?logo=chartdotjs)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> [📖 English Version / 英文版](README.md)

全栈网络诊断 Web 应用 —— Flask 后端 + 响应式前端，监控 WSL 系统健康与网络连通性。

## 功能

| 功能 | 说明 |
|------|------|
| 📊 **系统状态** | WSL 宿主机指标（uptime, CPU, 内存, 磁盘） |
| 🌐 **连通性检测** | 常用站点 Ping & HTTP 可达性 |
| 🔌 **端口扫描** | 检测远程 TCP 端口是否开放 |
| 🕵️ **DNS 查询** | 域名解析到 IP 地址 |
| 📡 **路由追踪** | 模拟 Traceroute 显示跳点 |
| 🛡️ **代理状态** | 检查本地 mihomo 代理是否运行 |

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python Flask |
| 前端 | HTML + Tailwind CSS + Chart.js |
| 平台 | WSL2 (Ubuntu 26.04) |

## 快速开始

```bash
pip install -r requirements.txt
python app.py
# 浏览器打开 http://localhost:5001
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/system` | GET | 系统指标 |
| `/api/connectivity` | GET | 站点可达性 |
| `/api/port-check` | POST | TCP 端口检测 `{host, port}` |
| `/api/dns-lookup` | POST | DNS 解析 `{domain}` |
| `/api/proxy-status` | GET | 代理状态 |

## 使用场景

- **日常检查**：系统资源 + 网络状态一目了然
- **故障排查**：端口扫描 + DNS 查询 —— 一个页面定位问题
- **WSL 诊断**：宿主机指标 + 代理状态，快速定位 WSL 问题

## 相关项目

| 项目 | 说明 |
|------|------|
| [net-diag-html](https://github.com/2281516753/net-diag-html) | 浏览器端网络诊断 |
| [net-auto](https://github.com/2281516753/net-auto) | 网络自动化工具集 |
| [cloud-lab](https://github.com/2281516753/cloud-lab) | 云基础设施实验平台 |
| [wsl-dev-setup](https://github.com/2281516753/wsl-dev-setup) | WSL2 开发环境一键部署 |

## 作者

**王炯 (Wang Jiong)** — 网络工程专业。

[![GitHub](https://img.shields.io/badge/GitHub-2281516753-181717?logo=github)](https://github.com/2281516753)

## License

MIT