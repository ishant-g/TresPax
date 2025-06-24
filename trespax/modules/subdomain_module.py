#!/usr/bin/env python3

import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from trespax.utils.colors import Colors
from trespax.utils.wordlist_manager import WordlistManager


class SubdomainModule:
    """Subdomain brute force module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.found_subdomains = []
        self.wordlist_manager = WordlistManager()
    
    def run(self):
        """Run subdomain brute force"""
        try:
            target = self.config.target
            
            # Skip if target is an IP
            if self._is_ip(target):
                return {"error": "Cannot perform subdomain enumeration on IP address"}
            
            # Get wordlist
            wordlist = self.wordlist_manager.get_wordlist('subdomains')
            if not wordlist:
                return {"error": "No subdomain wordlist found"}
            
            print(f"{Colors.CYAN}[*] Using wordlist: {wordlist}{Colors.RESET}")
            
            # Read wordlist
            try:
                with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    subdomains = [line.strip() for line in f if line.strip()]
            except Exception as e:
                return {"error": f"Failed to read wordlist: {str(e)}"}
            
            print(f"{Colors.CYAN}[*] Testing {len(subdomains)} subdomains...{Colors.RESET}")
            
            # Use ThreadPoolExecutor for concurrent subdomain testing
            with ThreadPoolExecutor(max_workers=self.config.threads) as executor:
                futures = []
                
                for subdomain in subdomains[:1000]:  # Limit to first 1000 for performance
                    full_domain = f"{subdomain}.{target}"
                    future = executor.submit(self._test_subdomain, full_domain)
                    futures.append(future)
                
                # Wait for completion
                for future in futures:
                    try:
                        future.result(timeout=1)
                    except:
                        pass
            
            if self.found_subdomains:
                result = {"subdomains": self.found_subdomains}
                
                if self.config.verbose:
                    print(f"{Colors.GREEN}[+] Found {len(self.found_subdomains)} subdomains:{Colors.RESET}")
                    for subdomain in self.found_subdomains:
                        print(f"    {subdomain}")
                
                return result
            else:
                return {"subdomains": []}
                
        except Exception as e:
            self.logger.error(f"Subdomain enumeration failed: {str(e)}")
            return {"error": str(e)}
    
    def _test_subdomain(self, subdomain):
        """Test if subdomain exists"""
        try:
            ip = socket.gethostbyname(subdomain)
            self.found_subdomains.append(f"{subdomain} -> {ip}")
            
            if self.config.verbose:
                print(f"{Colors.GREEN}[+] Found: {subdomain} -> {ip}{Colors.RESET}")
                
        except socket.gaierror:
            pass  # Subdomain doesn't exist
        except Exception:
            pass  # Other error, skip
    
    def _is_ip(self, target):
        """Check if target is an IP address"""
        try:
            socket.inet_aton(target)
            return True
        except socket.error:
            return False