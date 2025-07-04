"""
Service-specific enumeration module
"""

import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor

class ServiceScanner:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def enumerate_services(self, target, open_ports):
        """Enumerate services on open ports"""
        results = {
            'target': target,
            'services': []
        }
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for port_info in open_ports:
                port = port_info.get('port')
                service = port_info.get('service', '')
                
                future = executor.submit(self._enumerate_service, target, port, service)
                futures.append(future)
            
            for future in futures:
                service_result = future.result()
                if service_result:
                    results['services'].append(service_result)
        
        return results
    
    def _enumerate_service(self, target, port, service):
        """Enumerate specific service"""
        self.logger.debug(f"Enumerating {service} on {target}:{port}")
        
        service_info = {
            'port': port,
            'service': service,
            'banner': '',
            'details': {}
        }
        
        # Get banner
        banner = self._get_banner(target, port)
        if banner:
            service_info['banner'] = banner
        
        # Service-specific enumeration
        if service.lower() in ['http', 'https']:
            service_info['details'] = self._enumerate_http(target, port)
        elif service.lower() == 'ftp':
            service_info['details'] = self._enumerate_ftp(target, port)
        elif service.lower() == 'ssh':
            service_info['details'] = self._enumerate_ssh(target, port)
        elif service.lower() in ['smb', 'microsoft-ds']:
            service_info['details'] = self._enumerate_smb(target, port)
        
        return service_info
    
    def _get_banner(self, host, port, timeout=3):
        """Get service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return banner
        except:
            return ""
    
    def _enumerate_http(self, target, port):
        """Enumerate HTTP service"""
        details = {}
        try:
            import requests
            url = f"http://{target}:{port}" if port != 443 else f"https://{target}:{port}"
            response = requests.get(url, timeout=10)
            
            details['status_code'] = response.status_code
            details['server'] = response.headers.get('Server', '')
            details['powered_by'] = response.headers.get('X-Powered-By', '')
            details['content_length'] = len(response.content)
            
        except Exception as e:
            details['error'] = str(e)
        
        return details
    
    def _enumerate_ftp(self, target, port):
        """Enumerate FTP service"""
        details = {}
        try:
            # Try anonymous login
            import ftplib
            ftp = ftplib.FTP()
            ftp.connect(target, port, timeout=10)
            ftp.login('anonymous', 'anonymous@example.com')
            details['anonymous_login'] = True
            details['welcome_message'] = ftp.getwelcome()
            ftp.quit()
        except:
            details['anonymous_login'] = False
        
        return details
    
    def _enumerate_ssh(self, target, port):
        """Enumerate SSH service"""
        details = {}
        try:
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Get SSH version
            transport = paramiko.Transport((target, port))
            transport.start_client()
            details['version'] = transport.remote_version
            transport.close()
            
        except Exception as e:
            details['error'] = str(e)
        
        return details
    
    def _enumerate_smb(self, target, port):
        """Enumerate SMB service"""
        details = {}
        try:
            # Use smbclient to enumerate shares
            result = subprocess.run(
                ['smbclient', '-L', target, '-N'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                details['shares'] = result.stdout
            else:
                details['error'] = result.stderr
                
        except Exception as e:
            details['error'] = str(e)
        
        return details
