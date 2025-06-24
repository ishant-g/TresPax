#!/usr/bin/env python3

import os
import json
from datetime import datetime
from trespax.utils.colors import Colors


class Reporter:
    """Generate reports from scan results"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def generate_report(self, results):
        """Generate comprehensive report"""
        if not self.config.output_dir:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate individual module reports
        for module_name, result in results.items():
            if result:
                self._save_module_report(module_name, result)
        
        # Generate summary report
        self._generate_summary_report(results, timestamp)
        
        # Generate JSON report
        self._generate_json_report(results, timestamp)
        
        # Generate markdown report
        self._generate_markdown_report(results, timestamp)
    
    def _save_module_report(self, module_name, result):
        """Save individual module report"""
        filename = os.path.join(self.config.output_dir, f"{module_name}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"TresPax {module_name.upper()} Module Report\n")
            f.write(f"{'='*50}\n")
            f.write(f"Target: {self.config.target}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if isinstance(result, dict):
                for key, value in result.items():
                    f.write(f"{key}: {value}\n")
            elif isinstance(result, list):
                for item in result:
                    f.write(f"{item}\n")
            else:
                f.write(f"{result}\n")
    
    def _generate_summary_report(self, results, timestamp):
        """Generate summary text report"""
        filename = os.path.join(self.config.output_dir, "summary.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("TresPax Reconnaissance Report\n")
            f.write("="*50 + "\n")
            f.write(f"Target: {self.config.target}\n")
            f.write(f"Scan Date: {timestamp}\n")
            f.write(f"TOR Used: {'Yes' if self.config.use_tor else 'No'}\n")
            f.write(f"Modules Run: {len([r for r in results.values() if r])}/{len(results)}\n\n")
            
            for module_name, result in results.items():
                f.write(f"{module_name.upper()} Module:\n")
                f.write("-" * 20 + "\n")
                
                if result:
                    if isinstance(result, dict):
                        for key, value in result.items():
                            if isinstance(value, list):
                                f.write(f"{key}: {len(value)} items found\n")
                            else:
                                f.write(f"{key}: {value}\n")
                    elif isinstance(result, list):
                        f.write(f"Results: {len(result)} items found\n")
                    else:
                        f.write(f"Result: {result}\n")
                else:
                    f.write("No results found\n")
                
                f.write("\n")
    
    def _generate_json_report(self, results, timestamp):
        """Generate JSON report"""
        filename = os.path.join(self.config.output_dir, "report.json")
        
        report_data = {
            "target": self.config.target,
            "scan_date": timestamp,
            "tor_used": self.config.use_tor,
            "trespax_version": "1.0.0",
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
    
    def _generate_markdown_report(self, results, timestamp):
        """Generate markdown report"""
        filename = os.path.join(self.config.output_dir, "summary.md")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# TresPax Reconnaissance Report\n\n")
            f.write(f"**Target:** {self.config.target}\n\n")
            f.write(f"**Scan Date:** {timestamp}\n\n")
            f.write(f"**TOR Used:** {'Yes' if self.config.use_tor else 'No'}\n\n")
            f.write(f"**Modules Run:** {len([r for r in results.values() if r])}/{len(results)}\n\n")
            
            f.write("## Results Summary\n\n")
            
            for module_name, result in results.items():
                f.write(f"### {module_name.upper()} Module\n\n")
                
                if result:
                    if isinstance(result, dict):
                        for key, value in result.items():
                            if isinstance(value, list):
                                f.write(f"- **{key}:** {len(value)} items found\n")
                                if len(value) <= 10:  # Show first 10 items
                                    for item in value:
                                        f.write(f"  - {item}\n")
                                elif len(value) > 10:
                                    for item in value[:10]:
                                        f.write(f"  - {item}\n")
                                    f.write(f"  - ... and {len(value)-10} more\n")
                            else:
                                f.write(f"- **{key}:** {value}\n")
                    elif isinstance(result, list):
                        f.write(f"- **Results:** {len(result)} items found\n")
                        if len(result) <= 10:
                            for item in result:
                                f.write(f"  - {item}\n")
                        else:
                            for item in result[:10]:
                                f.write(f"  - {item}\n")
                            f.write(f"  - ... and {len(result)-10} more\n")
                    else:
                        f.write(f"- **Result:** {result}\n")
                else:
                    f.write("- No results found\n")
                
                f.write("\n")