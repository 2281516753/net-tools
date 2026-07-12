# NetScope 🌐 浏览器端网络诊断

[![HTML5](https://img.shields.io/badge/HTML5-✓-E34F26?logo=html5)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-✓-F7DF1E?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> [📖 English Version / 英文版](README.md)

纯浏览器端网络诊断工具，支持暗色模式、历史记录、自动刷新，无需后端，打开即用。

**[🔗 在线演示](https://2281516753.github.io/net-diag-html/)**

## 功能

| 功能 | 说明 |
|------|------|
| 📍 **IP 信息** | 自动获取公网 IP、ISP、ASN、地理位置 |
| 📶 **连通性检测** | 百度、GitHub、Google、Cloudflare 多站点延迟监控 |
| 🔍 **DNS 查询** | 基于 Cloudflare DNS-over-HTTPS 的域名解析 |
| 📋 **HTTP Headers** | 查看目标 URL 响应头 |
| 🗺️ **路由可视化** | Traceroute 模拟 + 跳点动画 |
| 🌙 **暗色模式** | Light/Dark 主题切换，偏好保存到 localStorage |
| 📜 **历史记录** | 最近活动记录（DNS/端口/Headers/Traceroute） |
| 🔄 **自动刷新** | 可配置连通性自动刷新（30s-5min） |

## 技术栈

| 组件 | 技术 |
|------|------|
| 前端 | 纯 HTML/CSS/JS，零依赖 |
| DNS | Cloudflare DNS-over-HTTPS API |
| 地理信息 | ip-api.com |
| 主题 | CSS 自定义属性 + localStorage |
| 历史 | localStorage |

## 快速开始

```bash
# 直接用浏览器打开
open index.html

# 或本地服务器
python -m http.server 8080
```

## 使用场景

- **日常检查**：IP、ISP、多站点延迟一目了然
- **故障排查**：DNS + HTTP Headers + 延迟 —— 一个页面全搞定
- **跨平台**：任何带浏览器的设备都能用
- **作品展示**：纯前端项目，API 集成能力的最佳示范

## 相关项目

| 项目 | 说明 |
|------|------|
| [net-diag-demo](https://github.com/2281516753/net-diag-demo) | 全栈 Flask 网络诊断仪表盘 |
| [net-auto](https://github.com/2281516753/net-auto) | 网络自动化工具集 |
| [cloud-lab](https://github.com/2281516753/cloud-lab) | 云基础设施实验平台 |

## 作者

**王炯 (Wang Jiong)** — 网络工程专业。

[![GitHub](https://img.shields.io/badge/GitHub-2281516753-181717?logo=github)](https://github.com/2281516753)

## License

MIT