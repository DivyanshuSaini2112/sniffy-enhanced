"""
Configuration management for Sniffy Enhanced
"""

import json
import os
from pathlib import Path

class Config:
    def __init__(self, config_file=None):
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_file = config_file or self.base_dir / 'config' / 'default.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return self._get_default_config()
    
    def _get_default_config(self):
        """Get default configuration"""
        return {
            "scanning": {
                "default_ports": "1-1000",
                "max_threads": 50,
                "timeout": 10,
                "rate_limit": 1000
            },
            "stealth": {
                "delay_range": [0.1, 0.5],
                "randomize_user_agents": True,
                "use_decoys": True
            },
            "wordlists": {
                "directories": "wordlists/directories/common.txt",
                "files": "wordlists/files/sensitive.txt",
                "subdomains": "wordlists/subdomains/common.txt"
            },
            "output": {
                "format": "html",
                "include_raw": True,
                "compress": False
            }
        }
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_wordlist_path(self, wordlist_name):
        """Get full path to wordlist file"""
        return self.base_dir / 'wordlists' / wordlist_name
