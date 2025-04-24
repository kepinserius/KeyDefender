#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from keydefender import KeyDefender

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = KeyDefender()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 