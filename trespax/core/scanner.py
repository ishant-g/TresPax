#!/usr/bin/env python3

import os
import time
from trespax.modules.whois_module import WhoisModule
from trespax.modules.dns_module import DNSModule
from trespax.modules.subdomain_module import SubdomainModule
from trespax.modules.port_module import PortModule
from trespax.modules.directory_module import DirectoryModule
from trespax.modules.header_module import HeaderModule
from trespax.modules.email_module import EmailModule
from trespax.modules.banner_module import BannerModule
from trespax.modules.robots_module import RobotsModule
from trespax.modules.ssl_module import SSLModule
from trespax.modules.geolocation_module import GeolocationModule
from trespax.utils.colors import Colors


class Scanner:
    """Main scanner class that orchestrates all modules"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.results = {}

        # Initialize modules
        self.modules = {
            'whois': WhoisModule(config, logger),
            'dns': DNSModule(config, logger),
            'subdomains': SubdomainModule(config, logger),
            'ports': PortModule(config, logger),
            'directories': DirectoryModule(config, logger),
            'headers': HeaderModule(config, logger),
            'emails': EmailModule(config, logger),
            'banner': BannerModule(config, logger),
            'robots': RobotsModule(config, logger),
            'ssl': SSLModule(config, logger),
            'geolocation': GeolocationModule(config, logger)
        }
    
    def select_tools_manual(self):
        """Allow user to manually select tools"""
        print(f"\n{Colors.CYAN}[?] Select tools to run:{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Press Enter to toggle, 'a' for all, 'n' for none, 'q' to continue{Colors.RESET}\n")
        
        tool_descriptions = {
            'whois': 'WHOIS Lookup - Domain registration information',
            'dns': 'DNS Enumeration - DNS records (A, AAAA, CNAME, MX, NS, TXT, SOA)',
            'subdomains': 'Subdomain Brute Force - Find subdomains using wordlists',
            'ports': 'Port Scanning - Identify open ports and services',
            'directories': 'Directory Busting - Find hidden directories and files',
            'headers': 'HTTP Header Analysis - Analyze HTTP headers and detect technologies',
            'emails': 'Email & Contact Finder - Extract email addresses from pages',
            'banner': 'Banner Grabbing - Extract server information and versions',
            'robots': 'Robots.txt & Sitemap Parser - Analyze robots.txt and sitemap.xml',
            'ssl': 'SSL/TLS Analysis - Analyze SSL certificate and configuration',
            'geolocation': 'IP Geolocation - Get geographical location of IP'
        }
        
        while True:
            for i, (tool, desc) in enumerate(tool_descriptions.items(), 1):
                status = f"{Colors.GREEN}[✓]" if self.config.selected_tools[tool] else f"{Colors.RED}[✗]"
                print(f"{status} {i:2d}. {desc}{Colors.RESET}")
            
            print(f"\n{Colors.CYAN}Selected: {sum(self.config.selected_tools.values())}/{len(self.config.selected_tools)} tools{Colors.RESET}")
            choice = input(f"\n{Colors.CYAN}[?] Enter tool number (1-{len(tool_descriptions)}), 'a' (all), 'n' (none), or 'q' (quit): {Colors.RESET}").strip().lower()
            
            if choice == 'q':
                break
            elif choice == 'a':
                for tool in self.config.selected_tools:
                    self.config.selected_tools[tool] = True
            elif choice == 'n':
                for tool in self.config.selected_tools:
                    self.config.selected_tools[tool] = False
            elif choice.isdigit() and 1 <= int(choice) <= len(tool_descriptions):
                tool_name = list(tool_descriptions.keys())[int(choice) - 1]
                self.config.selected_tools[tool_name] = not self.config.selected_tools[tool_name]
            
            print("\n" + "=" * 80)

    def save_partial_result(self, module_name, result):
        """Save result of a module to its own file"""
        if not self.config.output_dir:
            return
        
        try:
            filepath = os.path.join(self.config.output_dir, f"{module_name}.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                if isinstance(result, dict):
                    for k, v in result.items():
                        f.write(f"{k}: {v}\n")
                elif isinstance(result, list):
                    for item in result:
                        f.write(f"{item}\n")
                else:
                    f.write(str(result))
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to save {module_name} result: {e}{Colors.RESET}")

    def show_result_inline(self, module_name, result):
        """Print result of a module on screen"""
        print(f"\n{Colors.MAGENTA}--- {module_name.upper()} RESULTS ---{Colors.RESET}")
        
        if not result:
            print(f"{Colors.YELLOW}[!] No data returned for {module_name}{Colors.RESET}")
            return
        
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{Colors.CYAN}{key}:{Colors.RESET} {value}")
        elif isinstance(result, list):
            for item in result:
                print(f"{Colors.GREEN}- {item}{Colors.RESET}")
        else:
            print(f"{Colors.WHITE}{str(result)}{Colors.RESET}")

    def run(self):
        """Run the selected scanning modules"""
        print(f"\n{Colors.BLUE}[*] Starting TresPax scan on target: {self.config.target}{Colors.RESET}")

        if self.config.use_tor:
            print(f"{Colors.YELLOW}[*] Using TOR network for anonymity{Colors.RESET}")
        
        if self.config.manual_mode:
            self.select_tools_manual()

        start_time = time.time()

        for module_name, module in self.modules.items():
            if self.config.selected_tools.get(module_name, True):
                print(f"\n{Colors.CYAN}[*] Running {module_name.upper()} module...{Colors.RESET}")
                try:
                    result = module.run()
                    self.results[module_name] = result

                    self.show_result_inline(module_name, result)
                    self.save_partial_result(module_name, result)

                    if result and self.config.verbose:
                        print(f"{Colors.GREEN}[+] {module_name.upper()} completed successfully{Colors.RESET}")
                    elif not result:
                        print(f"{Colors.YELLOW}[!] {module_name.upper()} completed but returned no data{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[!] Error in {module_name} module: {str(e)}{Colors.RESET}")
                    if self.config.verbose:
                        import traceback
                        traceback.print_exc()
                    self.results[module_name] = None

        end_time = time.time()
        duration = end_time - start_time
        print(f"\n{Colors.GREEN}[+] Scan completed in {duration:.2f} seconds{Colors.RESET}")

        return self.results
