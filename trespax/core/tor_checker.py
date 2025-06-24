#!/usr/bin/env python3

import socket
import subprocess
import requests
from trespax.utils.colors import Colors


class TorChecker:
    """Check TOR service status and provide proxy configuration"""
    
    def __init__(self):
        self.tor_proxy = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
    
    def is_tor_running(self):
        """Check if TOR service is running"""
        try:
            # Method 1: Check if TOR port is open
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('127.0.0.1', 9050))
            sock.close()
            
            if result == 0:
                return True
            
            # Method 2: Check systemctl status
            try:
                result = subprocess.run(['systemctl', 'is-active', 'tor'], 
                                      capture_output=True, text=True, timeout=5)
                return result.stdout.strip() == 'active'
            except:
                pass
            
            # Method 3: Check process list
            try:
                result = subprocess.run(['pgrep', 'tor'], 
                                      capture_output=True, text=True, timeout=5)
                return bool(result.stdout.strip())
            except:
                pass
                
            return False
            
        except Exception:
            return False
    
    def get_tor_proxy(self):
        """Get TOR proxy configuration"""
        return self.tor_proxy
    
    def test_tor_connection(self):
        """Test TOR connection by checking IP"""
        try:
            # Get IP without TOR
            response_normal = requests.get('http://httpbin.org/ip', timeout=10)
            normal_ip = response_normal.json().get('origin', '')
            
            # Get IP with TOR
            response_tor = requests.get('http://httpbin.org/ip', 
                                     proxies=self.tor_proxy, timeout=10)
            tor_ip = response_tor.json().get('origin', '')
            
            return normal_ip != tor_ip and tor_ip != ''
            
        except Exception:
            return False