```
🔥========================================================🔥  
             IXEDGE FORGE
  ______               ____            
 /_  __/_______  _____/ __ \____ __  __  
  / / / ___/ _ \/ ___/ /_/ / __ `/ |/_/  
 / / / /  /  __(__  ) ____/ /_/ />  <    
/_/ /_/   \___/____/_/    \__,_/_/|_|    

    🛠  The One-Tool Recon & Enumeration Framework  
                    Version 1.0.0  
🔥========================================================🔥
```


## 📌 What is TresPax?

**TresPax** is a powerful, offline-capable, command-line cybersecurity reconnaissance and enumeration tool designed specifically for **Linux** systems. Whether you're a beginner exploring ethical hacking or a seasoned professional, TresPax offers a sleek CLI experience with TOR support, interactive prompts, real-time outputs, and full module integration — all in one place.

No need to switch tools — from DNS to subdomains to SSL certs, TresPax does it all.

> ⚡ Once installed, simply run the tool using keyword:
-----------
| trespax |
-----------


## ⚙️ Core Features

- 🌍 **Universal Accessibility**  
  - Global command: `trespax` works from any terminal session  
  - Fully offline-compatible  
  - Cross-distro support (Ubuntu, Kali, Parrot OS, etc.)

- 🔐 **TOR Network Integration and User Agent Switcher**  
  - Automatic TOR service check  
  - SOCKS5 proxy configuration  
  - Secure and anonymous scanning
  - Switches user agent for one step further anonymity

- 📊 **Comprehensive Reporting**  
  - Organized output in per-target directories  
  - Multiple formats: `.txt`, `.md`  
  - Module-specific and summary reports


## 🧩 Integrated Tools & Modules

| Module              | Description                    | Features                                                       |
|---------------------|--------------------------------|----------------------------------------------------------------|
| WHOIS Lookup        | Domain registration info       | Registrant, dates, nameservers, contacts                       |
| DNS Enumeration     | Complete DNS record analysis   | A, AAAA, MX, CNAME, TXT, SOA                                   |
| Subdomain Discovery | Discover hidden subdomains     | Wordlist brute force, wildcard resolution                      |
| Port Scanning       | Identify open ports/services   | Common ports, version detection                                |
| Directory Busting   | Hidden file & folder discovery | HTTP paths, status codes, response analysis                    |
| HTTP Header Analysis| Web server tech fingerprinting | HTTP status codes, headers, security headers                   |
| Email & Contact     | Extract emails from web pages  | Regex-based search, privacy warning                            |
| Robots/Sitemap      | Analyze crawler configs        | Detect exclusions, disallowed areas, deep links                |
| SSL/TLS Analyzer    | SSL cert and cipher audit      | Expiry, issuer, subject, cipher strength                       |
| Geolocation Lookup  | IP origin and location details | Country, ISP, city, latitude/longitude                         |
| Banner Grabbing     | Service banner extraction      | Server versions, service strings                               |



## 📦 Installation

To install TresPax, navigate to the internal installation folder:

=========================
| cd trespax/            |
| sudo bash install.sh   |
=========================

After installation, you can run `trespax` from any terminal!

## ✅ System Requirements

- OS: Any modern Linux distro (Debian-based recommended)
- Python: 3.8 or higher

❗ You don’t need to install Python dependencies manually. The `install.sh` script will take care of everything using `apt`.



## 📁 Output Structure

When saving results, TresPax creates a clean and organized directory under `reports/`, such as:


reports/
├── example.com_2025-01-20-14-30/
│   ├── whois.txt              # WHOIS information
│   ├── dns.txt                # DNS records
│   ├── subdomains.txt         # Found subdomains
│   ├── ports.txt              # Open ports
│   ├── directories.txt        # Discovered directories
│   ├── headers.txt            # HTTP headers
│   ├── emails.txt             # Found email addresses
│   ├── ssl.txt                # SSL certificate info
│   ├── geolocation.txt        # IP location data
│   ├── summary.txt            # Text summary
│   ├── summary.md             # Markdown report




## 📚 Wordlist Integration

TresPax automatically detects and uses the best available wordlists:

### System Wordlists (Preferred):
- `/usr/share/wordlists/rockyou.txt`
- `/usr/share/wordlists/dirb/common.txt`
- `/usr/share/wordlists/seclists/`
- `/usr/share/wordlists/dirbuster/`

### Built-in Fallback:
- `wordlists/subdomains.txt`
- `wordlists/directories.txt`

You can also provide your own custom wordlists.

---

## 🔒 Security & Privacy

- **TOR Integration**  
  - Checks if TOR is running  
  - Automatically configures SOCKS5  
  - Routes traffic through TOR for privacy  

- **Ethical Usage Only**  
  TresPax is built for:
  - ✅ Penetration testing (with permission)
  - ✅ Security research
  - ✅ Educational use
  - ✅ Bug bounty programs (authorized targets)

⚠️ Legal Notice: Use TresPax only on systems you own or have explicit written permission to test.
⚠️ Disclaimer: The developers, including IXEDGE FORGE and project contributors, are not responsible for any misuse or unauthorized activity performed with this tool.

---

🚀 Made with dedication by **IXEDGE FORGE**  
📫 Reach out, fork, or contribute via GitHub!