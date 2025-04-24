# KeyDefender - Anti-Keylogger Virtual Keyboard

KeyDefender is a secure desktop application designed to protect password entry from keyloggers by providing a virtual keyboard with randomizable layout.

## Features

- **Virtual Keyboard**: Enter passwords without using the physical keyboard
- **Randomizable Layout**: Keyboard layout can be randomized to prevent pattern recognition
- **Auto-Type**: Securely type passwords into applications
- **Clipboard Protection**: Automatic clipboard clearing for secure copy-paste
- **Keylogger Detection**: Basic detection of potential keyloggers running on the system
- **Dark/Light Mode**: Support for both dark and light themes

## Installation

### Prerequisites

- Python 3.7 or higher
- The required dependencies (see requirements.txt)

### Steps

1. Clone the repository or download the source code
2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
python src/main.py
```

### Building an Executable

To create a standalone executable:

```
cd KeyDefender
pyinstaller --onefile --windowed --icon=assets/icon.ico src/main.py
```

The executable will be created in the `dist` directory.

## Usage

1. Launch KeyDefender
2. Use the virtual keyboard to type your password
3. Use one of the following options:
   - **Auto-Type**: Types the password into the focused application
   - **Copy to Clipboard**: Copies password to clipboard (automatically cleared after a few seconds)
   - **Randomize Layout**: Randomizes the keyboard layout for increased security

## Security Features

- **Random Keyboard Layout**: Makes it harder for keyloggers to track key presses
- **Automatic Clipboard Clearing**: Prevents password from remaining in clipboard
- **Keylogger Detection**: Basic detection of known keylogger processes

## License

This project is open-source software.

## Disclaimer

KeyDefender provides a layer of protection against basic keyloggers but cannot guarantee complete security against all types of malware. Always ensure your system is properly secured with anti-virus software and keep your system updated. 