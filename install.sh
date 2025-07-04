#!/bin/bash
# Sniffy Enhanced - Installation Script
# Version: 2.0

set -euo pipefail

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

readonly INSTALL_DIR="/opt/sniffy"
readonly BIN_DIR="/usr/local/bin"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        log_error "Installation requires root privileges"
        exit 1
    fi
}

install_system_packages() {
    log_info "Installing system packages..."
    
    # Update package lists
    apt-get update -qq
    
    # Install required packages
    local packages=(
        "nmap" "gobuster" "python3" "python3-pip" "curl" "wget" "dnsutils" "whois"
        "nikto" "dirb" "smbclient" "enum4linux" "hydra" "netcat-openbsd" "sqlmap"
        "whatweb" "dnsrecon" "masscan" "git" "jq" "parallel" "xmlstarlet" "html2text"
        "golang-go" "build-essential"
    )
    
    for package in "${packages[@]}"; do
        if ! dpkg -l | grep -q "^ii.*$package"; then
            log_info "Installing $package..."
            apt-get install -y "$package" >/dev/null 2>&1 || log_warning "Failed to install $package"
        fi
    done
}

install_go_tools() {
    log_info "Installing Go-based tools..."
    
    # Set Go environment
    export GOPATH="/opt/go"
    export PATH="$PATH:/usr/local/go/bin:$GOPATH/bin"
    
    # Install tools
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
    go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
    go install -v github.com/ffuf/ffuf@latest
    go install -v github.com/epi052/feroxbuster@latest
    
    # Copy to system path
    cp "$GOPATH/bin"/* "$BIN_DIR/" 2>/dev/null || true
}

install_python_packages() {
    log_info "Installing Python packages..."
    
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
}

setup_directories() {
    log_info "Setting up directory structure..."
    
    # Create main directories
    mkdir -p "$INSTALL_DIR"/{core,modules,wordlists,exploits,reports,config}
    mkdir -p "$INSTALL_DIR/modules"/{network,web,services,privesc,lateral}
    mkdir -p "$INSTALL_DIR/wordlists"/{directories,files,usernames,passwords,subdomains}
    mkdir -p "$INSTALL_DIR/exploits"/{public,custom}
    mkdir -p "$INSTALL_DIR/reports"/{templates,output}
    
    # Copy files
    cp -r src/* "$INSTALL_DIR/"
    cp -r wordlists/* "$INSTALL_DIR/wordlists/"
    cp -r templates/* "$INSTALL_DIR/reports/templates/"
    cp config/* "$INSTALL_DIR/config/"
    
    # Set permissions
    chown -R root:root "$INSTALL_DIR"
    chmod -R 755 "$INSTALL_DIR"
    chmod +x "$INSTALL_DIR/core"/*.py
    chmod +x "$INSTALL_DIR/sniffy.py"
    
    # Create symlink
    ln -sf "$INSTALL_DIR/sniffy.py" "$BIN_DIR/sniffy"
}

main() {
    echo "🔍 Sniffy Enhanced - Installation Script"
    echo "========================================"
    
    check_root
    install_system_packages
    install_go_tools
    install_python_packages
    setup_directories
    
    log_success "Installation completed successfully!"
    log_info "Run 'sniffy --help' to get started"
}

main "$@"
