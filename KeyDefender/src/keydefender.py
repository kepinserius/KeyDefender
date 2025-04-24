#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import time
import platform
import pyperclip
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                           QHBoxLayout, QLineEdit, QApplication, QCheckBox,
                           QLabel, QGridLayout, QFrame, QTabWidget, QComboBox,
                           QMessageBox, QAction, QMenu)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont
import qdarkstyle
from keylogger_detector import KeyloggerDetector

# Constants
APP_NAME = "KeyDefender"
APP_VERSION = "1.0.0"

# Check if running in WSL
def is_wsl():
    """Check if running in Windows Subsystem for Linux"""
    if os.path.exists('/proc/version'):
        with open('/proc/version', 'r') as f:
            if 'microsoft' in f.read().lower():
                return True
    return False

# Global flag for WSL environment
IS_WSL = is_wsl()

class KeyDefender(QMainWindow):
    """Main application window for KeyDefender Anti-Keylogger Virtual Keyboard"""
    
    def __init__(self):
        super().__init__()
        
        self.clipboard_data = ""
        self.target_app = None
        self.dark_mode = False
        self.keylogger_detector = KeyloggerDetector()
        
        self.init_ui()
        self.setup_keyboard()
        self.setup_timers()
        
        # Show warning if running in WSL
        if IS_WSL:
            self.statusBar().showMessage("Running in WSL environment - clipboard features limited", 5000)
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{APP_NAME} - Anti-Keylogger Virtual Keyboard")
        self.setMinimumSize(800, 400)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Password field
        password_layout = QHBoxLayout()
        
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setReadOnly(True)
        self.password_field.setPlaceholderText("Your password will appear here")
        
        self.show_password_btn = QPushButton("Show")
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_password)
        
        password_layout.addWidget(self.password_field)
        password_layout.addWidget(self.show_password_btn)
        password_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(password_layout)
        
        # Keyboard container
        self.keyboard_frame = QFrame()
        self.keyboard_frame.setFrameShape(QFrame.StyledPanel)
        self.keyboard_layout = QGridLayout()
        self.keyboard_frame.setLayout(self.keyboard_layout)
        
        main_layout.addWidget(self.keyboard_frame)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.autotype_btn = QPushButton("Auto-Type")
        self.autotype_btn.clicked.connect(self.auto_type)
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        if IS_WSL:
            self.copy_btn.setToolTip("Limited functionality in WSL environment")
        
        self.randomize_btn = QPushButton("Randomize Layout")
        self.randomize_btn.clicked.connect(self.randomize_keyboard)
        
        self.theme_toggle = QPushButton("Toggle Dark Mode")
        self.theme_toggle.clicked.connect(self.toggle_theme)
        
        self.detect_keylogger_btn = QPushButton("Detect Keyloggers")
        self.detect_keylogger_btn.clicked.connect(self.detect_keyloggers)
        
        action_layout.addWidget(self.autotype_btn)
        action_layout.addWidget(self.copy_btn)
        action_layout.addWidget(self.randomize_btn)
        action_layout.addWidget(self.theme_toggle)
        action_layout.addWidget(self.detect_keylogger_btn)
        
        main_layout.addLayout(action_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Menu bar
        self.setup_menu()
        
    def setup_menu(self):
        """Set up the application menu"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Security menu
        security_menu = menubar.addMenu('Security')
        
        detect_action = QAction('Detect Keyloggers', self)
        detect_action.triggered.connect(self.detect_keyloggers)
        security_menu.addAction(detect_action)
        
        # Settings menu
        settings_menu = menubar.addMenu('Settings')
        
        toggle_theme_action = QAction('Toggle Theme', self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(toggle_theme_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_keyboard(self):
        """Set up the virtual keyboard"""
        # Clear existing keyboard if it exists
        for i in reversed(range(self.keyboard_layout.count())): 
            widget = self.keyboard_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Key sets
        self.keys = {
            'numbers': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            'letters': [chr(i) for i in range(ord('a'), ord('z')+1)],
            'symbols': ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', 
                        '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/']
        }
        
        # Create randomized lists
        numbers = list(self.keys['numbers'])
        letters = list(self.keys['letters'])
        symbols = list(self.keys['symbols'])
        
        random.shuffle(numbers)
        random.shuffle(letters)
        random.shuffle(symbols)
        
        # Add number keys (row 0)
        for i, key in enumerate(numbers):
            self.add_key_button(key, 0, i)
        
        # Add letter keys (rows 1-3)
        row1_end = 10
        row2_end = row1_end + 9
        row3_end = row2_end + 7
        
        for i, key in enumerate(letters[:row1_end]):
            self.add_key_button(key, 1, i)
            
        for i, key in enumerate(letters[row1_end:row2_end]):
            self.add_key_button(key, 2, i)
            
        for i, key in enumerate(letters[row2_end:]):
            self.add_key_button(key, 3, i)
        
        # Add symbol keys (rows 4-5)
        row4_end = 15
        
        for i, key in enumerate(symbols[:row4_end]):
            self.add_key_button(key, 4, i)
            
        for i, key in enumerate(symbols[row4_end:]):
            self.add_key_button(key, 5, i)
        
        # Add space and backspace (row 6)
        space_btn = QPushButton("Space")
        space_btn.clicked.connect(lambda: self.add_character(" "))
        self.keyboard_layout.addWidget(space_btn, 6, 3, 1, 5)
        
        backspace_btn = QPushButton("Backspace")
        backspace_btn.clicked.connect(self.remove_character)
        self.keyboard_layout.addWidget(backspace_btn, 6, 8, 1, 3)
    
    def add_key_button(self, key, row, col):
        """Add a key button to the keyboard layout"""
        key_btn = QPushButton(key)
        key_btn.setFixedSize(50, 50)
        key_btn.clicked.connect(lambda: self.add_character(key))
        self.keyboard_layout.addWidget(key_btn, row, col)
    
    def add_character(self, char):
        """Add a character to the password field"""
        current_text = self.password_field.text()
        self.password_field.setText(current_text + char)
    
    def remove_character(self):
        """Remove the last character from the password field"""
        current_text = self.password_field.text()
        if current_text:
            self.password_field.setText(current_text[:-1])
    
    def clear_password(self):
        """Clear the password field"""
        self.password_field.clear()
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_btn.isChecked():
            self.password_field.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText("Hide")
        else:
            self.password_field.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText("Show")
    
    def randomize_keyboard(self):
        """Randomize the keyboard layout"""
        self.setup_keyboard()
        self.statusBar().showMessage("Keyboard layout randomized", 2000)
    
    def copy_to_clipboard(self):
        """Copy password to clipboard"""
        password = self.password_field.text()
        if password:
            self.clipboard_data = password
            
            if IS_WSL:
                # In WSL environment, just show a message
                QMessageBox.information(self, "WSL Environment", 
                                     "Clipboard functionality is limited in WSL environment. Please manually copy your password.")
                self.statusBar().showMessage("Clipboard features limited in WSL", 2000)
                return
                
            try:
                pyperclip.copy(password)
                self.statusBar().showMessage("Password copied to clipboard", 2000)
            except Exception as e:
                self.statusBar().showMessage(f"Error copying to clipboard: {e}", 2000)
                QMessageBox.warning(self, "Clipboard Error", 
                                  "Could not copy to clipboard. This may be due to system limitations.")
    
    def auto_type(self):
        """Auto-type the password to the target application"""
        # For demonstration purposes, we'll just show a message
        # In a real app, you would use a library like pyautogui to type into the focused window
        password = self.password_field.text()
        if password:
            self.statusBar().showMessage("Auto-typing password...", 2000)
            QMessageBox.information(self, "Auto-Type", 
                                   "In a full implementation, the password would be typed into the focused window.")
    
    def detect_keyloggers(self):
        """Run keylogger detection and show results"""
        self.statusBar().showMessage("Scanning for keyloggers...", 3000)
        self.keylogger_detector.detect_all()
        self.keylogger_detector.show_results_dialog(self)
    
    def setup_timers(self):
        """Set up timers for security features"""
        # Clipboard clearing timer - disable in WSL environment
        if not IS_WSL:
            self.clipboard_timer = QTimer(self)
            self.clipboard_timer.timeout.connect(self.check_clipboard)
            self.clipboard_timer.start(5000)  # Check every 5 seconds
    
    def check_clipboard(self):
        """Check and clear clipboard if it contains our password"""
        if IS_WSL:
            return
            
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard == self.clipboard_data and self.clipboard_data:
                try:
                    pyperclip.copy('')
                    self.clipboard_data = ""
                    self.statusBar().showMessage("Clipboard cleared for security", 2000)
                except Exception as e:
                    print(f"Error clearing clipboard: {e}")
        except Exception as e:
            print(f"Error accessing clipboard: {e}")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            self.theme_toggle.setText("Light Mode")
            self.statusBar().showMessage("Dark mode enabled", 2000)
        else:
            QApplication.instance().setStyleSheet("")
            self.theme_toggle.setText("Dark Mode")
            self.statusBar().showMessage("Light mode enabled", 2000)
    
    def show_about(self):
        """Show the about dialog"""
        QMessageBox.about(self, f"About {APP_NAME}",
            f"<h2>{APP_NAME} v{APP_VERSION}</h2>"
            "<p>An anti-keylogger virtual keyboard application.</p>"
            "<p>Features:</p>"
            "<ul>"
            "<li>Keyboard with randomizable layout</li>"
            "<li>Auto-type to target applications</li>"
            "<li>Clipboard auto-clear</li>"
            "<li>Keylogger detection</li>"
            "<li>Dark/light mode</li>"
            "</ul>"
            "<p>&copy; 2023 KeyDefender</p>") 