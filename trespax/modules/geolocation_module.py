#!/usr/bin/env python3

import socket
import requests
from trespax.utils.colors import Colors


class GeolocationModule:
    """IP geolocation module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        self.session = requests.Session()
        if self.config.use_tor and self.config.tor_proxy:
            self.session.proxies.update(self.config.tor_proxy)
    
    def run(self):
        """Run IP geolocation"""
        try:
            target = self.config.target
            
            # Get IP address
            if self._is_ip(target):
                target_ip = target
            else:
                try:
                    target_ip = socket.gethostbyname(target)
                except:
                    return {"error": "Cannot resolve target to IP address"}
            
            # Skip private/local IPs
            if self._is_private_ip(target_ip):
                return {"error": "Cannot geolocate private/local IP addresses"}
            
            # Try multiple geolocation services
            geolocation_services = [
                self._geolocate_ipapi,
                self._geolocate_httpbin,
                self._geolocate_ipinfo
            ]
            
            for service in geolocation_services:
                try:
                    result = service(target_ip)
                    if result:
                        if self.config.verbose:
                            print(f"{Colors.GREEN}[+] Geolocation for {target_ip}:{Colors.RESET}")
                            for key, value in result.items():
                                print(f"    {key}: {value}")
                        
                        return result
                except:
                    continue
            
            return {"error": "Geolocation services unavailable"}
            
        except Exception as e:
            self.logger.error(f"Geolocation failed: {str(e)}")
            return {"error": str(e)}
    
    def _geolocate_ipapi(self, ip):
        """Use ip-api.com for geolocation"""
        try:
            url = f"http://ip-api.com/json/{ip}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    return {
                        'ip': ip,
                        'country': data.get('country', 'Unknown'),
                        'country_code': data.get('countryCode', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'latitude': data.get('lat', 'Unknown'),
                        'longitude': data.get('lon', 'Unknown'),
                        'timezone': data.get('timezone', 'Unknown'),
                        'isp': data.get('isp', 'Unknown'),
                        'organization': data.get('org', 'Unknown'),
                        'service': 'ip-api.com'
                    }
            
            return None
            
        except Exception:
            return None
    
    def _geolocate_httpbin(self, ip):
        """Use httpbin.org for basic IP info"""
        try:
            url = "http://httpbin.org/ip"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'ip': data.get('origin', ip),
                    'service': 'httpbin.org'
                }
            
            return None
            
        except Exception:
            return None
    
    def _geolocate_ipinfo(self, ip):
        """Use ipinfo.io for geolocation"""
        try:
            url = f"http://ipinfo.io/{ip}/json"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                location = data.get('loc', '').split(',')
                
                return {
                    'ip': ip,
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'latitude': location[0] if len(location) > 0 else 'Unknown',
                    'longitude': location[1] if len(location) > 1 else 'Unknown',
                    'organization': data.get('org', 'Unknown'),
                    'postal': data.get('postal', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown'),
                    'service': 'ipinfo.io'
                }
            
            return None
            
        except Exception:
            return None
    
    def _is_ip(self, target):
        """Check if target is an IP address"""
        try:
            socket.inet_aton(target)
            return True
        except socket.error:
            return False
    
    def _is_private_ip(self, ip):
        """Check if IP is private/local"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            # Convert to integers
            parts = [int(part) for part in parts]
            
            # Check private ranges
            if parts[0] == 10:  # 10.0.0.0/8
                return True
            elif parts[0] == 172 and 16 <= parts[1] <= 31:  # 172.16.0.0/12
                return True
            elif parts[0] == 192 and parts[1] == 168:  # 192.168.0.0/16
                return True
            elif parts[0] == 127:  # 127.0.0.0/8 (localhost)
                return True
            
            return False
            
        except Exception:
            return True  # Assume private if parsing fails