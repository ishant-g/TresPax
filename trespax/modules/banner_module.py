#!/usr/bin/env python3

import socket
import requests
from trespax.utils.colors import Colors


class BannerModule:
    """Banner grabbing module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config.user_agent})
        
        if self.config.use_tor and self.config.tor_proxy:
            self.session.proxies.update(self.config.tor_proxy)
    
    def run(self):
        """Run banner grabbing"""
        try:
            target = self.config.target
            results = {}
            
            # Resolve domain to IP if necessary
            if not self._is_ip(target):
                try:
                    target_ip = socket.gethostbyname(target)
                except:
                    return {"error": "Cannot resolve target to IP address"}
            else:
                target_ip = target
            
            # HTTP banner grabbing
            http_banner = self._grab_http_banner(target)
            if http_banner:
                results['http'] = http_banner
            
            # Service banner grabbing for common ports
            services = {
                21: 'FTP',
                22: 'SSH',
                25: 'SMTP',
                80: 'HTTP',
                110: 'POP3',
                143: 'IMAP',
                443: 'HTTPS',
                993: 'IMAPS',
                995: 'POP3S'
            }
            
            for port, service in services.items():
                if service in ['HTTP', 'HTTPS']:
                    continue  # Already handled above
                    
                banner = self._grab_service_banner(target_ip, port, service)
                if banner:
                    results[service.lower()] = banner
            
            if results and self.config.verbose:
                print(f"{Colors.GREEN}[+] Banner grabbing results:{Colors.RESET}")
                for service, banner in results.items():
                    print(f"    {service.upper()}: {banner}")
            
            return results if results else {"banners": []}
            
        except Exception as e:
            self.logger.error(f"Banner grabbing failed: {str(e)}")
            return {"error": str(e)}
    
    def _grab_http_banner(self, target):
        """Grab HTTP banner"""
        try:
            # Try HTTPS first, then HTTP
            urls = []
            if not target.startswith(('http://', 'https://')):
                urls = [f"https://{target}", f"http://{target}"]
            else:
                urls = [target]
            
            for url in urls:
                try:
                    response = self.session.head(url, timeout=5, verify=False)
                    
                    server = response.headers.get('Server', 'Unknown')
                    powered_by = response.headers.get('X-Powered-By', '')
                    
                    banner = server
                    if powered_by:
                        banner += f" (Powered by: {powered_by})"
                    
                    return banner
                    
                except:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _grab_service_banner(self, target_ip, port, service):
        """Grab banner from service port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                # Send appropriate command based on service
                if service == 'FTP':
                    pass  # FTP sends banner immediately
                elif service == 'SSH':
                    pass  # SSH sends banner immediately
                elif service == 'SMTP':
                    sock.send(b'HELO test\r\n')
                elif service in ['POP3', 'IMAP']:
                    pass  # These services send banner immediately
                
                # Receive banner
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                
                if banner:
                    return banner
            
            sock.close()
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