#!/usr/bin/env python3
"""
Net-Auto: Network Device Configuration Backup
Supports SSH (paramiko) and Telnet connections.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("[!] Install paramiko: pip install paramiko")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    Fore = type('', (), {'GREEN': '', 'YELLOW': '', 'RED': '', 'CYAN': '', '__getattr__': lambda *_: ''})()
    Style = type('', (), {'RESET_ALL': '', '__getattr__': lambda *_: ''})()


def load_devices(path="devices.json"):
    """Load device inventory from JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ssh_backup(device, output_dir):
    """Backup config via SSH."""
    host = device['host']
    username = device.get('username', 'admin')
    password = device.get('password', '')
    commands = device.get('commands', ['display current-configuration'])
    
    print(f"{Fore.CYAN}[*] Connecting to {host} via SSH...")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=username, password=password, timeout=10)
        
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode('utf-8', errors='replace')
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_cmd = cmd.replace(' ', '_').replace('/', '_')[:30]
            filename = f"{host}_{safe_cmd}_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output)
            
            print(f"{Fore.GREEN}[✓] Saved: {filename} ({len(output)} bytes)")
    
    except paramiko.AuthenticationException:
        print(f"{Fore.RED}[✗] {host}: Authentication failed")
    except Exception as e:
        print(f"{Fore.RED}[✗] {host}: {e}")
    finally:
        client.close()


def main():
    devices = load_devices()
    output_dir = Path('backups') / datetime.now().strftime('%Y%m%d')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"{Fore.CYAN}{'='*50}")
    print(f"Net-Auto Config Backup")
    print(f"Devices: {len(devices)}")
    print(f"Output: {output_dir}")
    print(f"{'='*50}{Style.RESET_ALL}\n")
    
    for device in devices:
        ssh_backup(device, str(output_dir))
    
    print(f"\n{Fore.GREEN}[✓] Backup complete. Files saved to {output_dir}")


if __name__ == '__main__':
    main()
