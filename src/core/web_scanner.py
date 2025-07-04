"""
Web application scanner and enumerator
"""

import requests
import random
import time
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

class WebScanner:
    def __init__(self, config, logger, stealth=False):
        self.config = config
        self.logger = logger
        self.stealth = stealth
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Setup requests session with appropriate headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents) if self.stealth else user_agents[0],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        # Set timeout
        self.session.timeout = 10
    
    def scan(self, target, ports):
        """Scan web applications on specified ports"""
        results = {
            'target': target,
            'web_services': [],
            'directories': [],
            'technologies': {},
            'vulnerabilities': []
        }
        
        # Build URLs for each port
        urls = []
        for port in ports:
            if port == 443 or port == 8443:
                urls.append(f"https://{target}:{port}")
            else:
                urls.append(f"http://{target}:{port}")
        
        # Scan each URL
        for url in urls:
            self.logger.info(f"Scanning web application: {url}")
            
            # Basic web service info
            service_info = self._get_service_info(url)
            if service_info:
                results['web_services'].append(service_info)
                
                # Technology detection
                tech_info = self._detect_technologies(url)
                results['technologies'][url] = tech_info
                
                # Directory enumeration
                directories = self._enumerate_directories(url)
                results['directories'].extend(directories)
                
                # Basic vulnerability checks
                vulns = self._check_basic_vulnerabilities(url)
                results['vulnerabilities'].extend(vulns)
        
        return results
    
    def _get_service_info(self, url):
        """Get basic information about web service"""
        try:
            response = self.session.get(url, allow_redirects=True)
            
            return {
                'url': url,
                'status_code': response.status_code,
                'server': response.headers.get('Server', ''),
                'content_length': len(response.content),
                'title': self._extract_title(response.text),
                'headers': dict(response.headers)
            }
            
        except Exception as e:
            self.logger.debug(f"Failed to get service info for {url}: {str(e)}")
            return None
    
    def _detect_technologies(self, url):
        """Detect web technologies"""
        technologies = {
            'server': '',
            'frameworks': [],
            'cms': [],
            'javascript': [],
            'css': []
        }
        
        try:
            response = self.session.get(url)
            content = response.text.lower()
            headers = response.headers
            
            # Server detection
            technologies['server'] = headers.get('Server', '')
            
            # Framework detection
            if 'django' in content or 'csrftoken' in content:
                technologies['frameworks'].append('Django')
            if 'flask' in content:
                technologies['frameworks'].append('Flask')
            if 'laravel' in content:
                technologies['frameworks'].append('Laravel')
            if 'express' in headers.get('X-Powered-By', '').lower():
                technologies['frameworks'].append('Express.js')
            
            # CMS detection
            if 'wp-content' in content or 'wordpress' in content:
                technologies['cms'].append('WordPress')
            if 'joomla' in content:
                technologies['cms'].append('Joomla')
            if 'drupal' in content:
                technologies['cms'].append('Drupal')
            
            # JavaScript libraries
            if 'jquery' in content:
                technologies['javascript'].append('jQuery')
            if 'angular' in content:
                technologies['javascript'].append('Angular')
            if 'react' in content:
                technologies['javascript'].append('React')
            if 'vue' in content:
                technologies['javascript'].append('Vue.js')
            
        except Exception as e:
            self.logger.debug(f"Technology detection failed for {url}: {str(e)}")
        
        return technologies
    
    def _enumerate_directories(self, url):
        """Enumerate directories using wordlist"""
        directories = []
        wordlist_path = self.config.get_wordlist_path('directories/common.txt')
        
        try:
            with open(wordlist_path, 'r') as f:
                words = [line.strip() for line in f if line.strip()]
            
            # Limit concurrent requests for stealth
            max_workers = 5 if self.stealth else 20
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                
                for word in words[:100]:  # Limit for demo
                    test_url = urljoin(url, word)
                    future = executor.submit(self._check_directory, test_url)
                    futures.append(future)
                    
                    if self.stealth:
                        time.sleep(random.uniform(0.1, 0.5))
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        directories.append(result)
        
        except Exception as e:
            self.logger.error(f"Directory enumeration failed: {str(e)}")
        
        return directories
    
    def _check_directory(self, url):
        """Check if directory exists"""
        try:
            response = self.session.get(url, allow_redirects=False)
            if response.status_code in [200, 301, 302, 401, 403]:
                return {
                    'url': url,
                    'status_code': response.status_code,
                    'content_length': len(response.content)
                }
        except:
            pass
        return None
    
    def _check_basic_vulnerabilities(self, url):
        """Check for basic web vulnerabilities"""
        vulnerabilities = []
        
        # Check for common files
        common_files = [
            '.env', 'web.config', '.htaccess', 'robots.txt',
            'sitemap.xml', 'crossdomain.xml', 'phpinfo.php'
        ]
        
        for file in common_files:
            try:
                test_url = urljoin(url, file)
                response = self.session.get(test_url)
                
                if response.status_code == 200:
                    vulnerabilities.append({
                        'type': 'Information Disclosure',
                        'url': test_url,
                        'description': f'Sensitive file exposed: {file}',
                        'severity': 'Medium'
                    })
            except:
                continue
        
        return vulnerabilities
    
    def _extract_title(self, html):
        """Extract title from HTML"""
        import re
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else ''
