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
