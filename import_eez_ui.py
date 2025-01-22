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

    print(f"Copied {copied_files} files from '{source_dir}' to '{dest_dir}'.")


def fix_headers():
    """
    Replaces "lvgl/lvgl.h" with "lvgl.h" in all UI files.
    """
    header_dir = "components/ui"
    files_changed = 0
    for root, dirs, files in os.walk(header_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                file_content = f.read()

            modified_content = file_content.replace("lvgl/lvgl.h", "lvgl.h")

            if file_content != modified_content:
                with open(file_path, 'w') as f:
                    f.write(modified_content)
                files_changed += 1
                print(f"Replaced 'lvgl/lvgl.h' with 'lvgl.h' in '{file_path}'.")

    print(f"Replaced 'lvgl/lvgl.h' in {files_changed} files.")


def fix_cmake():
    """
    Checks if CMakeLists.txt exists and prompts the user to replace it with the default.
    """
    cmake_file = "components/ui/CMakeLists.txt"
    if not os.path.exists(cmake_file):
        print("CMakeLists.txt not found in 'components/ui'.")
        response = input("Replace with default? (y/n): ").lower()  # Add colon here
        if response == 'y':
            shutil.copy2("templates/CMakeLists.txt", cmake_file)
            print("Default CMakeLists.txt copied.")
        else:
            print("Warning: You will need to create your own CMakeLists.txt file.")

def fix_actions():
    """
    Copies extern functions from actions.h to actions.c.
    """
    actions_h_path = "components/ui/actions.h"
    actions_c_path = "components/ui/actions.c"

    if not os.path.exists(actions_h_path):
        print("actions.h not found.")
        return

    with open(actions_h_path, 'r') as f:
        actions_h_content = f.read()

    extern_functions = re.findall(r"extern void (\w+)\(.*\);", actions_h_content)

    if not extern_functions:
        print("No extern functions found in actions.h.")
        return

    if not os.path.exists(actions_c_path):
        print("actions.c not found.")
        if input("Replace with default? (y/n): ").lower() == 'y':
            shutil.copy2("templates/actions.c", actions_c_path)
            print("Default actions.c copied.")
        else:
            print("Warning: actions.c will need to be created manually.")

    with open(actions_c_path, 'r+') as f:
        actions_c_content = f.read()
        existing_functions = re.findall(r"void (\w+)\(.*\)\s*{", actions_c_content)

    new_functions = []
    for func in extern_functions:
        if func not in existing_functions:
            new_functions.append(func)

    if new_functions:
        print(f"Found {len(extern_functions)} extern functions in actions.h.")
        print(f"Previously added: {len(extern_functions) - len(new_functions)}")
        print(f"New functions:")
        for func in new_functions:
            print(f"    {func}")

        for func in new_functions:
            f.write(f"void {func}() {{\n    // TODO: Implement {func}\n}}\n\n")

    print(f"Added {len(new_functions)} new functions to actions.c.")

def main():
    parser = argparse.ArgumentParser(description="UI Import Tool")
    parser.add_argument("-d", "--directory", help="Path to the UI source directory")
    parser.add_argument("-m", "--mode", choices=["copy-ui", "fix-headers", "fix-cmake", "fix-actions", "all"], help="Specify action to perform")

    args = parser.parse_args()

    # Load configuration
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILE)
        source_dir = config.get('Settings', 'source_dir', fallback=None)
    except (configparser.Error, IOError):
        source_dir = None

    if args.directory:
        source_dir = args.directory
        if not validate_ui_source(source_dir):
            sys.exit(1)

        # Save configuration
        config['Settings'] = {'source_dir': source_dir}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    if not source_dir:
        print("No source directory specified.")
        print(f"Example usage: python ui_import.py -d /UI/SOURCE/DIRECTORY")
        sys.exit(1)

    if not validate_ui_source(source_dir):
        sys.exit(1)


    if args.mode:
        if args.mode == "copy-ui":
            copy_ui(source_dir)
        elif args.mode == "fix-headers":
            fix_headers()
        elif args.mode == "fix-cmake":
            fix_cmake()
        elif args.mode == "fix-actions":
            fix_actions()
    else:
        copy_ui(source_dir)
        fix_headers()
        fix_cmake()
        fix_actions()

if __name__ == "__main__":
    main()