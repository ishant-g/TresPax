#!/usr/bin/env python3

import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from trespax.utils.colors import Colors
from trespax.utils.wordlist_manager import WordlistManager


class DirectoryModule:
    """Directory and file brute force module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.found_paths = []
        self.wordlist_manager = WordlistManager()
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config.user_agent})
        
        if self.config.use_tor and self.config.tor_proxy:
            self.session.proxies.update(self.config.tor_proxy)
    
    def run(self):
        """Run directory brute force"""
        try:
            target = self.config.target
            
            # Determine base URL
            if not target.startswith(('http://', 'https://')):
                # Try HTTPS first, then HTTP
                base_urls = [f"https://{target}", f"http://{target}"]
            else:
                base_urls = [target]
            
            # Test connectivity
            working_url = None
            for url in base_urls:
                try:
                    response = self.session.get(url, timeout=self.config.timeout, verify=False)
                    if response.status_code < 400:
                        working_url = url
                        break
                except:
                    continue
            
            if not working_url:
                return {"error": "Cannot connect to target"}
            
            print(f"{Colors.CYAN}[*] Using base URL: {working_url}{Colors.RESET}")
            
            # Get wordlist
            wordlist = self.wordlist_manager.get_wordlist('directories')
            if not wordlist:
                return {"error": "No directory wordlist found"}
            
            # Read wordlist
            try:
                with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception as e:
                return {"error": f"Failed to read wordlist: {str(e)}"}
            
            print(f"{Colors.CYAN}[*] Testing {min(len(paths), 500)} paths...{Colors.RESET}")
            
            # Use ThreadPoolExecutor for concurrent directory testing
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                
                for path in paths[:500]:  # Limit to first 500 for performance
                    full_url = urljoin(working_url, path)
                    future = executor.submit(self._test_path, full_url)
                    futures.append(future)
                
                # Wait for completion
                for future in futures:
                    try:
                        future.result(timeout=5)
                    except:
                        pass
            
            if self.found_paths:
                result = {"directories": self.found_paths}
                
                if self.config.verbose:
                    print(f"{Colors.GREEN}[+] Found {len(self.found_paths)} accessible paths:{Colors.RESET}")
                    for path_info in self.found_paths:
                        print(f"    {path_info}")
                
                return result
            else:
                return {"directories": []}
                
        except Exception as e:
            self.logger.error(f"Directory brute force failed: {str(e)}")
            return {"error": str(e)}
    
    def _test_path(self, url):
        """Test if path exists"""
        try:
            response = self.session.get(url, timeout=3, allow_redirects=False, verify=False)
            
            status_reasons = {
                200: "OK",
                201: "Created",
                202: "Accepted",
                204: "No Content",
                301: "Moved Permanently",
                302: "Found",
                403: "Forbidden",
                404: "Not Found",
                500: "Internal Server Error"
            }
            
            if response.status_code in [200, 201, 202, 204, 301, 302, 403]:
                reason = status_reasons.get(response.status_code, "Unknown")
                path_info = f"{url} [{response.status_code} - {reason}]"
                self.found_paths.append(path_info)
                
                if self.config.verbose:
                    color = Colors.GREEN if response.status_code < 300 else Colors.YELLOW
                    print(f"{color}[+] Found: {path_info}{Colors.RESET}")
                    
        except requests.exceptions.RequestException:
            pass  # Path test failed, skip
        except Exception:
            pass  # Other error, skip