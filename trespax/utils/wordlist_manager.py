#!/usr/bin/env python3

import os
from pathlib import Path


class WordlistManager:
    """Manage wordlists for TresPax"""
    
    def __init__(self):
        self.wordlist_paths = {
            'subdomains': [
                '/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt',
                '/usr/share/wordlists/seclists/Discovery/DNS/fierce-hostlist.txt',
                '/usr/share/wordlists/dirb/common.txt',
                'wordlists/subdomains.txt',
                'subdomains.txt'
            ],
            'directories': [
                '/usr/share/wordlists/dirb/common.txt',
                '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
                '/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt',
                'wordlists/directories.txt',
                'directories.txt'
            ],
            'passwords': [
                '/usr/share/wordlists/rockyou.txt',
                '/usr/share/wordlists/fasttrack.txt',
                '/usr/share/wordlists/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt',
                'wordlists/passwords.txt',
                'passwords.txt'
            ]
        }
    
    def get_wordlist(self, wordlist_type):
        """Get the first available wordlist of the specified type"""
        if wordlist_type not in self.wordlist_paths:
            return None
        
        for wordlist_path in self.wordlist_paths[wordlist_type]:
            if os.path.isfile(wordlist_path):
                return wordlist_path
        
        # If no system wordlists found, create a basic one
        return self._create_basic_wordlist(wordlist_type)
    
    def _create_basic_wordlist(self, wordlist_type):
        """Create a basic wordlist if none found"""
        try:
            # Create wordlists directory
            os.makedirs('wordlists', exist_ok=True)
            
            wordlist_file = f'wordlists/{wordlist_type}.txt'
            
            if wordlist_type == 'subdomains':
                basic_subdomains = [
                    'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging',
                    'api', 'blog', 'shop', 'store', 'secure', 'portal',
                    'support', 'help', 'news', 'media', 'static', 'assets',
                    'cdn', 'img', 'images', 'files', 'download', 'uploads'
                ]
                
                with open(wordlist_file, 'w') as f:
                    f.write('\n'.join(basic_subdomains))
            
            elif wordlist_type == 'directories':
                basic_directories = [
                    'admin', 'administrator', 'login', 'wp-admin', 'phpmyadmin',
                    'backup', 'backups', 'config', 'test', 'dev', 'staging',
                    'api', 'files', 'uploads', 'images', 'img', 'assets',
                    'css', 'js', 'scripts', 'includes', 'tmp', 'temp'
                ]
                
                with open(wordlist_file, 'w') as f:
                    f.write('\n'.join(basic_directories))
            
            elif wordlist_type == 'passwords':
                basic_passwords = [
                    'password', '123456', 'admin', 'root', 'test', 'guest',
                    'password123', '12345678', 'qwerty', 'abc123', 'letmein',
                    'welcome', 'monkey', '1234567890', 'password1'
                ]
                
                with open(wordlist_file, 'w') as f:
                    f.write('\n'.join(basic_passwords))
            
            if os.path.isfile(wordlist_file):
                return wordlist_file
            
        except Exception:
            pass
        
        return None