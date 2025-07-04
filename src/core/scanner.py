"""
Main scanner class that orchestrates all scanning modules
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from .network_scanner import NetworkScanner
from .web_scanner import WebScanner
from .service_scanner import ServiceScanner
from .vulnerability_scanner import VulnerabilityScanner

class SniffyScanner:
    def __init__(self, config, logger, stealth=False, deep_scan=False, rate_limit=1000, timeout=3600):
        self.config = config
        self.logger = logger
        self.stealth = stealth
        self.deep_scan = deep_scan
        self.rate_limit = rate_limit
        self.timeout = timeout
        
        # Initialize scanners
        self.network_scanner = NetworkScanner(config, logger, stealth, rate_limit)
        self.web_scanner = WebScanner(config, logger, stealth)
        self.service_scanner = ServiceScanner(config, logger)
        self.vuln_scanner = VulnerabilityScanner(config, logger)
        
        self.results = {}
        self.scan_start_time = None
    
    def scan_target(self, target):
        """Scan a single target"""
        self.logger.info(f"Starting comprehensive scan of target: {target}")
        self.scan_start_time = time.time()
        
        try:
            # Phase 1: Network Discovery
            self.logger.info("Phase 1: Network Discovery")
            network_results = self.network_scanner.scan(target)
            self.results['network'] = network_results
            
            # Phase 2: Service Enumeration
            self.logger.info("Phase 2: Service Enumeration")
            if network_results.get('open_ports'):
                service_results = self.service_scanner.enumerate_services(
                    target, network_results['open_ports']
                )
                self.results['services'] = service_results
            
            # Phase 3: Web Application Scanning
            web_ports = self._get_web_ports(network_results.get('open_ports', []))
            if web_ports:
                self.logger.info("Phase 3: Web Application Scanning")
                web_results = self.web_scanner.scan(target, web_ports)
                self.results['web'] = web_results
            
            # Phase 4: Vulnerability Assessment
            self.logger.info("Phase 4: Vulnerability Assessment")
            vuln_results = self.vuln_scanner.scan(target, self.results)
            self.results['vulnerabilities'] = vuln_results
            
            # Calculate scan duration
            scan_duration = time.time() - self.scan_start_time
            self.results['scan_info'] = {
                'target': target,
                'duration': scan_duration,
                'timestamp': time.time(),
                'stealth_mode': self.stealth,
                'deep_scan': self.deep_scan
            }
            
            return self.results
            
        except Exception as e:
            self.logger.error(f"Scan failed: {str(e)}")
            raise
    
    def scan_scope_file(self, scope_file):
        """Scan multiple targets from scope file"""
        targets = self._load_scope_file(scope_file)
        results = {}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_target = {
                executor.submit(self.scan_target, target): target 
                for target in targets
            }
            
            for future in as_completed(future_to_target):
                target = future_to_target[future]
                try:
                    results[target] = future.result()
                except Exception as e:
                    self.logger.error(f"Failed to scan {target}: {str(e)}")
                    results[target] = {'error': str(e)}
        
        return results
    
    def _get_web_ports(self, open_ports):
        """Extract web-related ports"""
        web_ports = []
        common_web_ports = [80, 443, 8080, 8443, 8000, 8888, 3000, 5000]
        
        for port_info in open_ports:
            port = port_info.get('port', 0)
            if port in common_web_ports:
                web_ports.append(port)
        
        return web_ports
    
    def _load_scope_file(self, scope_file):
        """Load targets from scope file"""
        targets = []
        try:
            with open(scope_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        targets.append(line)
        except Exception as e:
            self.logger.error(f"Failed to load scope file: {str(e)}")
            raise
        
        return targets
