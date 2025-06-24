#!/usr/bin/env python3

import pyfiglet
from trespax.utils.colors import Colors


def show_banner():
    """Display the TresPax banner"""
    
    # Create ASCII art banner
    banner_text = pyfiglet.figlet_format("TresPax", font="slant")
    
    print(f"{Colors.RED}")
    print("🔥" + "="*60 + "🔥")
    print(f"{Colors.BOLD}{Colors.RED}           IXEDGE FORGE PRESENTS{Colors.RESET}")
    print(f"{Colors.CYAN}{banner_text}{Colors.RESET}")
    print(f"{Colors.YELLOW}    🛠️  The One-Tool Recon & Enumeration Framework{Colors.RESET}")
    print(f"{Colors.GREEN}                    Version 1.0.0{Colors.RESET}")
    print(f"{Colors.RED}" + "="*62 + f"{Colors.RESET}")
    print()
    print(f"{Colors.MAGENTA}[*] Designed for Penetration Testers & Ethical Hackers{Colors.RESET}")
    print(f"{Colors.MAGENTA}[*] Offline-Capable | TOR Support | Modular Framework{Colors.RESET}")
    print(f"{Colors.MAGENTA}[*] Created by IXEDGE FORGE{Colors.RESET}")
    print()
    print(f"{Colors.CYAN}{'='*62}{Colors.RESET}")
    print()