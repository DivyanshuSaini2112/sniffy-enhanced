# 🔍 Sniffy Enhanced

**Comprehensive Reconnaissance and Enumeration Platform**

**Created by:** Divyanshu Saini

---

## 🎯 What is Sniffy Enhanced?

Sniffy Enhanced is a powerful, all-in-one reconnaissance platform that transforms the complex world of security scanning into a single, elegant command. Think of it as the **LinPEAS for external reconnaissance** - simple to use, yet incredibly comprehensive.

\`\`\`bash
# Traditional approach (multiple tools, manual correlation)
nmap -sS target.com
gobuster dir -u http://target.com
nikto -h target.com
# ... hours of manual work

# Sniffy Enhanced approach (one command, professional report)
sniffy -t target.com
# ✨ Done! Professional HTML report generated automatically
\`\`\`

## ✨ Key Features

| 🔍 **Network Discovery** | 🌐 **Web Scanning** | 🛡️ **Security Assessment** |
|--------------------------|---------------------|---------------------------|
| • Host & Port Discovery  | • Directory Enumeration | • Vulnerability Detection |
| • Service Fingerprinting | • Technology Stack ID  | • Risk Scoring |
| • OS Detection          | • Sensitive File Discovery | • Professional Reports |

### 🎭 **Stealth Mode**
Advanced evasion techniques including randomized timing, decoy IPs, and packet fragmentation.

### 📊 **Professional Reporting**
Beautiful HTML reports with executive summaries, technical details, and actionable recommendations.

### ⚡ **Performance Optimized**
Multi-threaded scanning with intelligent rate limiting and timeout management.

## 🚀 Quick Start

### One-Line Installation
\`\`\`bash
curl -fsSL https://raw.githubusercontent.com/divyanshu-saini/sniffy-enhanced/main/install.sh | sudo bash
\`\`\`

### First Scan
\`\`\`bash
# Scan a target
sniffy -t example.com

# Stealth scan
sniffy -t target.com --stealth

# Get help
sniffy --help
\`\`\`

## 📦 Installation

### 🔧 System Requirements

- **Operating System**: Ubuntu 18.04+ / Debian 10+ / Kali Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: 2GB free space
- **Network**: Internet connection for tool downloads

### 🎯 Installation Methods

#### Method 1: Automated (Recommended)

\`\`\`bash
# Download and run installation script
wget https://raw.githubusercontent.com/divyanshu-saini/sniffy-enhanced/main/install.sh
chmod +x install.sh
sudo ./install.sh
\`\`\`

#### Method 2: Manual Setup

\`\`\`bash
# Step 1: Clone the repository
git clone https://github.com/divyanshu-saini/sniffy-enhanced.git
cd sniffy-enhanced

# Step 2: Install system packages
sudo apt install -y nmap gobuster python3 python3-pip curl wget dnsutils whois \
nikto dirb smbclient enum4linux hydra netcat-openbsd sqlmap whatweb dnsrecon \
masscan git jq parallel xmlstarlet html2text golang-go build-essential

# Step 3: Install Python dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Step 4: Install Go-based tools
export GOPATH="/opt/go"
export PATH="$PATH:/usr/local/go/bin:$GOPATH/bin"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install -v github.com/ffuf/ffuf@latest

# Step 5: Setup directories and permissions
sudo mkdir -p /opt/sniffy
sudo cp -r src/* /opt/sniffy/
sudo cp -r config /opt/sniffy/
sudo cp -r wordlists /opt/sniffy/
sudo cp -r templates /opt/sniffy/
sudo chmod +x /opt/sniffy/sniffy.py
sudo ln -sf /opt/sniffy/sniffy.py /usr/local/bin/sniffy
\`\`\`

### ✅ Verify Installation

\`\`\`bash
# Check if sniffy command is available
sniffy --version

# Test basic functionality
sniffy --help

# Run a quick test scan
sniffy -t 127.0.0.1
\`\`\`

## 🎮 Usage

### Basic Syntax

\`\`\`bash
sniffy -t <target> [options]
\`\`\`

### Command Line Options

#### Required Arguments
- `-t, --target <target>` - Target IP address, domain name, or CIDR range

#### Optional Arguments
- `-o, --output <file>` - Output file for results (default: auto-generated)
- `-s, --scope <file>` - File containing multiple targets (one per line)
- `--stealth` - Enable stealth mode (slower but harder to detect)
- `--deep` - Enable deep scanning (comprehensive but slower)
- `--rate-limit <rate>` - Rate limit in packets per second (default: 1000)
- `--timeout <seconds>` - Scan timeout in seconds (default: 3600)
- `--config <file>` - Custom configuration file path
- `--debug` - Enable debug logging for troubleshooting
- `--version` - Show version information
- `-h, --help` - Display help message

#### Scan Modes
- `--quick` - Quick scan (top 100 ports)
- `--standard` - Standard scan (top 1000 ports) [default]
- `--comprehensive` - Full scan (all 65535 ports)
- `--web-only` - Web application scan only
- `--network-only` - Network infrastructure scan only

### Target Formats

\`\`\`bash
# Single IP address
sniffy -t 192.168.1.100

# Domain name
sniffy -t example.com

# CIDR network range
sniffy -t 192.168.1.0/24

# Multiple targets from file
echo -e "192.168.1.1\nexample.com\n10.0.0.1" > targets.txt
sniffy --scope targets.txt
\`\`\`

### Basic Examples

\`\`\`bash
# Standard scan of a single target
sniffy -t 192.168.1.1

# Stealth scan with custom output file
sniffy -t example.com --stealth -o stealth_scan.html

# Deep comprehensive scan
sniffy -t target.com --deep --comprehensive -o detailed_report.html

# Quick scan of network range
sniffy -t 192.168.1.0/24 --quick

# Web application only scan
sniffy -t webapp.example.com --web-only

# Scan with custom rate limiting
sniffy -t target.com --rate-limit 500 --timeout 1800
\`\`\`

### Advanced Examples

\`\`\`bash
# Maximum stealth scan for bug bounty
sniffy -t target.com --stealth --rate-limit 50 --timeout 7200

# Comprehensive enterprise network scan
sniffy --scope company_assets.txt --comprehensive --deep

# Custom configuration scan
sniffy -t target.com --config /path/to/custom.json

# Debug mode for troubleshooting
sniffy -t target.com --debug
\`\`\`

## ⚙️ Configuration

### 📁 Configuration Files

Configuration files are stored in `/opt/sniffy/config/`:

- `default.json` - Default configuration settings
- `stealth.json` - Stealth mode configuration
- `aggressive.json` - Aggressive scanning configuration

### 🎛️ Custom Configuration

\`\`\`bash
# Copy default configuration
sudo cp /opt/sniffy/config/default.json /opt/sniffy/config/my_config.json

# Edit configuration
sudo nano /opt/sniffy/config/my_config.json

# Use custom configuration
sniffy -t target.com --config /opt/sniffy/config/my_config.json
\`\`\`

### Configuration Options

Key configuration sections:

- **scanning**: Port ranges, timeouts, thread limits
- **stealth**: Delay ranges, decoy options, randomization
- **wordlists**: Paths to directory and file wordlists
- **output**: Report format and template options
- **modules**: Enable/disable specific scanning modules

## 📊 Sample Output

### Terminal Output
\`\`\`
🔍 Sniffy Enhanced v2.0 - Starting Scan
========================================
[INFO] Target: example.com (93.184.216.34)
[INFO] Scan Mode: Standard

[SUCCESS] Network Discovery Complete - 1 host found
[SUCCESS] Port Scan Complete - 3 open ports
[SUCCESS] Service Enumeration Complete
[SUCCESS] Web Scan Complete - 12 directories found
[WARNING] Vulnerability Assessment - 2 issues found

📊 Scan Summary:
================
Duration: 2m 34s
Open Ports: 3 (22, 80, 443)
Vulnerabilities: 2 Medium Risk
Report: sniffy_example.com_20241204.html
\`\`\`

### HTML Report Features
- 📊 **Executive Dashboard** with risk metrics
- 🔌 **Network Services** table with versions
- 🌐 **Web Technologies** detected
- 🚨 **Vulnerability Findings** with recommendations
- 🎯 **Action Items** prioritized by risk

## 🏗️ Project Architecture

\`\`\`
sniffy-enhanced/
├── 🐍 src/core/           # Core scanning engines
├── ⚙️ config/             # Configuration files  
├── 📝 wordlists/          # Scanning dictionaries
├── 🎨 templates/          # Report templates
├── 🧪 tests/              # Unit tests
├── 🚀 sniffy.py           # Main entry point
└── 📋 install.sh          # Installation script
\`\`\`

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 🚫 Permission denied | Run with `sudo` |
| 🐍 Python errors | Update: `pip3 install --upgrade pip` |
| 🔍 Nmap not found | Install: `sudo apt install nmap` |
| 🐌 Slow scanning | Use: `--quick` or increase `--rate-limit` |
| 🚨 Getting blocked | Enable: `--stealth` mode |

### Debug Mode

\`\`\`bash
sniffy -t target.com --debug  # Detailed troubleshooting output
\`\`\`

## ⚖️ Legal & Ethics

### ✅ **Authorized Use**
- 🏠 Your own systems and networks
- 📋 Authorized penetration testing
- 🎯 Bug bounty programs (within scope)
- 🎓 Educational environments

### ❌ **Prohibited Use**
- 🚫 Unauthorized system scanning
- ⚔️ Malicious activities
- 📜 Violating terms of service
- 🏴‍☠️ Any illegal activities

> ⚠️ **Important**: Always obtain proper authorization before scanning any systems you don't own.

## 🤝 Contributing

We welcome contributions! Here's how:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. ✨ Make your improvements
4. 🧪 Add tests if needed
5. 📤 Submit a pull request

## 📄 License

MIT License - Feel free to use, modify, and distribute.

## Disclaimer

The author and contributors are not responsible for any misuse of this tool. Users are solely responsible for ensuring their use complies with all applicable laws and regulations.

<div align="center">

**🎉 Happy Scanning!**

*Made with ❤️ by Divyanshu Saini*

**Disclaimer**: This tool is for authorized security testing only. Users are responsible for compliance with all applicable laws.

</div>
