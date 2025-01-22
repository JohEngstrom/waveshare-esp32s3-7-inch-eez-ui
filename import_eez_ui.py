import os
import shutil
import re
import argparse
import configparser
import sys

# Default source directory
DEFAULT_SOURCE_DIR = "ui"

# Configuration file path
CONFIG_FILE = ".ui_import_config"

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)

def update_config(config, source_dir):
    if 'Settings' in config:
        del config['Settings']
    config['Settings'] = {'source_dir': source_dir}
    save_config(config)

def validate_ui_source(source_dir):
    """
    Validates the UI source directory.

    Args:
        source_dir: Path to the UI source directory.

    Returns:
        True if valid, False otherwise.
    """
    if not os.path.isdir(source_dir):
        print(f"Error: '{source_dir}' is not a directory.")
        return False

    if not os.path.isfile(os.path.join(source_dir, "ui.h")):
        print(f"Error: '{source_dir}' does not contain a 'ui.h' file.")
        return False

    return True

def copy_ui(source_dir):
    """
    Copies UI files from the source directory to the destination.

    Args:
        source_dir: Path to the UI source directory.
    """
    print(f"Copying UI files from '{source_dir}' to 'components/ui'.")
    dest_dir = "components/ui"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    copied_files = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, os.path.relpath(src_file, source_dir))
            shutil.copy2(src_file, dest_file)
            copied_files += 1

    print(f"Copied {copied_files} files.")

def fix_headers():
    """
    Replaces "lvgl/lvgl.h" with "lvgl.h" in all UI files.
    """
    count = 0
    for root, dirs, files in os.walk("components/ui"):
        for file in files:
            if file.endswith(".h") or file.endswith(".c"):
                file_path = os.path.join(root, file)
                with open(file_path, "r+") as f:
                    content = f.read()
                    if "lvgl/lvgl.h" in content:
                        print(f"Replacing 'lvgl/lvgl.h' with 'lvgl.h' in {file_path}")
                        content = content.replace("lvgl/lvgl.h", "lvgl.h")
                        f.seek(0)
                        f.write(content)
                        f.truncate()
                        count += 1
    print(f"Total edits performed: {count}")

def fix_cmake():
    """
    Checks if CMakeLists.txt exists and prompts the user to replace it with the default.
    """
    cmake_file = "components/ui/CMakeLists.txt"
    if os.path.exists(cmake_file):
        print(f"{cmake_file} found. Leaving in place.")
    else:    
        print(f"{cmake_file} missing. Do you want to replace it with the default? (y/n)")
        response = input().lower()
        if response == "y":
            shutil.copy2("./templates/CMakeLists.txt", cmake_file)
            print(f"{cmake_file} replaced with the default.")
        else:
            print(f"{cmake_file} not replaced.")

def fix_actions():
    """
    Copies extern functions from actions.h to actions.c.
    """
    actions_h = "components/ui/actions.h"
    actions_c = "components/ui/actions.c"
    actions_template = "templates/actions.c"
    if os.path.exists(actions_h):
        with open(actions_h, "r") as f:
            content = f.read()
            extern_functions = re.findall(r"extern\s+void\s+(\w+)\s*\(.*?\);", content)
            existing_functions = []
            if os.path.exists(actions_c):
                print(f"{actions_c} found. Using existing actions.c.")
                with open(actions_c, "r") as f:
                    content = f.read()
                    existing_functions = re.findall(r"void\s+(\w+)\s*\(.*?\)", content)
            else: 
                print(f"{actions_c} not found. Creating new actions.c")
                if os.path.exists(actions_template):
                    shutil.copy2(actions_template, actions_c)
                else:
                    print(f"{actions_template} not found. Skipping template copy.")
                
            print(f"Found {len(extern_functions)} extern functions in {actions_h}")    
            with open(actions_c, "a") as f:
                print(f"Writing extern functions to {actions_c}")
                for func in extern_functions:
                    print(f"Found extern function: {func}")
                    if func not in existing_functions:
                        print(f"Function {func} not found in {actions_c}.")
                        print(f"Adding extern function: {func}")
                        f.write(f"\nvoid {func}() {{\n\t// TODO: implement {func}\n}}\n")
                    else:
                        print(f"Function {func} found in {actions_c} already. Skipping.")
    else:
        print(f"{actions_h} not found. Skipping.")

def main():
    parser = argparse.ArgumentParser(description='Import EEZ UI')
    parser.add_argument('-d', '--directory', help='Source directory to import ui files from EEZ-Studio Usually similar to "./eez-projects/project_name/src/ui" ')
    parser.add_argument('-m', '--mode', default='all', choices=['copy-ui', 'fix-headers', 'fix-cmake', 'fix-actions', 'all'], help='Mode selection - Allows you to run only portions of the script for specific functions')
    args = parser.parse_args()

    config = load_config()
    source_dir = args.directory

    if source_dir:
        if validate_ui_source(source_dir):
            update_config(config, source_dir)
            print(f"Directory '{source_dir}' set as default import directory.")
            sys.exit(1)
        else:
            print(f"Directory '{source_dir}' is not a valid UI source directory.")
            sys.exit(1)
    else:
        if 'Settings' in config:
            source_dir = config['Settings']['source_dir']
        else:
            print("No source directory specified. Please use -d or --directory to specify the source directory.")
            print(f"Example usage: python ui_import.py -d /path/to/your/ui/source/directory")
            sys.exit(1)

    if not validate_ui_source(source_dir):
        sys.exit(1)

    if args.mode == 'copy-ui' or args.mode == 'all':
        copy_ui(source_dir)
    if args.mode == 'fix-headers' or args.mode == 'all':
        fix_headers()
    if args.mode == 'fix-cmake' or args.mode == 'all':
        fix_cmake()
    if args.mode == 'fix-actions' or args.mode == 'all':
        fix_actions()
        
    if args.mode == 'all':
        print("UI import complete.")

if __name__ == "__main__":
    main()