#!/usr/bin/env python3
"""
Net-Auto: TCP Port Scanner
Fast multi-port TCP connect scan.
"""

import socket
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    Fore = type('', (), {'GREEN': '', 'YELLOW': '', 'RED': '', '__getattr__': lambda *_: ''})()
    Style = type('', (), {'RESET_ALL': '', '__getattr__': lambda *_: ''})()

# Common service names
SERVICES = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
    993: 'IMAPS', 995: 'POP3S', 3306: 'MySQL', 3389: 'RDP',
    5432: 'PostgreSQL', 6379: 'Redis', 8080: 'HTTP-Alt',
    8443: 'HTTPS-Alt', 27017: 'MongoDB', 5000: 'Flask-Dev',
}


def scan_port(host, port, timeout=2):
    """Scan a single TCP port. Returns (port, open, service_name)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            service = SERVICES.get(port, 'Unknown')
            return (port, True, service)
        return (port, False, '')
    except Exception:
        return (port, False, '')


def parse_ports(port_str):
    """Parse port specification like '22,80,443' or '1-1024'."""
    ports = set()
    for part in port_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def main():
    parser = argparse.ArgumentParser(description='Net-Auto TCP Port Scanner')
    parser.add_argument('--host', required=True, help='Target host')
    parser.add_argument('--ports', default='22,80,443,3389,8080', help='Ports (e.g. 22,80,443 or 1-1024)')
    args = parser.parse_args()
    
    ports = parse_ports(args.ports)
    
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"  Port Scanner")
    print(f"  Target: {args.host}")
    print(f"  Ports: {len(ports)} to scan")
    print(f"{'='*50}{Style.RESET_ALL}\n")
    
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, args.host, p): p for p in ports}
        for future in as_completed(futures):
            port, is_open, service = future.result()
            if is_open:
                open_ports.append((port, service))
                print(f"  {Fore.GREEN}[OPEN]{Style.RESET_ALL}   Port {port:>6}  {service}")
    
    print(f"\n{Fore.CYAN}Scan complete. {len(open_ports)} open port(s) found.{Style.RESET_ALL}\n")


if __name__ == '__main__':
    main()
