"""
Report generation module for multiple output formats
"""

import json
import time
from datetime import datetime
from pathlib import Path
from jinja2 import Template

class ReportGenerator:
    def __init__(self, logger):
        self.logger = logger
        self.base_dir = Path(__file__).parent.parent.parent
        self.templates_dir = self.base_dir / 'templates'
    
    def generate_report(self, scan_results, output_file):
        """Generate report in specified format"""
        self.logger.info(f"Generating report: {output_file}")
        
        # Determine format from file extension
        if output_file.endswith('.json'):
            return self._generate_json_report(scan_results, output_file)
        elif output_file.endswith('.html'):
            return self._generate_html_report(scan_results, output_file)
        else:
            # Default to HTML
            return self._generate_html_report(scan_results, output_file + '.html')
    
    def _generate_html_report(self, scan_results, output_file):
        """Generate HTML report"""
        try:
            # Load template
            template_path = self.templates_dir / 'report.html'
            with open(template_path, 'r') as f:
                template_content = f.read()
            
            template = Template(template_content)
            
            # Prepare template variables
            template_vars = self._prepare_template_vars(scan_results)
            
            # Render template
            html_content = template.render(**template_vars)
            
            # Write to file
            with open(output_file, 'w') as f:
                f.write(html_content)
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {str(e)}")
            raise
    
    def _generate_json_report(self, scan_results, output_file):
        """Generate JSON report"""
        try:
            # Add metadata
            report_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'generator': 'Sniffy Enhanced v2.0',
                    'format_version': '1.0'
                },
                'scan_results': scan_results
            }
            
            # Write to file
            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {str(e)}")
            raise
    
    def _prepare_template_vars(self, scan_results):
        """Prepare variables for template rendering"""
        # Extract scan info
        scan_info = scan_results.get('scan_info', {})
        target = scan_info.get('target', 'Unknown')
        duration = scan_info.get('duration', 0)
        
        # Extract network results
        network_results = scan_results.get('network', {})
        open_ports = network_results.get('open_ports', [])
        os_detection = network_results.get('os_detection', [])
        
        # Extract web results
        web_results = scan_results.get('web', {})
        web_services = web_results.get('web_services', [])
        directories = web_results.get('directories', [])
        technologies = web_results.get('technologies', {})
        
        # Extract vulnerability results
        vuln_results = scan_results.get('vulnerabilities', {})
        vulnerabilities = vuln_results.get('vulnerabilities', [])
        risk_score = vuln_results.get('risk_score', 0)
        recommendations = vuln_results.get('recommendations', [])
        
        # Calculate summary statistics
        open_ports_count = len(open_ports)
        services_count = len(scan_results.get('services', {}).get('services', []))
        vulnerabilities_count = len(vulnerabilities)
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = 'Critical'
        elif risk_score >= 50:
            risk_level = 'High'
        elif risk_score >= 30:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        # Format duration
        duration_str = self._format_duration(duration)
        
        # Generate network services table
        network_services_table = self._generate_network_services_table(open_ports)
        
        # Generate web directories list
        web_directories = self._generate_web_directories_list(directories)
        
        # Generate technologies list
        technologies_list = self._generate_technologies_list(technologies)
        
        # Generate vulnerabilities section
        vulnerabilities_section = self._generate_vulnerabilities_section(vulnerabilities)
        
        # Generate recommendations list
        recommendations_list = self._generate_recommendations_list(recommendations)
        
        return {
            'target': target,
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'duration': duration_str,
            'open_ports_count': open_ports_count,
            'services_count': services_count,
            'vulnerabilities_count': vulnerabilities_count,
            'risk_level': risk_level,
            'resolved_ip': self._resolve_ip(target),
            'os_detection': self._format_os_detection(os_detection),
            'hostname': target,
            'network_services_table': network_services_table,
            'web_directories': web_directories,
            'technologies': technologies_list,
            'vulnerabilities_section': vulnerabilities_section,
            'recommendations': recommendations_list
        }
    
    def _format_duration(self, seconds):
        """Format duration in human readable format"""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
    
    def _resolve_ip(self, target):
        """Resolve target to IP address"""
        import socket
        try:
            return socket.gethostbyname(target)
        except:
            return target
    
    def _format_os_detection(self, os_detection):
        """Format OS detection results"""
        if not os_detection:
            return "Unknown"
        
        if isinstance(os_detection, list) and os_detection:
            first_result = os_detection[0]
            if isinstance(first_result, dict):
                return first_result.get('os_info', {}).get('name', 'Unknown')
        
        return str(os_detection)
    
    def _generate_network_services_table(self, open_ports):
        """Generate HTML table for network services"""
        if not open_ports:
            return "<tr><td colspan='5'>No open ports found</td></tr>"
        
        rows = []
        for port_info in open_ports:
            port = port_info.get('port', 'Unknown')
            protocol = port_info.get('protocol', 'tcp')
            service = port_info.get('service', 'Unknown')
            version = port_info.get('version', '')
            state = port_info.get('state', 'open')
            
            rows.append(f"""
                <tr>
                    <td>{port}</td>
                    <td>{protocol}</td>
                    <td>{service}</td>
                    <td>{version}</td>
                    <td>{state}</td>
                </tr>
            """)
        
        return ''.join(rows)
    
    def _generate_web_directories_list(self, directories):
        """Generate HTML list for web directories"""
        if not directories:
            return "<li>No directories discovered</li>"
        
        items = []
        for dir_info in directories:
            url = dir_info.get('url', '')
            status_code = dir_info.get('status_code', 0)
            items.append(f"<li>{url} (Status: {status_code})</li>")
        
        return ''.join(items)
    
    def _generate_technologies_list(self, technologies):
        """Generate HTML list for technologies"""
        if not technologies:
            return "<li>No technologies detected</li>"
        
        items = []
        for url, tech_info in technologies.items():
            if isinstance(tech_info, dict):
                server = tech_info.get('server', '')
                frameworks = tech_info.get('frameworks', [])
                cms = tech_info.get('cms', [])
                
                if server:
                    items.append(f"<li>Server: {server}</li>")
                if frameworks:
                    items.append(f"<li>Frameworks: {', '.join(frameworks)}</li>")
                if cms:
                    items.append(f"<li>CMS: {', '.join(cms)}</li>")
        
        return ''.join(items) if items else "<li>No technologies detected</li>"
    
    def _generate_vulnerabilities_section(self, vulnerabilities):
        """Generate HTML section for vulnerabilities"""
        if not vulnerabilities:
            return "<p>No vulnerabilities detected.</p>"
        
        sections = []
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'Unknown')
            vuln_type = vuln.get('type', 'Unknown')
            description = vuln.get('description', '')
            recommendation = vuln.get('recommendation', '')
            
            severity_class = severity.lower()
            
            sections.append(f"""
                <div class="vulnerability {severity_class}">
                    <h4>[{severity.upper()}] {vuln_type}</h4>
                    <p><strong>Description:</strong> {description}</p>
                    <p><strong>Recommendation:</strong> {recommendation}</p>
                </div>
            """)
        
        return ''.join(sections)
    
    def _generate_recommendations_list(self, recommendations):
        """Generate HTML list for recommendations"""
        if not recommendations:
            return "<li>No specific recommendations</li>"
        
        items = [f"<li>{rec}</li>" for rec in recommendations]
        return ''.join(items)
