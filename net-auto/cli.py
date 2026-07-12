#!/usr/bin/env python3
"""
Net-Auto: Unified CLI — Network Automation Toolkit

Usage:
    python cli.py backup --hosts devices.json
    python cli.py ping --targets 8.8.8.8,1.1.1.1
    python cli.py subnet 192.168.1.0/24
    python cli.py scan --host 192.168.1.1 --ports 22,80,443
"""

import argparse
import json as json_mod
import logging
import sys

# ── Logging setup ────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE = "%H:%M:%S"


def setup_logging(level="INFO"):
    """Configure root logger."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=LOG_FORMAT,
        datefmt=LOG_DATE,
    )


# ── JSON output helper ───────────────────────────────────────
def output(data, json_mode=False):
    """Print data as JSON if json_mode, else print as-is."""
    if json_mode:
        print(json_mod.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, list):
                    print(f"{k}:")
                    for item in v:
                        print(f"  - {item}")
                else:
                    print(f"{k}: {v}")


# ── Subcommands ──────────────────────────────────────────────

def cmd_backup(args):
    """Run config backup."""
    from backup import load_devices, ssh_backup
    from pathlib import Path
    from datetime import datetime

    logger = logging.getLogger("backup")
    devices = load_devices(args.hosts)
    output_dir = Path(args.output) / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting backup: {len(devices)} device(s)")
    logger.debug(f"Output directory: {output_dir}")

    results = []
    for device in devices:
        logger.info(f"Connecting to {device['host']}...")
        try:
            ssh_backup(device, str(output_dir))
            results.append({"host": device["host"], "status": "success"})
        except Exception as e:
            logger.error(f"{device['host']}: {e}")
            results.append({"host": device["host"], "status": "failed", "error": str(e)})

    if args.json:
        output({"backup": {"output": str(output_dir), "results": results}}, json_mode=True)
    else:
        success = sum(1 for r in results if r["status"] == "success")
        print(f"\nDone: {success}/{len(results)} successful")


def cmd_ping(args):
    """Run ping monitor."""
    from pingmon import ping_host
    import time
    from datetime import datetime

    logger = logging.getLogger("ping")
    targets = [t.strip() for t in args.targets.split(",")]
    count = args.count or 0

    logger.info(f"Pinging {len(targets)} target(s)")

    if args.json:
        # JSON mode: single-shot with structured output
        results = []
        for t in targets:
            latency = ping_host(t)
            results.append({"target": t, "latency_ms": latency, "reachable": latency is not None})
        output({"ping": {"timestamp": datetime.now().isoformat(), "results": results}}, json_mode=True)
    else:
        # Interactive mode
        print(f"{'Time':<20}", end="")
        for t in targets:
            print(f"{t:>12}", end="")
        print()
        print("-" * (20 + 12 * len(targets)))

        iteration = 0
        try:
            while True:
                iteration += 1
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{now:<20}", end="")
                for t in targets:
                    lat = ping_host(t)
                    if lat is None:
                        print(f"{'TIMEOUT':>12}", end="")
                    else:
                        print(f"{lat:>9.1f} ms", end="  ")
                print()
                if count and iteration >= count:
                    break
                if args.interval and (count == 0 or iteration < count):
                    time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped.")


def cmd_subnet(args):
    """Run subnet calculator."""
    import ipaddress

    cidr = args.cidr
    network = ipaddress.ip_network(cidr, strict=False)
    hosts = list(network.hosts())

    data = {
        "cidr": cidr,
        "network": str(network.network_address),
        "broadcast": str(network.broadcast_address),
        "netmask": str(network.netmask),
        "wildcard": str(network.hostmask),
        "first_host": str(hosts[0]) if hosts else "N/A",
        "last_host": str(hosts[-1]) if hosts else "N/A",
        "total_addresses": network.num_addresses,
        "usable_hosts": max(0, network.num_addresses - 2),
        "ip_version": f"IPv{network.version}",
        "is_private": network.is_private,
    }

    if args.json:
        output(data, json_mode=True)
    else:
        print(f"\n{'='*50}")
        print(f"  Subnet Calculator")
        print(f"{'='*50}")
        for k, v in data.items():
            label = k.replace("_", " ").title()
            print(f"  {label:<18} {v}")
        print(f"{'='*50}\n")


def cmd_scan(args):
    """Run port scanner."""
    from scanner import scan_port, parse_ports
    from concurrent.futures import ThreadPoolExecutor, as_completed

    logger = logging.getLogger("scan")
    host = args.host
    ports = parse_ports(args.ports)

    logger.info(f"Scanning {host}: {len(ports)} port(s)")

    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, host, p): p for p in ports}
        for future in as_completed(futures):
            port, is_open, service = future.result()
            if is_open:
                open_ports.append({"port": port, "service": service})
                logger.info(f"Open: {port} ({service})")

    if args.json:
        output({"scan": {"host": host, "ports_scanned": len(ports), "open": open_ports}}, json_mode=True)
    else:
        print(f"\nHost: {host}  |  Scanned: {len(ports)}  |  Open: {len(open_ports)}")
        for p in open_ports:
            print(f"  [OPEN] {p['port']:>6}  {p['service']}")
        print()


# ── Main CLI ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="net-auto",
        description="Network Automation Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  net-auto backup --hosts devices.json
  net-auto ping --targets 8.8.8.8,1.1.1.1 --interval 5
  net-auto subnet 192.168.1.0/24
  net-auto scan --host 10.0.0.1 --ports 22,80,443
        """,
    )
    parser.add_argument("--json", action="store_true", help="JSON output mode")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # backup
    p = sub.add_parser("backup", help="Backup device configs via SSH")
    p.add_argument("--hosts", default="devices.json", help="Device inventory JSON")
    p.add_argument("--output", default="./backups/", help="Output directory")

    # ping
    p = sub.add_parser("ping", help="Multi-target ping monitor")
    p.add_argument("--targets", required=True, help="Comma-separated target IPs")
    p.add_argument("--interval", type=int, default=5, help="Ping interval (seconds)")
    p.add_argument("--count", type=int, default=0, help="Number of pings (0=unlimited)")

    # subnet
    p = sub.add_parser("subnet", help="CIDR subnet calculator")
    p.add_argument("cidr", help="CIDR notation (e.g. 192.168.1.0/24)")

    # scan
    p = sub.add_parser("scan", help="TCP port scanner")
    p.add_argument("--host", required=True, help="Target host")
    p.add_argument("--ports", default="22,80,443,3389,8080", help="Ports to scan")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    setup_logging(args.log_level)

    commands = {
        "backup": cmd_backup,
        "ping": cmd_ping,
        "subnet": cmd_subnet,
        "scan": cmd_scan,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
