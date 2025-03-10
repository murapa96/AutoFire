# RapidFire

[![PyPI version](https://badge.fury.io/py/rapidfire.svg)](https://badge.fury.io/py/rapidfire)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/murapa96/RapidFire)](https://github.com/murapa96/RapidFire/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/murapa96/RapidFire)](https://github.com/murapa96/RapidFire/commits/main)

A utility for automatically pressing keys at regular intervals.

## Description

RapidFire is a simple auto key-press utility that simulates continuous key presses after you've pressed a key once. It's useful for scenarios where repeated key presses are needed, such as in games, form filling, or text repetition.

## Features

- Start auto-pressing by pressing any key once
- Continue pressing at 1-second intervals (configurable)
- Stop immediately with a key combination (Ctrl+Esc+W) (also configurable)
- Lightweight with minimal dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python rapid_fire.py
```

2. Press any key to begin auto-pressing that key every second
3. Press Ctrl+Esc+W to stop the auto-pressing functionality

### Fallback CLI Mode

If the keyboard listener fails to initialize, the program will automatically switch to Command-Line Interface (CLI) mode. In this mode, you can use the following commands:

- `start <key>` - Start auto-pressing a key (e.g., 'start a' or 'start space')
- `stop` - Stop current auto-pressing
- `interval <seconds>` - Change the press interval (e.g., 'interval 0.5')
- `exit` or `quit` - Exit the program

### Special Keys

For special keys, use these keywords:
- `space` - Space key
- `enter` - Enter key
- `tab` - Tab key
- `esc` - Escape key
- `ctrl` - Control key
- `alt` - Alt key
- `shift` - Shift key

## Advanced Configuration

You can modify the `rapid_fire.py` script to change:

- Key press interval (default: 1 second)
- Stop key combination (default: Ctrl+Esc+W)

## Requirements

- Python 3.6+
- keyboard library (automatically installed via requirements.txt)

## Note

This utility requires root/administrator privileges to run on most systems due to the keyboard library needing global keyboard access.

## License

[MIT](LICENSE)

## Author

Pablo Ramos Muras ([@murapa96](https://github.com/murapa96))