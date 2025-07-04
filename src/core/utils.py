"""
Utility functions for Sniffy Enhanced
"""

import re
import os
import tempfile
import ipaddress
from pathlib import Path

def validate_target(target):
    """Validate target format (IP, CIDR, or domain)"""
    # IP address validation
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass
    
    # CIDR validation
    try:
        ipaddress.ip_network(target, strict=False)
        return True
    except ValueError:
        pass
    
    # Domain validation
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    if re.match(domain_pattern, target):
        return True
    
    return False

def setup_temp_directory():
    """Setup temporary directory for scan files"""
    temp_dir = tempfile.mkdtemp(prefix='sniffy_')
    return temp_dir

def is_port_open(host, port, timeout=3):
    """Check if a port is open"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_banner(host, port, timeout=3):
    """Get service banner"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner
    except:
        return ""

def resolve_hostname(target):
    """Resolve hostname to IP address"""
    import socket
    try:
        return socket.gethostbyname(target)
    except:
        return target

def format_duration(seconds):
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
