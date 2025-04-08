import os
import shutil
import re
import argparse
import configparser
import sys

# Default source directory
DEFAULT_SOURCE_DIR = "./example/eez-project/project_name/src/ui"
DEFAULT_PROJECT_DIR = "./components/ui"
DEFAULT_BACKUP_DIR = "./backup/ui"
DEFAULT_USER_SELECTED_MODES = "all"

# CMakeLists.txt file path
cmake_file = "./components/ui/CMakeLists.txt"

# Configuration file path
CONFIG_FILE = ".ui_import_config"

def load_config():
    """
    Loads the configuration from the config file. If the file does not exist,
    creates a default configuration.

    Returns:
        configparser.ConfigParser: The loaded configuration object.
    """
    config = configparser.ConfigParser()
    # Check if the config file exists
    if os.path.exists(CONFIG_FILE):
        print(f"\nLoading configuration from {CONFIG_FILE}")
        config.read(CONFIG_FILE)
    # If the config file does not exist, create a default configuration
    else:
        print(f"\nNo configuration file found at {CONFIG_FILE}")
        print("\nWould you like to create a default configuration? This will set the defaults:\n\nSource directory set to ./example/eez-project/project_name/src/ui\nBackup directory set to ./backup/ui\nDestination directory set to ./components/ui.\nUser selected modes set to 'all'\n")
        user_input = input("Enter 'y' to create a default configuration, or 'n' to exit: ")
        # If the user input is 'y', create a default configuration
        if user_input.lower() == 'y':
            # Create a default configuration
            config['ImportSettings'] = {
                'source_dir': DEFAULT_SOURCE_DIR,
                'destination_dir': DEFAULT_BACKUP_DIR,
                'project_dir': DEFAULT_PROJECT_DIR,
                'user_selected_modes': DEFAULT_USER_SELECTED_MODES,
            }
            save_config(config)
        # If the user input is 'n', exit
        else:
            print("Exiting")
            sys.exit(0)
    # Return the loaded configuration
    return config


def save_config(config):
    """
    Saves the configuration to the file defined by CONFIG_FILE.
    If config is None, prints an error message and does not save the configuration.
    
    Args:
    config (configparser.ConfigParser): The configuration to be saved.
    """
    # If config is None, print an error message and exit without saving
    if config is None:
        print("\nERROR: save_config(config): config is null. Cannot save null configuration. Please run -m config first.")
        sys.exit(1)
    # If config is not None, save the configuration
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)
    print(f"\nConfiguration saved to {CONFIG_FILE}")
    

def update_config(config, source_dir=None, destination_dir=None, user_selected_modes=None):
    """
    Updates the configuration file with the provided values.

    This function is used to update the configuration after it has been loaded.
    It takes the loaded configuration object and updates it with the provided values.

    Args:
        config: The loaded configuration object.
        source_dir: New source directory to update (if provided).
        destination_dir: New destination directory to update (if provided).
        user_selected_modes: New modes to update (if provided).
    """
    if 'ImportSettings' not in config:
        config['ImportSettings'] = {}

    if source_dir is not None:
        # Update the source directory in the configuration
        config['ImportSettings']['source_dir'] = source_dir

    if destination_dir is not None:
        # Update the destination directory in the configuration
        config['ImportSettings']['destination_dir'] = destination_dir

    if user_selected_modes is not None:
        # Update the user selected modes in the configuration
        config['ImportSettings']['user_selected_modes'] = user_selected_modes

    # Save the updated configuration
    save_config(config)


def validate_ui_source(source_dir):
    """
    Validates the UI source directory.

    This function checks if the source directory exists and contains a ui.h file.
    If the directory does not exist, it prints an error message and returns False.
    If the directory does not contain a ui.h file, it prints a warning and returns True.

    Args:
        source_dir: Path to the UI source directory.

    Returns:
        True if valid, False otherwise.
    """
    # Check if the source directory exists
    if not os.path.isdir(source_dir):
        print(f"Error: '{source_dir}' is not a directory.")
        return False

    # Check if the source directory contains a ui.h file
    if not os.path.isfile(os.path.join(source_dir, "ui.h")):
        print(f"\nWARNING: '{source_dir}' does not contain a 'ui.h' file.")
        print(f"            You can safely ignore this warning if this you havent performed a backup yet.\n")
        return True

    # Validation Passed
    return True

def config_mode(config):
    """
    Interactively configures the script's settings. Allows the user to:
    - Set the source directory for UI files
    - Set the backup directory
    - Configure user-selected modes for default execution

    Args: 
        config: A configparser object containing the script's configuration
    """
    # Set source directory
    print("\nConfiguration Mode: Set up your UI Import settings.\n")
    print("Current source directory:", config.get('ImportSettings', 'source_dir', fallback=DEFAULT_SOURCE_DIR))
    source_dir = input("Enter the source directory for UI files (press Enter to keep current): ").strip()
    # Validate source directory
    if source_dir:
        if not validate_ui_source(source_dir):
            print(f"Invalid source directory: {source_dir}. Please try again.")
            return
        config['ImportSettings']['source_dir'] = source_dir

    # Set backup directory
    print("\nCurrent backup directory:", config.get('ImportSettings', 'destination_dir', fallback=DEFAULT_BACKUP_DIR))
    backup_dir = input("Enter the backup directory (press Enter to keep current): ").strip()
    if backup_dir:
        if not os.path.isdir(backup_dir):
            print(f"Backup directory '{backup_dir}' does not exist. Creating it...")
            os.makedirs(backup_dir, exist_ok=True)
        config['ImportSettings']['destination_dir'] = backup_dir

    # Select user-selected modes
    available_modes = ['config', 'backup-ui', 'restore-ui', 'delete-backup', 'copy-ui', 'fix-headers', 'fix-cmake', 'fix-actions', 'fix-flow']
    print("\nAvailable modes:")
    # Print available modes
    for i, mode in enumerate(available_modes, 1):
        print(f"{i}. {mode}")
    # Print all modes as it is handled seperately
    print("0. All modes (Default)(Runs backup-ui, restore-ui, copy-ui, fix-headers, fix-cmake, fix-actions)")
    print(f"\nCurrent modes: {config.get('ImportSettings', 'user_selected_modes', fallback='all')}")
    selected_modes = input("Enter the mode numbers to select (e.g., 1,3 for copy-ui and fix-cmake): ").strip()
    #Handle 0 seperately so that it can be ordered correctly
    if selected_modes == "0":
        user_selected_modes = ['all']
        config['ImportSettings']['user_selected_modes'] = ",".join(user_selected_modes)
    # Do nothing if user input is empty
    elif selected_modes == "":
        print(f"\nUsing existing modes: {config.get('ImportSettings', 'user_selected_modes', fallback='all')}")
    # Handle the rest of user modes
    else:
        selected_modes = selected_modes.split(",")
        user_selected_modes = [
            available_modes[int(i) - 1]
            for i in selected_modes if i.isdigit() and 0 < int(i) <= len(available_modes)
        ]
        config['ImportSettings']['user_selected_modes'] = ",".join(user_selected_modes)
    # Save configuration
    save_config(config)


def backup_ui(source_dir, destination_dir):
    """
    Copies UI files from the source directory to the backup directory.

    Args:
        source_dir (str): Path to the UI source directory.
        destination_dir (str): Path to the backup directory.
    """
    # Print a message to indicate that the backup process is starting
    print(f"\nBacking up UI files from '{source_dir}' to '{destination_dir}'.")

    # Create the backup directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Initialize a counter to keep track of the number of files copied
    copied_files_count = 0

    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(source_dir):
        # Iterate over the files in the current directory
        for file in files:
            # Construct the full path of the source file
            src_file = os.path.join(root, file)
            # Construct the full path of the destination file
            dest_file = os.path.join(destination_dir, os.path.relpath(src_file, source_dir))
            # Copy the source file to the destination file
            shutil.copy2(src_file, dest_file)
            # Increment the counter
            copied_files_count += 1

    # Print a message to indicate how many files were copied
    print(f"Total files copied: {copied_files_count}")

def restore_ui(source_dir, destination_dir):
    """
    This function restores the UI files from the backup directory
    to the source directory. If the backup directory does not exist,
    it will not restore anything.

    Args:
        source_dir: Path to the current UI source directory.
        destination_dir: Path to the backup directory.
    """
    print(f"\nRestoring UI files from '{destination_dir}' to '{source_dir}'.")
    restored_files_count = 0
    # Check if the backup directory exists
    if os.path.exists(destination_dir):
        # Copy UI files from backup directory to source directory
        for root, dirs, files in os.walk(destination_dir):
            for file in files:
                # Construct the full path of the source file in the backup directory
                src_file = os.path.join(root, file)
                # Construct the full path of the destination file in the source directory
                dest_file = os.path.join(source_dir, os.path.relpath(src_file, destination_dir))
                # Copy the source file to the destination file
                shutil.copy2(src_file, dest_file)
                # Increment the counter
                restored_files_count += 1
        # Print a message to indicate how many files were restored
        print(f"Total files restored: {restored_files_count}")
    # If the backup directory does not exist
    else:
        print(f"Backup directory '{destination_dir}' does not exist.")
        

def copy_ui(source_dir):
    """
    Copies UI files from the source directory to the destination directory.

    Args:
        source_dir: Path to the UI source directory.
    """
    print(f"\nCopying UI files from '{source_dir}' to 'components/ui'.")
    dest_dir = "components/ui"
    
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    copied_files = 0  # Counter for the number of copied files
    
    # Walk through the source directory to copy files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            src_file = os.path.join(root, file)  # Get the full path of the source file
            dest_file = os.path.join(dest_dir, os.path.relpath(src_file, source_dir))  # Determine destination path
            shutil.copy2(src_file, dest_file)  # Copy the file to the destination
            copied_files += 1  # Increment the copied files counter
    
    print(f"Copied {copied_files} files.")  # Output the number of copied files


def fix_flow():
    """
    Copies the eez-flow.h template from the backup directory to the destination directory if it doesn't already exist.
    This is necessary to ensure that the project compiles.
    """
    # Check if the file already exists in the destination directory
    if not os.path.exists(os.path.join(DEFAULT_PROJECT_DIR, "eez-flow.h")):
        # If the file doesn't exist, copy it from the backup directory
        print(f"\nCopying eez-flow.h template from backup to {DEFAULT_PROJECT_DIR}.")
        shutil.copy2(os.path.join("backup/templates/eez-flow.h"), os.path.join(DEFAULT_PROJECT_DIR, "eez-flow.h"))
        
        
def fix_headers():
    """
    Replaces "lvgl/lvgl.h" with "lvgl.h" in all UI files.

    This is necessary because the UI files from the template project
    include the header file with "lvgl/lvgl.h", which is not valid if
    the lvgl component is used in a project.
    """
    count = 0
    print("\nReplacing occurrences of 'lvgl/lvgl.h' with 'lvgl.h' in all UI files.")
    # Replace "lvgl/lvgl.h" with "lvgl.h"
    for root, dirs, files in os.walk("components/ui"):
        # Only process .h, .c, .cpp, and .hpp files
        for file in files:
            if file.endswith(".h") or file.endswith(".c") or file.endswith(".cpp") or file.endswith(".hpp"):
                file_path = os.path.join(root, file)
                # Read file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Replaces all occurrences
                updated_content = content.replace("lvgl/lvgl.h", "lvgl.h")
                # Check if changes were made
                if content != updated_content:
                    # Write updated content
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    print(f"Updated '{file_path}'")
                    count += 1
    print(f"Total files updated: {count}")

def fix_cmake():
    """
    Verifies the existence of CMakeLists.txt and replaces it with a default if missing.

    This function checks if the CMakeLists.txt file exists in the specified directory.
    If the file is absent, it copies a default version from the backup directory to ensure
    that the project can be successfully built. This step is necessary as the CMakeLists.txt
    file is not generated automatically during project creation.
    """
    # Check if CMakeLists.txt exists at the specified path
    if os.path.exists(cmake_file):
        # Print a message indicating the file exists and will be used
        print(f"\nCMakeLists.txt found.\nUsing existing {cmake_file}")
    else:
        # Print a message indicating the file is missing and will be replaced
        print(f"\n{cmake_file} missing. Replacing it with the default")
        # Copy the default CMakeLists.txt from the backup directory to the specified path
        shutil.copy2("./backup/templates/CMakeLists.txt", cmake_file)

def fix_actions():
    """
    This function searches for extern functions in actions.h and if the function is not
    implemented in actions.c, it adds the function to actions.c with a TODO comment to
    implement the function.
    """

    actions_h = "components/ui/actions.h"
    actions_c = "components/ui/actions.c"
    actions_template = "./backup/templates/actions.c"
    
    if os.path.exists(actions_h):
        with open(actions_h, "r") as f:
            content = f.read()
            # Find all extern functions in actions.h
            extern_functions = re.findall(r"extern\s+void\s+(\w+)\s*\(.*?\);", content)
        
        # Check if actions.c exists
        if os.path.exists(actions_c):
            print(f"\n{actions_c} found. Using existing actions.c.")
            with open(actions_c, "r") as f:
                content = f.read()
                # Find all existing functions in actions.c
                existing_functions = re.findall(r"void\s+(\w+)\s*\(.*?\)", content)
        else: 
            print(f"\n{actions_c} not found. Creating new actions.c")
            # If actions.c does not exist, copy the template from the backup directory
            if os.path.exists(actions_template):
                shutil.copy2(actions_template, actions_c)
            else:
                print(f"\n{actions_template} not found. Skipping template copy.")
        
        print(f"Found {len(extern_functions)} extern functions in {actions_h}")    
        # Write extern functions to actions.c
        with open(actions_c, "a") as f:
            print(f"Writing extern functions to {actions_c}")
            for func in extern_functions:
                print(f"Found extern function: {func}")
                # Check if the function is not implemented in actions.c
                if func not in existing_functions:
                    print(f"Function {func} not found in {actions_c}.")
                    print(f"Adding extern function: {func}")
                    f.write(f"\nvoid {func}() {{\n\t// TODO: implement {func}\n}}\n")
                else:
                    print(f"Function {func} found in {actions_c} already. Skipping.")
    else:
        print(f"{actions_h} not found. Skipping.")

def main():
    """
    Main function to run the script with the given arguments.
    """
    parser = argparse.ArgumentParser(description='Running EEZ UI Importer')
    parser.add_argument('-d', '--directory',nargs='?', const='', help='Source directory for UI files')
    parser.add_argument('-b', '--backup-directory',nargs='?', const='', help='Backup directory for UI files')
    parser.add_argument('-m', '--mode', choices=['config', 'backup-ui', 'restore-ui', 'delete-backup', 'copy-ui', 'fix-headers', 'fix-cmake', 'fix-actions', 'all'], default=None) 
    help_parser = argparse.ArgumentParser(description='Import EEZ UI', formatter_class=argparse.RawDescriptionHelpFormatter, epilog='''
                                     
  -d, --directory         -Set the source directory for UI files exported from EEZ-Studio. Must be in folder called ui
                            Default: ./example/eez-project/project_name/src/ui
                            Example: python import_eez_ui.py -d ./example/eez-project/project_name/src/ui
    
  -b, --backup-directory  -Set the backup directory for .components/ui files. 
                            Default: ./backup/ui
                            Example: python import_eez_ui.py -b ./backup/ui
    
  -m, --mode:             -Run a specific mode.
                            Default: ALL Modes unless set by config, then user selected modes.
                            Example: python import_eez_ui.py -m <mode_choice>
    
        Optional Modes:
              
        config         -Run Interactive Config
        backup-ui      -Copy UI files from ./components/ui to backup directory
        restore-ui     -Copy UI files from backup directory to ./components/ui
        delete-backup  -Delete backup directory
        copy-ui        -Copy UI files from source directory to ./components/ui
        fix-headers    -Fix header files - if ui files from EEZ-Studio still link to lvgl/lvgl.h this will 
                        replace it with the correct lvgl.h.
        fix-cmake      -Fix CMakeLists.txt - if you accidently delete CMakeLists.txt, this will replace it 
                        with a default
        fix-actions    -Fix actions.c - if custom actions are defined in EEZ-Studio this will create stubs for 
                        you to implement
        fix-flow       -Fix for eez-flow - if ui.h from EEZ-Studio still links to eez-flow.c even if not used 
                        this will add in the correct eez-flow.h
        all            -Run all modes(Except delete-backup) with settings from config file
                        ''')
    args = parser.parse_args()

    # Load config file
    config = load_config()
    # Set script variables from config variables
    source_dir = config.get('ImportSettings', 'source_dir', fallback=DEFAULT_SOURCE_DIR)
    backup_dir = config.get('ImportSettings', 'backup_dir', fallback=DEFAULT_BACKUP_DIR)
    user_selected_modes = config.get('ImportSettings', 'user_selected_modes', fallback=DEFAULT_USER_SELECTED_MODES).split(',')
    
     # Handle -d (directory) flag
    if args.directory is not None:
        if args.directory == "":
            # If -d is passed without a value, display the current source directory
            print(f"Current source directory: {source_dir}")
        else:
            # If -d is passed with a value, validate and update the source directory
            new_source_dir = args.directory
            if validate_ui_source(new_source_dir):
                update_config(config, source_dir=new_source_dir)
                print(f"Source directory updated to: {new_source_dir}")
            else:
                print(f"Invalid source directory: {new_source_dir}")
        sys.exit(0) # End script with success

    # Handle -b (backup-directory) flag
    if args.backup_directory is not None:
        if args.backup_directory == "":
            # If -b is passed without a value, display the current backup directory
            print(f"Current backup directory: {backup_dir}")
        else:
            # If -b is passed with a value, validate and update the backup directory
            new_backup_dir = args.backup_directory
            if validate_ui_source(new_backup_dir):
                update_config(config, destination_dir=new_backup_dir)
                print(f"Backup directory updated to: {new_backup_dir}")
            else:
                print(f"Invalid backup directory: {new_backup_dir}")
        sys.exit(0) # End script with success
    
    # Handle config mode and exit before other operations
    if args.mode == 'config':
        config_mode(config)
        sys.exit(0) # End script with success

    # Handle default or mode-specific operations
    if args.mode is None and not args.backup_directory and not args.directory:
        # If user_selected_mode is set to 'all' from config (default before config)
        if 'all' in user_selected_modes:
            backup_ui(source_dir, backup_dir)
            copy_ui(source_dir)
            fix_headers()
            fix_cmake()
            fix_actions()
            fix_flow()
            print("\nAll operations completed successfully.\nFull Clean and Build the project to verify.\n")
            sys.exit(0)
        # If user_selected_mode is to any other value, run each mode that is specified.
        else:
            # Run each selected mode that is listed in user_selected_modes
            for mode in user_selected_modes:
                if mode == 'config':
                    config_mode(config)
                elif mode == 'backup-ui':
                    backup_ui(DEFAULT_PROJECT_DIR, backup_dir)
                elif mode == 'restore-ui':
                    restore_ui(DEFAULT_PROJECT_DIR, backup_dir)
                elif mode == 'delete-backup':
                    # Delete backup directory
                    shutil.rmtree(backup_dir, ignore_errors=True)
                    print(f"\nDeleted backup directory: {backup_dir}")
                elif mode == 'copy-ui':
                    copy_ui(source_dir)
                elif mode == 'fix-headers':
                    fix_headers()
                elif mode == 'fix-cmake':
                    fix_cmake()
                elif mode == 'fix-actions':
                    fix_actions()
                elif mode == 'fix-flow':
                    fix_flow()
            print("\nSelected operations completed successfully.\nFull Clean and Build the project to verify.\n")
        sys.exit(0)
    # Run only the selected mode when -m is passed
    else:
        if args.mode == 'backup-ui':
            backup_ui(DEFAULT_PROJECT_DIR, backup_dir)
        elif args.mode == 'restore-ui':
            restore_ui(DEFAULT_PROJECT_DIR, backup_dir)
        elif args.mode == 'delete-backup':
            shutil.rmtree(backup_dir, ignore_errors=True)
            print(f"\nDeleted backup directory: {backup_dir}")
        elif args.mode == 'copy-ui':
            copy_ui(source_dir)
        elif args.mode == 'fix-headers':
            fix_headers()
        elif args.mode == 'fix-cmake':
            fix_cmake()
        elif args.mode == 'fix-actions':
            fix_actions()
        elif args.mode == 'fix-flow':
            fix_flow()
        elif args.mode == 'all':
            backup_ui(source_dir, backup_dir)
            copy_ui(source_dir)
            fix_headers()
            fix_cmake()
            fix_actions()
            print("\n{args.mode} completed successfully.\nFull Clean and Build the project to verify.\n")
    sys.exit(0) # End script with success
            

if __name__ == "__main__":
    main()