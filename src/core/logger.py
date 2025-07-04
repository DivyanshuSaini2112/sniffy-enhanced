"""
Enhanced logging system for Sniffy Enhanced
"""

import logging
import sys
from datetime import datetime

class Logger:
    def __init__(self, debug=False):
        self.debug_mode = debug
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging configuration"""
        # Colors for console output
        self.colors = {
            'RED': '\033[0;31m',
            'GREEN': '\033[0;32m',
            'YELLOW': '\033[1;33m',
            'BLUE': '\033[0;34m',
            'PURPLE': '\033[0;35m',
            'CYAN': '\033[0;36m',
            'WHITE': '\033[1;37m',
            'NC': '\033[0m'  # No Color
        }
        
        # Setup logger
        self.logger = logging.getLogger('sniffy')
        self.logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def _log_with_color(self, level, message, color):
        """Log message with color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colored_message = f"{color}[{level}]{self.colors['NC']} {message}"
        print(colored_message)
    
    def info(self, message):
        """Log info message"""
        self._log_with_color("INFO", message, self.colors['BLUE'])
    
    def success(self, message):
        """Log success message"""
        self._log_with_color("SUCCESS", message, self.colors['GREEN'])
    
    def warning(self, message):
        """Log warning message"""
        self._log_with_color("WARNING", message, self.colors['YELLOW'])
    
    def error(self, message):
        """Log error message"""
        self._log_with_color("ERROR", message, self.colors['RED'])
    
    def debug(self, message):
        """Log debug message"""
        if self.debug_mode:
            self._log_with_color("DEBUG", message, self.colors['PURPLE'])
    
    def critical(self, message):
        """Log critical message"""
        self._log_with_color("CRITICAL", message, self.colors['RED'])
