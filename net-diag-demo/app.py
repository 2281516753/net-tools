#!/usr/bin/env python3
"""
Network Diagnostics Dashboard
A Flask web app for WSL network & system diagnostics.
Built with AI-assisted development (Hermes Agent + DeepSeek V4).
"""

import subprocess
import socket
import json
import os
import platform
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ─── System Info ─────────────────────────────────────────────────────────

def run_cmd(cmd, timeout=5):
    """Run a shell command, return (stdout, stderr, exit_code)."""
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, shell=True
        )
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    except Exception as e:
        return "", str(e), -1


def parse_uptime(text):
    """Extract uptime string from `uptime -p` output."""
    return text.strip() or "unknown"


def parse_memory(text):
    """Parse `free -h` for mem used/total."""
    lines = text.strip().split("\n")
    if len(lines) < 2:
        return {"total": "N/A", "used": "N/A", "percent": 0}
    parts = lines[1].split()
    if len(parts) < 3:
        return {"total": "N/A", "used": "N/A", "percent": 0}
    total = parts[1]
    used = parts[2]
    pct = round(float(used.replace("Gi", "").replace("Mi", "")) /
                float(total.replace("Gi", "").replace("Mi", "")) * 100, 1) if "Gi" in total else 0
    return {"total": total, "used": used, "percent": pct}


def parse_disk(text):
    """Parse `df -h /` for disk usage."""
    lines = text.strip().split("\n")
    if len(lines) < 2:
        return {"total": "N/A", "used": "N/A", "avail": "N/A", "percent": 0}
    parts = lines[1].split()
    if len(parts) < 5:
        return {"total": "N/A", "used": "N/A", "avail": "N/A", "percent": 0}
    return {
        "total": parts[1],
        "used": parts[2],
        "avail": parts[3],
        "percent": parts[4].replace("%", "")
    }


@app.route("/api/system")
def api_system():
    """Get system metrics."""
    uptime, _, _ = run_cmd("uptime -p")
    mem_text, _, _ = run_cmd("free -h")
    disk_text, _, _ = run_cmd("df -h /")
    # load average
    load_text, _, _ = run_cmd("cat /proc/loadavg | cut -d' ' -f1-3")

    return jsonify({
        "hostname": socket.gethostname(),
        "platform": platform.uname().system,
        "release": platform.uname().release,
        "uptime": parse_uptime(uptime),
        "memory": parse_memory(mem_text),
        "disk": parse_disk(disk_text),
        "load_avg": load_text.strip(),
        "timestamp": datetime.now().isoformat()
    })


# ─── Connectivity Check ─────────────────────────────────────────────────

SITES = [
    ("百度", "https://www.baidu.com"),
    ("GitHub", "https://github.com"),
    ("Google", "https://www.google.com"),
    ("Telegram", "https://api.telegram.org"),
    ("DeepSeek", "https://api.deepseek.com"),
    ("小米 MiMo", "https://platform.xiaomimimo.com"),
]


def check_http(url, timeout=5):
    """Check HTTP reachability."""
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} (%{time_total}s)",
             "--connect-timeout", str(timeout), "--max-time", str(timeout+3), "-L", url],
            capture_output=True, text=True, timeout=timeout+5
        )
        output = r.stdout.strip()
        if r.returncode == 0 and output:
            return {"status": "reachable", "detail": output}
        else:
            return {"status": "unreachable", "detail": r.stderr.strip() or "no response"}
    except subprocess.TimeoutExpired:
        return {"status": "unreachable", "detail": "timeout"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def ping_host(host, count=2, timeout=5):
    """Ping a host, return avg latency."""
    try:
        r = subprocess.run(
            ["ping", "-c", str(count), "-W", str(timeout), host.split("//")[-1].split("/")[0]],
            capture_output=True, text=True, timeout=timeout+3
        )
        out = r.stdout
        if "avg" in out:
            avg = out.split("avg")[-1].split("=")[-1].split("/")[0].strip()
            return {"status": "ok", "latency_ms": avg}
        elif "1 received" in out or "2 received" in out:
            return {"status": "ok", "latency_ms": "high"}
        return {"status": "unreachable", "detail": "no reply"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.route("/api/connectivity")
def api_connectivity():
    """Check reachability to well-known sites."""
    results = []
    for name, url in SITES:
        http = check_http(url)
        results.append({
            "name": name,
            "url": url,
            "http": http,
        })
    return jsonify({
        "results": results,
        "timestamp": datetime.now().isoformat()
    })


# ─── Port Check ──────────────────────────────────────────────────────────

@app.route("/api/port-check", methods=["POST"])
def api_port_check():
    """Check if a TCP port is open."""
    data = request.get_json()
    host = data.get("host", "").strip()
    port = data.get("port", 0)

    if not host or not (1 <= port <= 65535):
        return jsonify({"error": "Invalid host or port (1-65535)"}), 400

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex((host, port))
        s.close()
        return jsonify({
            "host": host,
            "port": port,
            "open": result == 0,
            "message": "Port is open" if result == 0 else "Port is closed or filtered"
        })
    except socket.gaierror:
        return jsonify({"host": host, "port": port, "open": False, "message": "DNS resolution failed"})
    except Exception as e:
        return jsonify({"host": host, "port": port, "open": False, "message": str(e)})


# ─── DNS Lookup ───────────────────────────────────────────────────────────

@app.route("/api/dns-lookup", methods=["POST"])
def api_dns_lookup():
    """Resolve a domain name."""
    data = request.get_json()
    domain = data.get("domain", "").strip()
    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    try:
        addrs = socket.getaddrinfo(domain, 80)
        ips = list(set(a[4][0] for a in addrs))
        return jsonify({
            "domain": domain,
            "ips": ips,
            "count": len(ips)
        })
    except socket.gaierror as e:
        return jsonify({"domain": domain, "ips": [], "error": str(e)})


# ─── Proxy Status ─────────────────────────────────────────────────────────

@app.route("/api/proxy-status")
def api_proxy_status():
    """Check if mihomo proxy is running."""
    stdout, _, rc = run_cmd("systemctl --user is-active mihomo.service 2>/dev/null || echo inactive")
    proxy_running = "active" in stdout.lower()
    # Also check if proxy port is listening
    port_stdout, _, _ = run_cmd("ss -tlnp | grep -q ':7890' && echo listening || echo not_listening")
    return jsonify({
        "service": stdout.strip(),
        "http_proxy": os.environ.get("HTTP_PROXY", ""),
        "https_proxy": os.environ.get("HTTPS_PROXY", ""),
        "proxy_port_7890": port_stdout.strip(),
        "running": proxy_running,
        "timestamp": datetime.now().isoformat()
    })


# ─── Traceroute (simplified) ─────────────────────────────────────────────

@app.route("/api/traceroute", methods=["POST"])
def api_traceroute():
    """Run a simplified traceroute."""
    data = request.get_json()
    target = data.get("target", "").strip()
    if not target:
        return jsonify({"error": "Target is required"}), 400
    max_hops = min(data.get("max_hops", 15), 30)

    stdout, stderr, rc = run_cmd(
        f"traceroute -n -q 1 -m {max_hops} -w 2 {target} 2>&1 | head -30",
        timeout=60
    )
    lines = [l for l in stdout.split("\n") if l.strip()]
    hops = []
    for l in lines:
        parts = l.split()
        if len(parts) >= 2 and parts[0].isdigit():
            hop_num = parts[0]
            hop_ip = parts[1] if parts[1] != "*" else "timeout"
            hops.append({"hop": hop_num, "ip": hop_ip})

    return jsonify({
        "target": target,
        "hops": hops,
        "raw": stdout[:2000],
        "timestamp": datetime.now().isoformat()
    })


# ─── Main Page ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# Health check
@app.route("/api/health")
def api_health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@socketio.on("connect")
def handle_connect():
    """Handle client connection."""
    print(f"Client connected: {request.sid}")


@socketio.on("request_system_update")
def handle_system_update():
    """Send real-time system metrics."""
    uptime, _, _ = run_cmd("uptime -p")
    mem_text, _, _ = run_cmd("free -h")
    disk_text, _, _ = run_cmd("df -h /")
    load_text, _, _ = run_cmd("cat /proc/loadavg | cut -d' ' -f1-3")

    socketio.emit("system_update", {
        "uptime": uptime,
        "memory": parse_memory(mem_text),
        "disk": parse_disk(disk_text),
        "load": load_text,
        "timestamp": datetime.now().isoformat()
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"🚀 Network Diagnostics Dashboard")
    print(f"   http://localhost:{port}")
    print(f"   Press Ctrl+C to stop")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
