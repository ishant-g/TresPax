#!/usr/bin/env python3

import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from trespax.utils.colors import Colors


class PortModule:
    """Port scanning module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.open_ports = []
        
        # Common ports to scan
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
            1723, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 9090, 10000
        ]
    
    def run(self):
        """Run port scan"""
        try:
            target = self.config.target
            
            # Resolve domain to IP if necessary
            if not self._is_ip(target):
                try:
                    target_ip = socket.gethostbyname(target)
                except:
                    return {"error": "Cannot resolve target to IP address"}
            else:
                target_ip = target
            
            print(f"{Colors.CYAN}[*] Scanning {len(self.common_ports)} common ports on {target_ip}...{Colors.RESET}")
            
            # Use ThreadPoolExecutor for concurrent port scanning
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = []
                
                for port in self.common_ports:
                    future = executor.submit(self._scan_port, target_ip, port)
                    futures.append(future)
                
                # Wait for completion
                for future in futures:
                    try:
                        future.result(timeout=2)
                    except:
                        pass
            
            if self.open_ports:
                result = {"open_ports": sorted(self.open_ports)}
                
                if self.config.verbose:
                    print(f"{Colors.GREEN}[+] Found {len(self.open_ports)} open ports:{Colors.RESET}")
                    for port_info in sorted(self.open_ports):
                        print(f"    {port_info}")
                
                return result
            else:
                return {"open_ports": []}
                
        except Exception as e:
            self.logger.error(f"Port scan failed: {str(e)}")
            return {"error": str(e)}
    
    def _scan_port(self, target_ip, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                service = self._get_service_name(port)
                port_info = f"{port}/tcp - {service}"
                self.open_ports.append(port_info)
                
                if self.config.verbose:
                    print(f"{Colors.GREEN}[+] Open: {port_info}{Colors.RESET}")
            
            sock.close()
            
        except Exception:
            pass  # Port scan failed, skip
    
    def _get_service_name(self, port):
        """Get service name for port"""
        services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            111: "RPCbind",
            135: "MS-RPC",
            139: "NetBIOS-SSN",
            143: "IMAP",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
            1723: "PPTP",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP-Alt",
            8443: "HTTPS-Alt",
            8888: "HTTP-Alt",
            9090: "HTTP-Alt",
            10000: "Webmin"
        }
        
        return services.get(port, "Unknown")
    
    def _is_ip(self, target):
        """Check if target is an IP address"""
        try:
            socket.inet_aton(target)
            return True
        except socket.error:
            return False