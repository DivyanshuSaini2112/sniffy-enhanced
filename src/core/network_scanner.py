"""
Enhanced network scanner with stealth capabilities
"""

import nmap
import random
import ipaddress
from concurrent.futures import ThreadPoolExecutor

class NetworkScanner:
    def __init__(self, config, logger, stealth=False, rate_limit=1000):
        self.config = config
        self.logger = logger
        self.stealth = stealth
        self.rate_limit = rate_limit
        self.nm = nmap.PortScanner()
    
    def scan(self, target):
        """Perform comprehensive network scan"""
        results = {
            'target': target,
            'hosts_discovered': [],
            'open_ports': [],
            'os_detection': [],
            'network_info': {}
        }
        
        try:
            # Host discovery
            hosts = self._discover_hosts(target)
            results['hosts_discovered'] = hosts
            
            # Port scanning
            for host in hosts:
                host_results = self._scan_host_ports(host)
                if host_results['open_ports']:
                    results['open_ports'].extend(host_results['open_ports'])
                
                # OS detection
                os_info = self._detect_os(host)
                if os_info:
                    results['os_detection'].append({
                        'host': host,
                        'os_info': os_info
                    })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Network scan failed: {str(e)}")
            return {'error': str(e)}
    
    def _discover_hosts(self, target):
        """Discover live hosts"""
        self.logger.info(f"Discovering hosts for target: {target}")
        
        try:
            # Ping scan to discover hosts
            scan_args = '-sn -n'
            if self.stealth:
                scan_args += ' -T2 --randomize-hosts'
            else:
                scan_args += ' -T4'
            
            result = self.nm.scan(hosts=target, arguments=scan_args)
            hosts = list(result['scan'].keys())
            
            self.logger.success(f"Discovered {len(hosts)} live hosts")
            return hosts
            
        except Exception as e:
            self.logger.error(f"Host discovery failed: {str(e)}")
            return [target]  # Fallback to original target
    
    def _scan_host_ports(self, host):
        """Scan ports on a specific host"""
        self.logger.info(f"Scanning ports on {host}")
        
        results = {
            'host': host,
            'open_ports': []
        }
        
        try:
            # Build scan arguments
            scan_args = ['-sS', '-n', f'--max-rate {self.rate_limit}']
            
            if self.stealth:
                scan_args.extend(['-T2', '-f', '--data-length 25'])
                # Add decoy scanning
                decoys = self._generate_decoys(host)
                if decoys:
                    scan_args.extend(['-D', decoys])
            else:
                scan_args.append('-T4')
            
            # Port range
            port_range = '1-65535' if self.config.get('deep_scan') else '1-1000'
            
            # Perform scan
            scan_result = self.nm.scan(
                hosts=host,
                ports=port_range,
                arguments=' '.join(scan_args)
            )
            
            # Parse results
            if host in scan_result['scan']:
                host_data = scan_result['scan'][host]
                if 'tcp' in host_data:
                    for port, port_data in host_data['tcp'].items():
                        if port_data['state'] == 'open':
                            results['open_ports'].append({
                                'host': host,
                                'port': port,
                                'protocol': 'tcp',
                                'state': port_data['state'],
                                'service': port_data.get('name', ''),
                                'version': port_data.get('version', ''),
                                'product': port_data.get('product', '')
                            })
            
            self.logger.success(f"Found {len(results['open_ports'])} open ports on {host}")
            return results
            
        except Exception as e:
            self.logger.error(f"Port scan failed for {host}: {str(e)}")
            return results
    
    def _detect_os(self, host):
        """Detect operating system"""
        try:
            result = self.nm.scan(hosts=host, arguments='-O --osscan-guess')
            if host in result['scan'] and 'osmatch' in result['scan'][host]:
                os_matches = result['scan'][host]['osmatch']
                if os_matches:
                    return {
                        'name': os_matches[0]['name'],
                        'accuracy': os_matches[0]['accuracy'],
                        'line': os_matches[0]['line']
                    }
        except Exception as e:
            self.logger.debug(f"OS detection failed for {host}: {str(e)}")
        
        return None
    
    def _generate_decoys(self, target):
        """Generate decoy IP addresses for stealth scanning"""
        try:
            ip = ipaddress.ip_address(target)
            network = ipaddress.ip_network(f"{ip}/24", strict=False)
            decoys = []
            
            for _ in range(3):
                decoy = str(random.choice(list(network.hosts())))
                if decoy != target:
                    decoys.append(decoy)
            
            return ','.join(decoys)
        except:
            return None
