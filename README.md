# Text to QMK Keycode Converter

![Cross-Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-green)

A cross-platform CLI utility that converts text input into QMK firmware keycode sequences with automatic clipboard integration and input timeout handling. Perfect for keyboard firmware developers and enthusiasts.

## Features ✨

- **OS Agnostic Operation**  
  Works seamlessly on Windows, macOS, and Linux systems

- **Bilingual Interface**  
  Supports both Chinese (中文) and English prompts

- **Smart Conversion**  
  Auto-converts:
  - Uppercase letters → Shift-modified keycodes
  - Symbols → Shifted equivalents (e.g., `!` → `Shift+1`)
  - Special characters → QMK-compatible sequences

- **Timing Control**  
  Configurable delay intervals between key actions (default: 15ms)

- **Safety Features**  
  - 300-second input timeout
  - Clean exit with Ctrl+C
  - Clipboard sanitization

## Installation 📦

### Requirements
```bash
# Linux users need xclip:
sudo apt-get install xclip  # Debian/Ubuntu
sudo dnf install xclip     # Fedora
```

## Usage 🚀

### Basic Conversion
```python
python3 text_to_qmk_keycodes.py
```

### Language Selection
```python
# For Chinese interface:
ttqk = Text_To_QMK_Keycodes(language='CN')

# For English interface (default):
ttqk = Text_To_QMK_Keycodes(language='EN')
```

**### Sample Workflow:**
1. Run the script
2. Enter text at the prompt: `Hello!`
3. Get converted output:
```
{+KC_LSFT}{15}h{-KC_LSFT}{15}e{15}l{15}l{15}o{+KC_LSFT}{15}1{-KC_LSFT}
```
4. Result automatically copied to clipboard

## Customization ⚙️
### Modify Delays
```python
def __init__(self, language):
    self.delay = 15    # Change keypress delay (ms)
    self.timeout = 300 # Change input timeout (sec)
```
### Add Symbol Mappings
Extend the `symbol_dict` in `convert_text_to_qmk_keycodes()`:
```python
symbol_dict = {
    '!':'1', 
    '@':'2',
    # Add new entries using format:
    # 'SYMBOL': 'BASE_KEY'
}
```
## Platform Notes ℹ️
|OS       | Dependencies    | Input Handling Method|
|:--------|:----------------|:---------------------|
|Windows  | Built-in        | `msvcrt` module      |
|macOS    | None            | `select` module      |
|Linux    | `xclip` package | `select` module      |
## Troubleshooting 🔧
**### Linux Clipboard Issues:**
```bash
# If you see xclip errors:
sudo apt-get install xclip && export DISPLAY=:0
```
**### Long Strings Not Converting:**
* The program handles input line-by-line
* Keep individual lines under 1024 characters

## Contributing 🤝
Pull requests are welcome! Please:
1. Maintain cross-platform compatibility
2. Keep methods OS-agnostic
3. Add Chinese/English prompt support for new features

## License 📄
MIT License - See ![LICENSE](https://github.com/jonschlinkert/markdown-link/blob/master/LICENSE) for details

**Pro Tip:** 🔥 Combine with ![QMK Firmware](https://docs.qmk.fm/) to create custom keyboard macros!
