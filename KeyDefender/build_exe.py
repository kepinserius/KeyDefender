#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform

def build_executable():
    """Build the KeyDefender executable using PyInstaller"""
    
    print("Building KeyDefender executable...")
    
    # Determine the system platform
    os_name = platform.system().lower()
    
    # Base command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=KeyDefender",
        "--clean",
    ]
    
    # Add icon if available
    icon_path = os.path.join("assets", "icon.ico")
    if os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    
    # Add the main script
    cmd.append(os.path.join("src", "main.py"))
    
    try:
        # Run PyInstaller
        subprocess.run(cmd, check=True)
        
        print("\nBuild completed successfully!")
        print(f"Executable can be found in the 'dist' directory.")
        
        # Additional instructions based on OS
        if os_name == "windows":
            print("\nTo run the application, double-click 'dist/KeyDefender.exe'")
        elif os_name == "linux":
            print("\nTo run the application, execute 'dist/KeyDefender'")
        elif os_name == "darwin":  # macOS
            print("\nTo run the application, execute 'dist/KeyDefender'")
            
    except subprocess.CalledProcessError as e:
        print(f"\nError building executable: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    # Ensure we're in the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    build_executable() 