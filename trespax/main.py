#!/usr/bin/env python3

import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

# Try to import signal, but handle gracefully if not available
try:
    import signal
    SIGNAL_AVAILABLE = True
except ImportError:
    SIGNAL_AVAILABLE = False
    print("Warning: Signal handling not available in this environment")

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add the parent directory to sys.path to import trespax modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from trespax.core.banner import show_banner
from trespax.core.config import Config
from trespax.core.tor_checker import TorChecker
from trespax.core.scanner import Scanner
from trespax.core.reporter import Reporter
from trespax.utils.colors import Colors
from trespax.utils.logger import Logger


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n{Colors.YELLOW}[!] Scan interrupted by user{Colors.RESET}")
    sys.exit(0)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="TresPax - The One-Tool Recon & Enumeration Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  trespax -t example.com                    # Basic scan
  trespax -t example.com --tor             # Scan through TOR
  trespax -t example.com -v                # Verbose mode
  trespax -t example.com -o /tmp/results   # Custom output directory
  trespax -t example.com --manual          # Manual tool selection
        """
    )

    parser.add_argument('-t', '--target', help='Target domain or IP address', required=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--tor', action='store_true', help='Use TOR network for anonymity')
    parser.add_argument('-o', '--output', help='Output directory for results')
    parser.add_argument('--manual', action='store_true', help='Manual tool selection mode')
    parser.add_argument('--no-banner', action='store_true', help='Disable banner display')
    parser.add_argument('--version', action='version', version='TresPax 1.0.0')
    return parser.parse_args()


def get_target_interactive():
    """Get target from user input"""
    while True:
        target = input(f"{Colors.CYAN}[?] Enter target domain or IP: {Colors.RESET}").strip()
        if target:
            return target
        print(f"{Colors.RED}[!] Please enter a valid target{Colors.RESET}")


def ask_yes_no(question, default=False):
    """Ask yes/no question"""
    default_str = "Y/n" if default else "y/N"
    while True:
        response = input(f"{Colors.CYAN}[?] {question} [{default_str}]: {Colors.RESET}").strip().lower()
        if not response:
            return default
        elif response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print(f"{Colors.RED}[!] Please enter 'y' or 'n'{Colors.RESET}")


def is_root():
    """Check if script is running as root"""
    return os.geteuid() == 0


def main():
    """Main entry point"""
    if SIGNAL_AVAILABLE:
        signal.signal(signal.SIGINT, signal_handler)

    args = parse_arguments()

    if not args.no_banner:
        show_banner()
        print(f"{Colors.YELLOW}[!] Disclaimer: Use this tool only on systems you own or have permission to test.{Colors.RESET}")
        print(f"{Colors.YELLOW}🔒 Note: Saving reports requires sudo/root access to write to secure directories.{Colors.RESET}")

    config = Config()

    # Get target
    config.target = args.target or get_target_interactive()
    config.verbose = args.verbose
    logger = Logger(config.verbose)

    # TOR
    config.use_tor = args.tor or ask_yes_no("Do you want to use TOR for anonymity?", False)
    if config.use_tor:
        tor_checker = TorChecker()
        if not tor_checker.is_tor_running():
            print(f"{Colors.RED}[!] TOR service is not active. Please start TOR service first.{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Run: sudo systemctl start tor{Colors.RESET}")
            sys.exit(1)
        print(f"{Colors.GREEN}[+] TOR service is active. Routing traffic through TOR.{Colors.RESET}")
        config.tor_proxy = tor_checker.get_tor_proxy()

    # SUDO check
    has_root = is_root()
    can_save = False
    if has_root:
        can_save = True
    else:
        print(f"{Colors.YELLOW}🔒 Saving scan results requires sudo/root access.{Colors.RESET}")
        wants_sudo = ask_yes_no("Do you want to provide sudo/root access to save the results?", False)
        if wants_sudo:
            print(f"{Colors.RED}[!] Please restart the tool using: sudo python3 main.py{Colors.RESET}")
            sys.exit(1)
        else:
            print(f"{Colors.YELLOW}[!] Scan results will not be saved.{Colors.RESET}")

    # Output dir
    if can_save:
        if args.output:
            config.output_dir = args.output
        else:
            save_results = ask_yes_no("Do you want to save scan results?", True)
            if save_results:
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
                config.output_dir = f"reports/{config.target}_{timestamp}"
        if config.output_dir:
            try:
                os.makedirs(config.output_dir, exist_ok=True)
                print(f"{Colors.GREEN}[+] Results will be saved to: {config.output_dir}{Colors.RESET}")
            except PermissionError:
                print(f"{Colors.RED}[!] Cannot write to {config.output_dir}. Check permissions.{Colors.RESET}")
                sys.exit(1)

    config.manual_mode = args.manual

    try:
        # Start scan
        print(f"\n[*] Starting TresPax scan on target: {config.target}")
        if config.use_tor:
            print("[*] Using TOR network for anonymity\n")

        scanner = Scanner(config, logger)
        results = scanner.run()  # <- make sure this method prints output

        # Save report after each module
        if config.output_dir:
            reporter = Reporter(config, logger)
            reporter.generate_report(results)
            print(f"\n{Colors.GREEN}[+] Scan completed! Results saved to: {config.output_dir}{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}[+] Scan completed!{Colors.RESET}")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Scan interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.RESET}")
        if config.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
# This is the main entry point for the TresPax tool.
