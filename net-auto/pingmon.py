#!/usr/bin/env python3
"""
Net-Auto: Multi-target Ping Monitor
Real-time ICMP latency monitoring with colored output.
"""

import subprocess
import time
import sys
import argparse
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    Fore = type('', (), {'GREEN': '', 'YELLOW': '', 'RED': '', 'CYAN': '', '__getattr__': lambda *_: ''})()
    Style = type('', (), {'RESET_ALL': '', '__getattr__': lambda *_: ''})()


def ping_host(host, count=1, timeout=2):
    """Ping a host and return latency in ms, or None if failed."""
    try:
        result = subprocess.run(
            ['ping', '-c', str(count), '-W', str(timeout), host],
            capture_output=True, text=True, timeout=timeout + 1
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'time=' in line:
                    return float(line.split('time=')[1].split()[0])
        return None
    except Exception:
        return None


def color_latency(latency):
    """Return colored latency string."""
    if latency is None:
        return f"{Fore.RED}✗ TIMEOUT{Style.RESET_ALL}"
    elif latency < 20:
        return f"{Fore.GREEN}{latency:>6.1f} ms{Style.RESET_ALL}"
    elif latency < 80:
        return f"{Fore.YELLOW}{latency:>6.1f} ms{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}{latency:>6.1f} ms{Style.RESET_ALL}"


def main():
    parser = argparse.ArgumentParser(description='Net-Auto Ping Monitor')
    parser.add_argument('--targets', required=True, help='Comma-separated host list')
    parser.add_argument('--interval', type=int, default=5, help='Ping interval in seconds')
    args = parser.parse_args()
    
    targets = [t.strip() for t in args.targets.split(',')]
    
    print(f"{Fore.CYAN}Net-Auto Ping Monitor{Style.RESET_ALL}")
    print(f"Targets: {', '.join(targets)}")
    print(f"Interval: {args.interval}s | Press Ctrl+C to stop\n")
    
    header = f"{'Time':<20}" + ''.join(f"{t:>12}" for t in targets)
    print(header)
    print('-' * len(header))
    
    try:
        while True:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            results = [ping_host(t) for t in targets]
            line = f"{now:<20}" + ''.join(color_latency(r) for r in results)
            print(line)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}[!] Monitor stopped.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
