# Net-Auto 🔧 网络自动化工具集

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Tests](https://img.shields.io/badge/Tests-pytest-orange)](https://docs.pytest.org/)

> [📖 English Version / 英文版](README.md)

网络自动化工具集 — 配置备份、Ping 监控、子网计算、端口扫描。现已支持统一 CLI 和 JSON 输出。

## 功能

| 工具 | 说明 |
|------|------|
| **Config Backup** | 批量 SSH 备份交换机/路由器配置 |
| **Ping Monitor** | 多目标 ICMP 监控 + 延迟追踪 |
| **Subnet Calculator** | CIDR 子网计算器 |
| **Port Scanner** | TCP 端口扫描 + 服务识别 |

## 快速开始

```bash
git clone https://github.com/2281516753/net-auto.git
cd net-auto
pip install -r requirements.txt
```

## 使用方法

### 统一 CLI（推荐）

```bash
# 配置备份
python cli.py backup --hosts devices.json --output ./backups/

# Ping 监控（交互模式）
python cli.py ping --targets 8.8.8.8,1.1.1.1,192.168.1.1 --interval 5

# Ping 监控（JSON 输出）
python cli.py ping --targets 8.8.8.8,1.1.1.1 --count 3 --json

# 子网计算
python cli.py subnet 192.168.1.0/24
python cli.py subnet 10.0.0.0/8 --json

# 端口扫描
python cli.py scan --host 192.168.1.1 --ports 22,80,443
python cli.py scan --host 10.0.0.1 --ports 1-1024 --json
```

### 独立脚本

```bash
python backup.py --hosts devices.json --output ./backups/
python pingmon.py --targets 8.8.8.8,1.1.1.1 --interval 5
python subnet.py 192.168.1.0/24
python scanner.py --host 192.168.1.1 --ports 22,80,443,3389
```

### JSON 输出模式

所有命令支持 `--json` 参数输出机器可读格式：

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

### 日志级别

```bash
python cli.py scan --host 10.0.0.1 --log-level DEBUG
```

## 项目结构

```
net-auto/
├── cli.py             # 统一 CLI 入口
├── backup.py          # 配置备份 (SSH)
├── pingmon.py         # Ping 监控
├── subnet.py          # 子网计算
├── scanner.py         # 端口扫描
├── setup.py           # pip install 支持
├── devices.json       # 设备清单模板
├── requirements.txt   # 依赖
└── tests/             # pytest 测试套件
    └── test_cli.py
```

## 依赖

- Python 3.10+
- `paramiko` (SSH)
- `colorama` (彩色输出)

## 测试

```bash
pip install pytest
pytest tests/ -v
```

## 使用场景

- **批量备份**：SSH 登录 50+ 台设备，导出配置并按时间戳归档
- **链路监控**：多目标持续 Ping，快速定位丢包源头
- **子网规划**：CIDR 计算器，多 VLAN 办公网络规划利器
- **安全审计**：全网段端口扫描，在攻击者之前发现暴露服务

## 相关项目

| 项目 | 说明 |
|------|------|
| [cloud-lab](https://github.com/2281516753/cloud-lab) | 云基础设施实验平台 |
| [wsl-dev-setup](https://github.com/2281516753/wsl-dev-setup) | WSL2 开发环境一键部署 |
| [net-diag-html](https://github.com/2281516753/net-diag-html) | 浏览器端网络诊断 |
| [net-diag-demo](https://github.com/2281516753/net-diag-demo) | 全栈网络诊断仪表盘 |

## 作者

**王炯 (Wang Jiong)** — 网络工程专业，云计算方向求职中。

[![GitHub](https://img.shields.io/badge/GitHub-2281516753-181717?logo=github)](https://github.com/2281516753)

## License

MIT