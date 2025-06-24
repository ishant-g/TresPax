#!/usr/bin/env python3

import whois
import socket
from trespax.utils.colors import Colors


class WhoisModule:
    """WHOIS lookup module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def run(self):
        """Run WHOIS lookup"""
        try:
            target = self.config.target
            
            # If target is an IP, get the domain first
            if self._is_ip(target):
                try:
                    target = socket.gethostbyaddr(target)[0]
                except:
                    return {"error": "Cannot perform WHOIS lookup on IP address without reverse DNS"}
            
            domain_info = whois.whois(target)
            
            result = {}
            
            if domain_info:
                # Extract relevant information
                fields = [
                    'domain_name', 'registrar', 'whois_server', 'referral_url',
                    'updated_date', 'creation_date', 'expiration_date',
                    'name_servers', 'status', 'emails', 'org', 'country'
                ]
                
                for field in fields:
                    value = getattr(domain_info, field, None)
                    if value:
                        if isinstance(value, list):
                            result[field] = [str(v) for v in value]
                        else:
                            result[field] = str(value)
                
                if self.config.verbose:
                    for key, value in result.items():
                        print(f"{Colors.GREEN}[+] {key}: {value}{Colors.RESET}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"WHOIS lookup failed: {str(e)}")
            return {"error": str(e)}
    
    def _is_ip(self, target):
        """Check if target is an IP address"""
        try:
            socket.inet_aton(target)
            return True
        except socket.error:
            return False