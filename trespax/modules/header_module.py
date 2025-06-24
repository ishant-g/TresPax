#!/usr/bin/env python3

import requests
from trespax.utils.colors import Colors


class HeaderModule:
    """HTTP header analysis module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config.user_agent})
        
        if self.config.use_tor and self.config.tor_proxy:
            self.session.proxies.update(self.config.tor_proxy)
    
    def run(self):
        """Run HTTP header analysis"""
        try:
            target = self.config.target
            
            # Determine base URL
            if not target.startswith(('http://', 'https://')):
                # Try HTTPS first, then HTTP
                urls = [f"https://{target}", f"http://{target}"]
            else:
                urls = [target]
            
            # Test connectivity and get headers
            for url in urls:
                try:
                    response = self.session.get(url, timeout=self.config.timeout, verify=False)
                    
                    result = {
                        "url": url,
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "technologies": self._detect_technologies(response.headers),
                        "security_headers": self._analyze_security_headers(response.headers)
                    }
                    
                    if self.config.verbose:
                        print(f"{Colors.GREEN}[+] URL: {url}{Colors.RESET}")
                        print(f"{Colors.GREEN}[+] Status Code: {response.status_code}{Colors.RESET}")
                        
                        if result["technologies"]:
                            print(f"{Colors.GREEN}[+] Technologies detected:{Colors.RESET}")
                            for tech in result["technologies"]:
                                print(f"    {tech}")
                        
                        if result["security_headers"]["missing"]:
                            print(f"{Colors.YELLOW}[!] Missing security headers:{Colors.RESET}")
                            for header in result["security_headers"]["missing"]:
                                print(f"    {header}")
                    
                    return result
                    
                except requests.exceptions.RequestException:
                    continue
            
            return {"error": "Cannot connect to target"}
            
        except Exception as e:
            self.logger.error(f"Header analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def _detect_technologies(self, headers):
        """Detect technologies from headers"""
        technologies = []
        
        # Server detection
        server = headers.get('Server', '').lower()
        if 'nginx' in server:
            technologies.append(f"Web Server: Nginx {server}")
        elif 'apache' in server:
            technologies.append(f"Web Server: Apache {server}")
        elif 'iis' in server:
            technologies.append(f"Web Server: IIS {server}")
        elif 'cloudflare' in server:
            technologies.append("CDN: Cloudflare")
        
        # Framework detection
        framework_headers = {
            'x-powered-by': 'Framework',
            'x-aspnet-version': 'ASP.NET',
            'x-generator': 'Generator',
            'x-drupal-cache': 'Drupal CMS',
            'x-varnish': 'Varnish Cache'
        }
        
        for header, tech in framework_headers.items():
            value = headers.get(header)
            if value:
                technologies.append(f"{tech}: {value}")
        
        # Security/CDN detection
        if headers.get('cf-ray'):
            technologies.append("CDN: Cloudflare")
        if headers.get('x-amz-cf-id'):
            technologies.append("CDN: Amazon CloudFront")
        if headers.get('x-azure-ref'):
            technologies.append("Cloud: Microsoft Azure")
        
        return technologies
    
    def _analyze_security_headers(self, headers):
        """Analyze security headers"""
        security_headers = [
            'strict-transport-security',
            'content-security-policy',
            'x-frame-options',
            'x-content-type-options',
            'x-xss-protection',
            'referrer-policy'
        ]
        
        present = []
        missing = []
        
        for header in security_headers:
            if header in headers:
                present.append(f"{header}: {headers[header]}")
            else:
                missing.append(header)
        
        return {
            "present": present,
            "missing": missing
        }