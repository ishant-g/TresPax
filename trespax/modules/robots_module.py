#!/usr/bin/env python3

import requests
from urllib.parse import urljoin
from trespax.utils.colors import Colors


class RobotsModule:
    """Robots.txt and sitemap.xml parser module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config.user_agent})
        
        if self.config.use_tor and self.config.tor_proxy:
            self.session.proxies.update(self.config.tor_proxy)
    
    def run(self):
        """Run robots.txt and sitemap analysis"""
        try:
            target = self.config.target
            results = {}
            
            # Determine base URL
            if not target.startswith(('http://', 'https://')):
                urls = [f"https://{target}", f"http://{target}"]
            else:
                urls = [target]
            
            # Find working URL
            working_url = None
            for url in urls:
                try:
                    response = self.session.get(url, timeout=self.config.timeout, verify=False)
                    if response.status_code < 400:
                        working_url = url
                        break
                except:
                    continue
            
            if not working_url:
                return {"error": "Cannot connect to target"}
            
            # Check robots.txt
            robots_result = self._check_robots_txt(working_url)
            if robots_result:
                results['robots_txt'] = robots_result
            
            # Check sitemap.xml
            sitemap_result = self._check_sitemap(working_url)
            if sitemap_result:
                results['sitemap'] = sitemap_result
            
            # Check other common files
            common_files = [
                'security.txt', '.well-known/security.txt',
                'humans.txt', 'crossdomain.xml', 'clientaccesspolicy.xml'
            ]
            
            found_files = []
            for file_path in common_files:
                file_url = urljoin(working_url, file_path)
                try:
                    response = self.session.get(file_url, timeout=5, verify=False)
                    if response.status_code == 200:
                        found_files.append(file_path)
                        
                        if self.config.verbose:
                            print(f"{Colors.GREEN}[+] Found: {file_path}{Colors.RESET}")
                except:
                    continue
            
            if found_files:
                results['other_files'] = found_files
            
            return results if results else {"files": []}
            
        except Exception as e:
            self.logger.error(f"Robots/Sitemap analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def _check_robots_txt(self, base_url):
        """Check robots.txt file"""
        try:
            robots_url = urljoin(base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=5, verify=False)
            
            if response.status_code == 200:
                content = response.text
                
                # Parse robots.txt
                disallowed_paths = []
                allowed_paths = []
                sitemaps = []
                
                for line in content.split('\n'):
                    line = line.strip()
                    
                    if line.lower().startswith('disallow:'):
                        path = line.split(':', 1)[1].strip()
                        if path and path != '/':
                            disallowed_paths.append(path)
                    
                    elif line.lower().startswith('allow:'):
                        path = line.split(':', 1)[1].strip()
                        if path:
                            allowed_paths.append(path)
                    
                    elif line.lower().startswith('sitemap:'):
                        sitemap = line.split(':', 1)[1].strip()
                        if sitemap:
                            sitemaps.append(sitemap)
                
                result = {
                    'url': robots_url,
                    'content_length': len(content),
                    'disallowed_paths': disallowed_paths,
                    'allowed_paths': allowed_paths,
                    'sitemaps': sitemaps
                }
                
                if self.config.verbose:
                    print(f"{Colors.GREEN}[+] robots.txt found with {len(disallowed_paths)} disallowed paths{Colors.RESET}")
                    if disallowed_paths:
                        for path in disallowed_paths[:10]:  # Show first 10
                            print(f"    Disallowed: {path}")
                
                return result
            
            return None
            
        except Exception:
            return None
    
    def _check_sitemap(self, base_url):
        """Check sitemap.xml file"""
        try:
            sitemap_urls = [
                urljoin(base_url, '/sitemap.xml'),
                urljoin(base_url, '/sitemap_index.xml'),
                urljoin(base_url, '/sitemaps.xml')
            ]
            
            for sitemap_url in sitemap_urls:
                try:
                    response = self.session.get(sitemap_url, timeout=5, verify=False)
                    
                    if response.status_code == 200:
                        content = response.text
                        
                        # Count URLs in sitemap
                        url_count = content.lower().count('<url>')
                        sitemap_count = content.lower().count('<sitemap>')
                        
                        result = {
                            'url': sitemap_url,
                            'content_length': len(content),
                            'url_count': url_count,
                            'sitemap_count': sitemap_count
                        }
                        
                        if self.config.verbose:
                            print(f"{Colors.GREEN}[+] Sitemap found: {sitemap_url}{Colors.RESET}")
                            print(f"    URLs: {url_count}, Sitemaps: {sitemap_count}")
                        
                        return result
                        
                except:
                    continue
            
            return None
            
        except Exception:
            return None