#!/usr/bin/env python3

class Config:
    """Configuration class for TresPax"""
    
    def __init__(self):
        self.target = None
        self.verbose = False
        self.use_tor = False
        self.tor_proxy = None
        self.output_dir = None
        self.manual_mode = False
        self.timeout = 10
        self.threads = 50
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
        # Tool selection for manual mode
        self.selected_tools = {
            'whois': True,
            'dns': True,
            'subdomains': True,
            'ports': True,
            'directories': True,
            'headers': True,
            'emails': True,
            'banner': True,
            'robots': True,
            'ssl': True,
            'geolocation': True
        }
        
        # Wordlist paths
        self.wordlists = {
            'subdomains': [
                '/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt',
                '/usr/share/wordlists/dirb/common.txt',
                'wordlists/subdomains.txt'
            ],
            'directories': [
                '/usr/share/wordlists/dirb/common.txt',
                '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
                'wordlists/directories.txt'
            ],
            'passwords': [
                '/usr/share/wordlists/rockyou.txt',
                '/usr/share/wordlists/fasttrack.txt',
                'wordlists/passwords.txt'
            ]
        }