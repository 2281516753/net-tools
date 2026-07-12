#!/usr/bin/env python3
"""
Net-Auto: Subnet Calculator
CIDR notation to detailed subnet information.
"""

import sys
import ipaddress


def calc_subnet(cidr):
    """Calculate and display subnet details."""
    network = ipaddress.ip_network(cidr, strict=False)
    
    print(f"\n{'='*50}")
    print(f"  Subnet Calculator")
    print(f"{'='*50}")
    print(f"  CIDR Notation:    {cidr}")
    print(f"  Network Address:  {network.network_address}")
    print(f"  Broadcast:        {network.broadcast_address}")
    print(f"  Netmask:          {network.netmask}")
    print(f"  Wildcard:         {network.hostmask}")
    print(f"  First Host:       {list(network.hosts())[0] if network.num_addresses > 2 else 'N/A'}")
    print(f"  Last Host:        {list(network.hosts())[-1] if network.num_addresses > 2 else 'N/A'}")
    print(f"  Total Addresses:  {network.num_addresses}")
    print(f"  Usable Hosts:     {max(0, network.num_addresses - 2)}")
    print(f"  IP Version:       IPv{network.version}")
    print(f"  Private:          {'Yes' if network.is_private else 'No'}")
    print(f"{'='*50}\n")
    
    # Show all subnets if /24 or larger
    if network.prefixlen <= 24 and network.num_addresses <= 256:
        print("Host List:")
        for i, host in enumerate(network.hosts(), 1):
            print(f"  {i:>3}. {host}")
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python subnet.py <CIDR>")
        print("Example: python subnet.py 192.168.1.0/24")
        sys.exit(1)
    
    calc_subnet(sys.argv[1])


if __name__ == '__main__':
    main()
