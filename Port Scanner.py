#!/usr/bin/env python3

import ipaddress
import socket
import sys

PORT_MIN = 0
PORT_MAX = 65535


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        try:
            # Attempt to resolve the input as a domain name
            socket.gethostbyname(ip)
            return True
        except socket.gaierror:
            return False


def parse_port_range(port_range):
    if "-" in port_range:
        start_port, end_port = map(int, port_range.split("-"))
        if PORT_MIN <= start_port <= end_port <= PORT_MAX:
            return list(range(start_port, end_port + 1))
    elif PORT_MIN <= int(port_range) <= PORT_MAX:
        return [int(port_range)]
    return None


def scan_ports(host_ip, ports):
    open_ports_found = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host_ip, port))
            if result == 0:
                print(f"Port {port} is open")
                open_ports_found.append(port)
            else:
                print(f"Port {port} is closed")
    return open_ports_found


try:
    host_ip = input("Enter the IP or domain you want to scan: ")
    if not is_valid_ip(host_ip):
        print("Invalid IP address or domain name")
        sys.exit()

    port_check = input("Enter Port Number or Port Range: ")
    port_range = parse_port_range(port_check)
    if port_range:
        host_ip = socket.gethostbyname(host_ip)
        open_ports_found = scan_ports(host_ip, port_range)
        input(f"Port scan finished. Found open Ports: {open_ports_found}\nPress Enter to exit...")
    else:
        print("Invalid port range")
except KeyboardInterrupt:
    print("\nScan aborted by user.")
except Exception as e:
    print(f"Error running Script: {e}")
