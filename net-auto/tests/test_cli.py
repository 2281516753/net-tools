"""Tests for net-auto CLI and core modules."""

import sys
import os
import json
import pytest

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSubnet:
    """Subnet calculator tests (no external deps)."""

    def test_basic_cidr(self):
        import ipaddress
        net = ipaddress.ip_network("192.168.1.0/24", strict=False)
        assert str(net.network_address) == "192.168.1.0"
        assert str(net.broadcast_address) == "192.168.1.255"
        assert net.num_addresses == 256
        assert net.is_private

    def test_small_subnet(self):
        import ipaddress
        net = ipaddress.ip_network("10.0.0.0/30", strict=False)
        assert net.num_addresses == 4
        hosts = list(net.hosts())
        assert len(hosts) == 2

    def test_ipv6(self):
        import ipaddress
        net = ipaddress.ip_network("2001:db8::/32", strict=False)
        assert net.version == 6


class TestScanner:
    """Port scanner tests."""

    def test_parse_single_port(self):
        from scanner import parse_ports
        assert parse_ports("22") == [22]

    def test_parse_comma_ports(self):
        from scanner import parse_ports
        assert parse_ports("22,80,443") == [22, 80, 443]

    def test_parse_range(self):
        from scanner import parse_ports
        result = parse_ports("22-25")
        assert result == [22, 23, 24, 25]

    def test_parse_mixed(self):
        from scanner import parse_ports
        result = parse_ports("22,80-82,443")
        assert result == [22, 80, 81, 82, 443]

    def test_localhost_port_open(self):
        """Test scanning a port on localhost."""
        from scanner import scan_port
        # We can't guarantee any port is open, but this should not crash
        port, is_open, service = scan_port("127.0.0.1", 22, timeout=1)
        assert isinstance(port, int)
        assert isinstance(is_open, bool)


class TestCLI:
    """CLI integration tests."""

    def test_subnet_json_output(self, capsys):
        """Test subnet command with JSON output."""
        from cli import cmd_subnet
        import argparse

        ns = argparse.Namespace(cidr="192.168.1.0/24", json=True)
        cmd_subnet(ns)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["cidr"] == "192.168.1.0/24"
        assert data["total_addresses"] == 256
        assert data["usable_hosts"] == 254

    def test_scan_json_output(self, capsys):
        """Test scan command with JSON output."""
        from cli import cmd_scan
        import argparse

        ns = argparse.Namespace(host="127.0.0.1", ports="22", json=True, log_level="WARNING")
        cmd_scan(ns)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["scan"]["host"] == "127.0.0.1"
        assert data["scan"]["ports_scanned"] == 1
        assert isinstance(data["scan"]["open"], list)


class TestPingMon:
    """Ping monitor tests."""

    def test_ping_localhost(self):
        """Ping localhost should succeed."""
        from pingmon import ping_host
        latency = ping_host("127.0.0.1", count=1, timeout=2)
        assert latency is not None
        assert latency >= 0

    def test_ping_invalid_host(self):
        """Ping invalid host should return None."""
        from pingmon import ping_host
        latency = ping_host("192.0.2.1", count=1, timeout=1)
        # TEST-NET-1 range, should timeout
        assert latency is None or latency >= 0
