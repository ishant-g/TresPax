#!/usr/bin/env python3

import ssl
import socket
from datetime import datetime
import requests
from trespax.utils.colors import Colors


class SSLModule:
    """SSL/TLS analysis module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def run(self):
        """Run SSL/TLS analysis"""
        try:
            target = self.config.target
            
            # Skip if target is just an IP without HTTPS indication
            if self._is_ip(target):
                target_host = target
                port = 443
            else:
                target_host = target
                port = 443
            
            # Get SSL certificate info
            cert_info = self._get_ssl_certificate(target_host, port)
            
            if cert_info:
                result = {
                    'certificate': cert_info,
                    'ssl_labs_grade': self._check_ssl_labs(target_host) if not self._is_ip(target) else None
                }
                
                if self.config.verbose:
                    print(f"{Colors.GREEN}[+] SSL Certificate Info:{Colors.RESET}")
                    print(f"    Subject: {cert_info.get('subject', 'Unknown')}")
                    print(f"    Issuer: {cert_info.get('issuer', 'Unknown')}")
                    print(f"    Valid From: {cert_info.get('not_before', 'Unknown')}")
                    print(f"    Valid To: {cert_info.get('not_after', 'Unknown')}")
                    print(f"    Days Until Expiry: {cert_info.get('days_until_expiry', 'Unknown')}")
                
                return result
            else:
                return {"error": "No SSL certificate found or connection failed"}
                
        except Exception as e:
            self.logger.error(f"SSL analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def _get_ssl_certificate(self, hostname, port=443):
        """Get SSL certificate information"""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        # Parse certificate information
                        subject = dict(x[0] for x in cert.get('subject', []))
                        issuer = dict(x[0] for x in cert.get('issuer', []))
                        
                        # Parse dates
                        not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        
                        # Calculate days until expiry
                        days_until_expiry = (not_after - datetime.now()).days
                        
                        return {
                            'subject': subject.get('commonName', 'Unknown'),
                            'issuer': issuer.get('organizationName', issuer.get('commonName', 'Unknown')),
                            'not_before': not_before.strftime('%Y-%m-%d %H:%M:%S'),
                            'not_after': not_after.strftime('%Y-%m-%d %H:%M:%S'),
                            'days_until_expiry': days_until_expiry,
                            'serial_number': cert.get('serialNumber', 'Unknown'),
                            'version': cert.get('version', 'Unknown'),
                            'subject_alt_names': [x[1] for x in cert.get('subjectAltName', [])]
                        }
            
            return None
            
        except Exception:
            return None
    
    def _check_ssl_labs(self, hostname):
        """Check SSL Labs rating (simplified)"""
        try:
            # This is a simplified check - in reality you'd use SSL Labs API
            # For now, we'll do a basic SSL handshake test
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher = ssock.cipher()
                    protocol = ssock.version()
                    
                    # Basic grading based on protocol and cipher
                    if protocol == 'TLSv1.3':
                        grade = 'A'
                    elif protocol == 'TLSv1.2':
                        if cipher and 'AES' in cipher[0]:
                            grade = 'A-'
                        else:
                            grade = 'B'
                    elif protocol in ['TLSv1.1', 'TLSv1']:
                        grade = 'C'
                    else:
                        grade = 'F'
                    
                    return {
                        'grade': grade,
                        'protocol': protocol,
                        'cipher': cipher[0] if cipher else 'Unknown'
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