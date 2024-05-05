#!/usr/bin/env python3

import socket
import ipaddress

PORT_MIN = 0
PORT_MAX = 65535

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
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
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                if s.connect_ex((host_ip, port)) == 0:
                    print(f'Port {port} is open')
                else:
                    print(f'Port {port} is closed')
        except Exception as e:
            print(f'Error trying to scan port {port}: {e}')

host_ip = input("Enter the IP you want to scan: ")
if not is_valid_ip(host_ip):
    print('Invalid IP address')

port_check = input("Enter Port Number or Port Range: ")
port_range = parse_port_range(port_check)
if port_range:
    scan_ports(host_ip, port_range)
else:
    print('Invalid port range')

