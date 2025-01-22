# EEZ-Studio LVGL Project for Waveshare ESP32-S3      7 Inch Board

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
It is based off the demo's provided by waveshare on their [wiki](https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-7)

## 🎯 Supported Hardware

| Category | Specification |
|---------|---------------|
| **Target** | Waveshare ESP32-S3 7 Inch |
| **LCD Controller** | ST7262 |
| **Touch Controller** | GT911 |

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:
- [VS Code](https://code.visualstudio.com/)
- [ESP-IDF Extension](https://github.com/espressif/vscode-esp-idf-extension) can also be installed directly from VSCode extension manager
- ESP-IDF V5.4 with tools and virtual environment setup either by the ESP-IDF or your own manual install
- The [Waveshare Wiki](https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-7) has a great example on how to set up VSCode and get the ESP-IDF installed

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

## 📊 Alternative Method: ui_import.py
This script simplifies the process of importing and integrating UI components into your project. It automates several tasks, making your development workflow more efficient.

**Key Features**
Automated File Copying: Copies UI files from your source directory to the designated project folder `./components/ui` .

Header Modification: Automatically replaces `lvgl/lvgl.h` with `lvgl.h` in all UI files.

CMake Integration: Helps you manage the build process by checking for and optionally replacing CMakeLists.txt with a default template.

Action Implementation: Copies extern functions from actions.h to actions.c and provides basic function stubs for easy implementation.

**Usage**
To run the script, execute the following command in your terminal:

```bash
python ui_import.py [options]
'''

**Specifying Source Directory**
Use the `-d` or `--directory` option to specify the path to your UI source directory.

Example:
```bash
python ui_import.py -d /path/to/your/ui/components
'''
If not provided, the script will attempt to use the last specified directory from a configuration file.

**Selecting Import Mode**

Use the `-m` or `--mode` option to specify the specific actions you want to perform.

Available modes:

-`copy-ui`: Only copy UI files.
-`fix-headers`: Only replace headers.
-`fix-cmake`: Only check and optionally replace CMakeLists.txt.
-`fix-actions`: Only copy and create stubs for action functions.
-`all` (default): Perform all actions.

**Viewing Help**
Use the `-h` or `--help` option to display a list of available options and their descriptions.

Example:
```bash
python ui_import.py -h
'''

**Example Usage**
To import all UI components from `/path/to/your/ui/components` and perform all actions:

```bash
python ui_import.py -d /path/to/your/ui/components
'''

**Note**
The script assumes a specific project structure and file organization. You may need to adapt the script for projects with different structures. This documentation provides a concise overview of the ui_import.py script. For detailed information and troubleshooting, refer to the script's source code.

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

