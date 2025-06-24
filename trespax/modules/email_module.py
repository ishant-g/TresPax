#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
from trespax.utils.colors import Colors


class EmailModule:
    """Email and contact finder module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.found_emails = set()
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config.user_agent})
        
        if self.config.use_tor and self.config.tor_proxy:
            self.session.proxies.update(self.config.tor_proxy)
    
    def run(self):
        """Run email and contact finder"""
        try:
            target = self.config.target
            
            # Determine base URL
            if not target.startswith(('http://', 'https://')):
                urls = [f"https://{target}", f"http://{target}"]
            else:
                urls = [target]
            
            # Test connectivity and scrape emails
            working_url = None
            for url in urls:
                try:
                    response = self.session.get(url, timeout=self.config.timeout, verify=False)
                    if response.status_code == 200:
                        working_url = url
                        self._extract_emails(response.text, target)
                        break
                except:
                    continue
            
            if not working_url:
                return {"error": "Cannot connect to target"}
            
            # Try common pages
            common_pages = [
                '/contact', '/contact.html', '/contacts.html',
                '/about', '/about.html', '/about-us.html',
                '/team', '/team.html', '/staff.html',
                '/support', '/help', '/info'
            ]
            
            for page in common_pages:
                try:
                    full_url = working_url.rstrip('/') + page
                    response = self.session.get(full_url, timeout=5, verify=False)
                    
                    if response.status_code == 200:
                        self._extract_emails(response.text, target)
                        
                except:
                    continue
            
            if self.found_emails:
                result = {"emails": list(self.found_emails)}
                
                if self.config.verbose:
                    print(f"{Colors.GREEN}[+] Found {len(self.found_emails)} email addresses:{Colors.RESET}")
                    for email in self.found_emails:
                        print(f"    {email}")
                
                return result
            else:
                return {"emails": []}
                
        except Exception as e:
            self.logger.error(f"Email search failed: {str(e)}")
            return {"error": str(e)}
    
    def _extract_emails(self, content, domain):
        """Extract emails from content"""
        # Email regex patterns
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
        ]
        
        for pattern in email_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                email = match if isinstance(match, str) else match[0]
                # Filter out common false positives
                if not any(x in email.lower() for x in ['example.com', 'test.com', 'domain.com']):
                    self.found_emails.add(email)
        
        # Parse HTML for better extraction
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Look for mailto links
            mailto_links = soup.find_all('a', href=re.compile(r'^mailto:', re.I))
            for link in mailto_links:
                href = link.get('href', '')
                if href.startswith('mailto:'):
                    email = href[7:].split('?')[0]  # Remove mailto: and query params
                    if '@' in email:
                        self.found_emails.add(email)
            
            # Look for emails in text content
            text_content = soup.get_text()
            for pattern in email_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    email = match if isinstance(match, str) else match[0]
                    if not any(x in email.lower() for x in ['example.com', 'test.com', 'domain.com']):
                        self.found_emails.add(email)
                        
        except Exception:
            pass  # HTML parsing failed, continue with regex results