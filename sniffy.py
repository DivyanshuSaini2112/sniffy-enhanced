#!/usr/bin/env python3
"""
Sniffy Enhanced - Comprehensive Reconnaissance and Enumeration Platform
Version: 2.0
Author: Security Research Team
License: MIT
"""

import argparse
import sys
import os
import json
import time
from pathlib import Path

# Add src directory to path (absolute)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from core.scanner import SniffyScanner
from core.config import Config
from core.logger import Logger
from core.utils import validate_target, setup_temp_directory
from core.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description='Sniffy Enhanced - Comprehensive Reconnaissance Platform v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sniffy -t 192.168.1.1
  sniffy -t example.com --stealth -o results.json
  sniffy -t 10.0.0.0/24 --deep --rate-limit 500
  sniffy --scope targets.txt --stealth

For more information, visit: https://github.com/yourusername/sniffy-enhanced
        """
    )
    
    # Required arguments
    parser.add_argument('-t', '--target', help='Target IP, domain, or CIDR range')
    
    # Optional arguments
    parser.add_argument('-o', '--output', help='Output file for results')
    parser.add_argument('-s', '--scope', help='Scope file with multiple targets')
    parser.add_argument('--stealth', action='store_true', help='Enable stealth mode')
    parser.add_argument('--deep', action='store_true', help='Enable deep scanning')
    parser.add_argument('--rate-limit', type=int, default=1000, help='Rate limit in packets/second')
    parser.add_argument('--timeout', type=int, default=3600, help='Scan timeout in seconds')
    parser.add_argument('--config', help='Custom configuration file')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--version', action='version', version='Sniffy Enhanced v2.0')
    
    args = parser.parse_args()
    
    # Validate input
    if not args.target and not args.scope:
        parser.error("Target or scope file required")
    
    if args.target and not validate_target(args.target):
        parser.error(f"Invalid target format: {args.target}")
    
    # Initialize components
    config = Config(args.config)
    logger = Logger(debug=args.debug)
    
    # Setup temporary directory
    temp_dir = setup_temp_directory()
    
    try:
        # Initialize scanner
        scanner = SniffyScanner(
            config=config,
            logger=logger,
            stealth=args.stealth,
            deep_scan=args.deep,
            rate_limit=args.rate_limit,
            timeout=args.timeout
        )
        
        # Run scan
        if args.target:
            results = scanner.scan_target(args.target)
        else:
            results = scanner.scan_scope_file(args.scope)
        
        # Generate report
        report_generator = ReportGenerator(logger)
        report_file = report_generator.generate_report(
            results, 
            args.output or f"sniffy_report_{int(time.time())}.html"
        )
        
        logger.success(f"Scan completed. Report saved to: {report_file}")
        
    except KeyboardInterrupt:
        logger.warning("Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Scan failed: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup
        if not args.debug:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
