#!/usr/bin/env python3

import sys
from datetime import datetime
from trespax.utils.colors import Colors


class Logger:
    """Simple logger for TresPax"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def info(self, message):
        """Log info message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.CYAN}[{timestamp}] [INFO] {message}{Colors.RESET}")
    
    def success(self, message):
        """Log success message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.GREEN}[{timestamp}] [SUCCESS] {message}{Colors.RESET}")
    
    def warning(self, message):
        """Log warning message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.YELLOW}[{timestamp}] [WARNING] {message}{Colors.RESET}")
    
    def error(self, message):
        """Log error message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.RED}[{timestamp}] [ERROR] {message}{Colors.RESET}", file=sys.stderr)
    
    def debug(self, message):
        """Log debug message (only in verbose mode)"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{Colors.BLUE}[{timestamp}] [DEBUG] {message}{Colors.RESET}")
    
    def verbose_print(self, message):
        """Print message only in verbose mode"""
        if self.verbose:
            print(message)