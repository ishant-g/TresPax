#!/usr/bin/env python3

import dns.resolver
import socket
from trespax.utils.colors import Colors


class DNSModule:
    """DNS enumeration module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def run(self):
        """Run DNS enumeration"""
        try:
            target = self.config.target
            results = {}
            
            # Record types to query
            record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 'PTR']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(target, record_type)
                    records = []
                    
                    for answer in answers:
                        records.append(str(answer))
                    
                    if records:
                        results[record_type] = records
                        
                        if self.config.verbose:
                            print(f"{Colors.GREEN}[+] {record_type} records found: {len(records)}{Colors.RESET}")
                            for record in records:
                                print(f"    {record}")
                
                except dns.resolver.NXDOMAIN:
                    if self.config.verbose:
                        print(f"{Colors.YELLOW}[!] Domain not found for {record_type}{Colors.RESET}")
                except dns.resolver.NoAnswer:
                    if self.config.verbose:
                        print(f"{Colors.YELLOW}[!] No {record_type} records found{Colors.RESET}")
                except Exception as e:
                    if self.config.verbose:
                        print(f"{Colors.RED}[!] Error querying {record_type}: {str(e)}{Colors.RESET}")
            
            # Try to get IP address if it's a domain
            if not self._is_ip(target):
                try:
                    ip = socket.gethostbyname(target)
                    results['IP'] = [ip]
                    
                    if self.config.verbose:
                        print(f"{Colors.GREEN}[+] Resolved IP: {ip}{Colors.RESET}")
                except:
                    pass
            
            return results
            
        except Exception as e:
            self.logger.error(f"DNS enumeration failed: {str(e)}")
            return {"error": str(e)}
    
    def _is_ip(self, target):
        """Check if target is an IP address"""
        try:
            socket.inet_aton(target)
            return True
        except socket.error:
            return False