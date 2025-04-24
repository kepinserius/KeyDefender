#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import psutil
import ctypes
from PyQt5.QtWidgets import QMessageBox

class KeyloggerDetector:
    """
    A class for detecting potential keyloggers on Windows systems.
    This is a basic implementation that uses process scanning.
    """
    
    def __init__(self):
        # Lists of known keylogger process names (partial matches)
        self.suspicious_process_names = [
            "keylog", "ardamax", "actual spy", "spyrix", "refog", 
            "spytector", "revealer", "spyhunter", "spytech", "keystroke"
        ]
        
        self.results = {
            "suspicious_processes": [],
        }
    
    def detect_all(self):
        """Run all detection methods and return results"""
        self.detect_processes()
        return self.results
    
    def detect_processes(self):
        """Scan running processes for potential keyloggers"""
        self.results["suspicious_processes"] = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                process_name = proc.info['name'].lower() if proc.info['name'] else ""
                
                # Check for suspicious process names
                for sus_name in self.suspicious_process_names:
                    if sus_name in process_name:
                        self.results["suspicious_processes"].append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "reason": f"Name contains '{sus_name}'"
                        })
                        break
        except Exception as e:
            print(f"Error in process detection: {e}")
        
        return self.results["suspicious_processes"]
    
    def get_formatted_results(self):
        """Get results formatted as a readable string"""
        output = []
        
        output.append("===== KeyDefender Keylogger Detection Results =====")
        output.append("")
        
        # Suspicious processes
        output.append("--- Suspicious Processes ---")
        if not self.results["suspicious_processes"]:
            output.append("No suspicious processes detected.")
        else:
            for proc in self.results["suspicious_processes"]:
                output.append(f"PID: {proc['pid']} - Name: {proc['name']}")
                output.append(f"Reason: {proc['reason']}")
                output.append("")
        
        return "\n".join(output)

    def show_results_dialog(self, parent=None):
        """Display results in a message box"""
        results_text = self.get_formatted_results()
        
        msg = QMessageBox(parent)
        msg.setWindowTitle("Keylogger Detection Results")
        msg.setText("Keylogger Detection Scan Complete")
        msg.setDetailedText(results_text)
        
        if self.results["suspicious_processes"]:
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText(f"Found {len(self.results['suspicious_processes'])} suspicious processes!")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText("No keyloggers detected.")
            
        msg.exec_()


# For testing
if __name__ == "__main__":
    detector = KeyloggerDetector()
    detector.detect_all()
    print(detector.get_formatted_results()) 