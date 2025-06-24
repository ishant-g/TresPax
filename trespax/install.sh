#!/bin/bash

# TresPax Installation Script (APT-based)
# Author: IXEDGE FORGE

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${RED}"
echo "🔥============================================================🔥"
echo -e "${RED}           IXEDGE FORGE PRESENTS${NC}"
echo -e "${CYAN}"
echo " _____                ____             "
echo "|_   _|_ __ ___  ___ |  _ \ __ ___  __ "
echo "  | || '__/ _ \/ __|| |_) / _\` \ \/ / "
echo "  | || | |  __/\__ \|  __/ (_| |>  <  "
echo "  |_||_|  \___||___/|_|   \__,_/_/\_\ "
echo ""
echo -e "${YELLOW}    🛠️  The One-Tool Recon & Enumeration Framework${NC}"
echo -e "${GREEN}                    Installation Script${NC}"
echo -e "${RED}============================================================${NC}"
echo ""

# Check if running as root (we now allow because apt requires sudo)
if [[ $EUID -ne 0 ]]; then
   echo -e "${YELLOW}[!] Please run this script with sudo (e.g., sudo ./install.sh)${NC}"
   exit 1
fi

# Update APT
echo -e "${CYAN}[*] Updating package list...${NC}"
apt update -y

# Install Python 3 if missing
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 is not installed. Installing...${NC}"
    apt install -y python3
fi

# Install required python packages via APT
echo -e "${CYAN}[*] Installing Python dependencies via apt...${NC}"

apt install -y python3-colorama \
    python3-termcolor \
    python3-pyfiglet \
    python3-requests \
    python3-dnspython \
    python3-whois \
    python3-socks \
    python3-nmap \
    python3-bs4 \
    python3-lxml \
    python3-geoip2 \
    python3-argparse-addons \
    python3-argparse-manpage \
    python3-dateutil \
    python3-tqdm \
    python3-tabulate \
    python3-validators \
    python3-psutil \
    python3-urllib3

# Create directories
echo -e "${CYAN}[*] Creating project directories...${NC}"
mkdir -p ~/trespax/reports
mkdir -p ~/trespax/wordlists

# Copy default wordlists if needed
if [ ! -f "/usr/share/wordlists/rockyou.txt" ] && [ ! -f "~/trespax/wordlists/passwords.txt" ]; then
    echo -e "${YELLOW}[!] System wordlists not found. Copying built-in wordlists...${NC}"
    cp -r wordlists/* ~/trespax/wordlists/ 2>/dev/null || true
fi

# Link main.py as global command: trespax
echo -e "${CYAN}[*] Linking tool to /usr/local/bin...${NC}"

INSTALL_PATH="/usr/local/bin/trespax"

cat <<EOF > $INSTALL_PATH
#!/bin/bash
python3 $(realpath main.py) "\$@"
EOF

chmod +x $INSTALL_PATH

# Confirm installation
echo -e "${CYAN}[*] Testing installation...${NC}"

if command -v trespax &> /dev/null; then
    echo -e "${GREEN}[+] TresPax installed successfully! You can now run it using:${NC}"
    echo -e "${YELLOW}    trespax -t example.com${NC}"
else
    echo -e "${RED}[!] Installation completed, but trespax command not found in PATH.${NC}"
    echo -e "${YELLOW}    Try running directly: ${CYAN}/usr/local/bin/trespax${NC}"
fi

# Final info
echo ""
echo -e "${GREEN}🔥 Installation completed! 🔥${NC}"
echo ""
echo -e "${CYAN}Usage examples:${NC}"
echo -e "${YELLOW}  trespax -t example.com${NC}"
echo -e "${YELLOW}  trespax -t example.com --tor${NC}"
echo -e "${YELLOW}  trespax -t example.com -v${NC}"
echo -e "${YELLOW}  trespax --help${NC}"
echo ""
echo -e "${BLUE}Happy hacking! 🛠️${NC}"
echo -e "${BLUE}- IXEDGE FORGE${NC}"
