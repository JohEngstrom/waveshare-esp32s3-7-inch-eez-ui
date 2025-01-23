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

## 📝 Project Overview

This project provides a comprehensive example of integrating an EEZ-Studio LVGL project with the [Waveshare ESP32-S3 7 Inch Board](https://www.waveshare.com/esp32-s3-touch-lcd-7.htm). It demonstrates how to:
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

*New* Use the included command to copy from a provided `./ui/` folder into the `./components/ui/` directory. 
```bash
python import_eez_ui.py -d /path/to/eez/ui # To set the directory to your EEZ-Studios output folder. Typically: './eez-project/project_name/src/ui'
python import_eez_ui.py -m copy-ui
```

### 4. Configure actions.h (Only required if you defined native actions in EEZ-Studio)
1. Open `./components/ui/actions.h`
2. Copy all of your functions declared with extern into the file `./components/ui/actions.c`
3. In `./components/ui/actions.c` remove the extern keyword from the beginning of all your functions.
4. Still in `./components/ui/actions.c` remove the semicolon at the end and add a set of curly braces in it's place.
5. You can leave these blank if you want, but this is where your custom action code goes
* There is an example inside of the `./components/ui/actions.c`

*New* Use the included command to perform this for you in the `./components/ui/` directory.
```bash
python import_eez_ui.py -m fix-actions
```

## 5. Edit UI Files (If EEZ doesn't generate the proper LVGL includes)
EEZ-Studio has an option to change the library include. I have noticed that sometimes it still spits out `lvgl/lvgl.h` despite being set to `lvgl.h`

This is a quick fix, though slightly annoying.

You will have to go through all of the files in `./components/ui/` and change `lvgl/lvgl.h` to `lvgl.h`

*New* Use the included command to perform this for you on all files in the `./components/ui/` directory.
```bash
python import_eez_ui.py -m fix-headers
```


## 📊 Alternative Method: import_eez_ui.py
This script simplifies the process of importing and integrating UI components into your project. It automates several tasks, making your development workflow more efficient.

**Key Features**

- **Automated File Copying:** Copies UI files from your source directory to the designated project folder `./components/ui` .

- **Header Modification:** Automatically replaces `lvgl/lvgl.h` with `lvgl.h` in all UI files.

- **CMake Integration:** Helps you manage the build process by checking for and optionally replacing CMakeLists.txt with a default template.

- **Action Implementation:** Copies extern functions from actions.h to actions.c and provides basic function stubs for easy implementation.

**Usage**

To run the script, execute the following command in your terminal:

```bash
python import_eez_ui.py [options]
```

**Specifying Source Directory**

Use the `-d` or `--directory` option to specify the path to your UI source directory.

Example:
```bash
python import_eez_ui.py -d /path/to/your/ui/components
```
If not provided, the script will attempt to use the last specified directory from a configuration file.

**Selecting Import Mode**

Use the `-m` or `--mode` option to specify the specific actions you want to perform.

Available modes:


- copy-ui: Only copy UI files.
- fix-headers: Only replace headers.
- fix-cmake: Only check and optionally replace CMakeLists.txt.
- fix-actions: Only copy and create stubs for action functions.
- all (default): Perform all actions.

**Viewing Help**
Use the `-h` or `--help` option to display a list of available options and their descriptions.

Example:
```bash
python import_eez_ui.py -h
```

**Example Usage**
To import all UI components from `/path/to/your/ui/components` and perform all actions:

```bash
python import_eez_ui.py -d /path/to/your/ui/components
```

**Note**
The script assumes a specific project structure and file organization. It is expected that you are pointing to an EEZ projects You may need to adapt the script for projects with different structures. This documentation provides a concise overview of the ui_import.py script. For detailed information and troubleshooting, refer to the script's source code.

## 🤔 Frequently Asked Questions (FAQ)

### LVGL Header Issue
**Problem**: `fatal error: lvgl/lvgl.h: No such file or directory`

**Solution**: 
- Manually replace `lvgl/lvgl.h` with `lvgl.h` in all files under `./components/ui/`
- __*New*__ Run `python import_eez_ui.py -m fix-headers` to allow the script to fix the headers.

### Undefined Action References
**Problem**: Undefined references to `action_****`

**Solution**:
- Create an `actions.c` file
- Use the template in `./templates/actions.c`
- Define your custom actions (can be left blank initially)
- __*New*__ Run `python import_eez_ui.py -m fix-actions` to allow the script to import functions from `./components/ui/actions.h`.

### CMake Component Resolution
**Problem**: `CMake Error: Failed to resolve component 'ui'`

**Solution**:
- Restore `CMakeLists.txt` in `./components/ui/`
- Use the template at `./templates/CMakeLists.txt`
- __*New*__ Run `python import_eez_ui.py -m fix-cmake` to allow the script to fix the cmake file in `./components/ui/`.

## 🌐 Additional Resources

- 📖 [Waveshare ESP32-S3 7 Inch Wiki](https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-7)
- 📚 [LVGL Documentation](https://docs.lvgl.io/)
- 🛠 [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- 🏗️ [EEZ-Studio](https://github.com/eez-open/studio)

## 🛣️ Roadmap
These are my up coming project goals:
- __Support More Waveshare Boards__ - This should be relatively easy as the underlying code uses the esp_lcd code.
- __Support For Squareline Studios__ - This should also be relatively easy as the files and folder structure are basically identical from both tools
- __Easy Config Peripherals__ - I would like to set up a quick easy way to enable and init the peripherals as you need them with a quick define or simple config file
- __More To Come__ - I am always thinking of ways to make this better and am open to contributions!

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


---

*Happy Coding! 👨‍💻👩‍💻*

