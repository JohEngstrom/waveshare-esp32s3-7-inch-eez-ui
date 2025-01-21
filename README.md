# 🖥️ EEZ-Studio LVGL Project for Waveshare ESP32-S3 7 Inch Board

## Badges

[![Project Status](https://img.shields.io/badge/status-development-yellow)](https://github.com/yourusername/yourproject)
[![Platform](https://img.shields.io/badge/platform-ESP32--S3-blue)](https://www.espressif.com/en/products/socs/esp32-s3)
[![LVGL](https://img.shields.io/badge/LVGL-v8.3-orange)](https://lvgl.io/)
[![ESP-IDF](https://img.shields.io/badge/ESP--IDF-v5.4-green)](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

## 📋 Table of Contents

- [📝 Project Overview](#-project-overview)
- [🎯 Supported Specifications](#-supported-specifications)
- [🛠 Prerequisites](#-prerequisites)
- [🚀 Quick Start Guide](#-quick-start-guide)
- [❓ Frequently Asked Questions](#-frequently-asked-questions)
- [📚 Additional Resources](#-additional-resources)
- [📄 License](#-license)

## 📝 Project Overview"

This project provides a comprehensive example of integrating an EEZ-Studio LVGL project with the Waveshare ESP32-S3 7 Inch Board. It demonstrates how to:
- Configure and run LVGL on the Waveshare ESP32-S3 7 Inch Board
- Implement custom UI designs from EEZ-Studio's Easily on this Waveshare board
- Use EEZ-Studio's output files in ESP-IDF

## 🎯 Supported Specifications

| Category | Specification |
|---------|---------------|
| **Target** | Waveshare ESP32-S3 7 Inch |
| **LCD Controller** | ST7701 |
| **Touch Controller** | GT911 |

## 🛠 Prerequisites

Before you begin, ensure you have:
- [VS Code](https://code.visualstudio.com/) installed
- [ESP-IDF Extension](https://github.com/espressif/vscode-esp-idf-extension) for VS Code
- ESP-IDF V5.4 with tools and virtual environment setup either by the ESP-IDF or your own manual install

## 🚀 Quick Start Guide

### 1. Clone the Project
```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Prepare EEZ-Studio Project
1. Open your own ui project in EEZ-Studio
2. Export/build the project
3. Locate the generated `ui` folder (typically similar to `/path/to/eez-projects/project_name/ui`)

### 3. Setup and Build
1. Copy the `ui` folder onto `./components/ui`
2. Open the project in VSCode with ESP-IDF extension
3. Build and flash the project


### 4. Configure actions.h (Only if you defined native actions in EEZ-Studio)
1. Open `./components/ui/actions.h`
2. Copy all of your functions declared with extern into the file `./components/ui/actions.c`
3. In `./components/ui/actions.c` remove the extern keyword from the beginning of all your functions.
4. Still in `./components/ui/actions.c` remove the semicolon at the end and add a set of curly braces in it's place.
5. You can leave these blank if you want, but this is where your custom action code goes
* There is an example inside of the `./components/ui/actions.c`

## 5. Edit UI Files (If EEZ doesn't generate the proper LVGL includes)
EEZ-Studio has an option to change the library include. I have noticed that is still spits out lvgl/lvgl.h despite being set to lvgl.h

This is a quick fix, though slightly annoying.

You will have to go through all of the files in `./components/ui/` and change `lvgl/lvgl.h` to `lvgl.h`

## 🤔 Frequently Asked Questions (FAQ)

### LVGL Header Issue
**Problem**: `fatal error: lvgl/lvgl.h: No such file or directory`

**Solution**: 
- Manually replace `lvgl/lvgl.h` with `lvgl.h` in all files under `./components/ui/`
- *Tip*: Consider creating a bash/python script for automated replacement

### Undefined Action References
**Problem**: Undefined references to `action_****`

**Solution**:
- Create an `actions.c` file
- Use the template in `./templates/actions.c`
- Define your custom actions (can be left blank initially)

### CMake Component Resolution
**Problem**: `CMake Error: Failed to resolve component 'ui'`

**Solution**:
- Restore `CMakeLists.txt` in `./components/ui/`
- Use the template at `./templates/CMakeLists.txt`

## 🌐 Additional Resources
- [Waveshare ESP32-S3 7 Inch Wiki](https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-7)

## 🌐 Additional Resources

- 📖 [Waveshare ESP32-S3 7 Inch Wiki](https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-7)
- 📚 [LVGL Documentation](https://docs.lvgl.io/)
- 🛠 [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


---

*Happy Coding! 👨‍💻👩‍💻*
