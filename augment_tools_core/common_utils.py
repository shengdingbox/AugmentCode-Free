"""
Common utility functions for Augment Tools Core
"""
import os
import platform
import shutil
import uuid
from pathlib import Path
from typing import Dict, Union # Added Union for type hinting

try:
    from colorama import init, Fore, Style
    init(autoreset=True)  # Initialize colorama for Windows support and auto-reset styles
    IS_COLORAMA_AVAILABLE = True
except ImportError:
    IS_COLORAMA_AVAILABLE = False

# --- Console Message Functions ---
def print_message(prefix: str, message: str, color_code: str = "") -> None:
    """Helper function to print messages with optional color."""
    if IS_COLORAMA_AVAILABLE and color_code:
        print(f"{color_code}{prefix}{Style.RESET_ALL} {message}")
    else:
        print(f"{prefix} {message}")

def print_info(message: str) -> None:
    """Prints an informational message (blue if colorama is available)."""
    prefix = "[INFO]"
    color = Fore.BLUE if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

def print_success(message: str) -> None:
    """Prints a success message (green if colorama is available)."""
    prefix = "[SUCCESS]"
    color = Fore.GREEN if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

def print_warning(message: str) -> None:
    """Prints a warning message (yellow if colorama is available)."""
    prefix = "[WARNING]"
    color = Fore.YELLOW if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

def print_error(message: str) -> None:
    """Prints an error message (red if colorama is available)."""
    prefix = "[ERROR]"
    color = Fore.RED if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

# --- VS Code Path Functions ---
def get_os_specific_vscode_paths() -> Dict[str, Path]:
    """
    Determines and returns OS-specific paths for VS Code configuration files.

    Returns:
        A dictionary containing 'state_db' and 'storage_json' paths.
    Raises:
        SystemExit: If the OS is not supported or APPDATA is not found on Windows.
    """
    system = platform.system()
    paths: Dict[str, Path] = {}

    try:
        if system == "Windows":
            appdata = os.environ.get("APPDATA")
            if not appdata:
                print_error("APPDATA environment variable not found. Cannot locate VS Code data.")
                raise SystemExit(1)
            base_dir = Path(appdata) / "Code" / "User"
        elif system == "Darwin":  # macOS
            base_dir = Path.home() / "Library" / "Application Support" / "Code" / "User"
        elif system == "Linux":
            base_dir = Path.home() / ".config" / "Code" / "User"
        else:
            print_error(f"Unsupported operating system: {system}")
            raise SystemExit(1)

        paths["state_db"] = base_dir / "globalStorage" / "state.vscdb"
        paths["storage_json"] = base_dir / "globalStorage" / "storage.json"
        return paths
    except Exception as e:
        print_error(f"Failed to determine VS Code paths: {e}")
        raise SystemExit(1)

# --- File Backup Function ---
def create_backup(file_path: Union[str, Path]) -> Union[Path, None]:
    """
    Creates a backup of the given file.

    Args:
        file_path: The path to the file to be backed up.

    Returns:
        The path to the backup file if successful, None otherwise.
    """
    original_path = Path(file_path)
    if not original_path.exists():
        print_error(f"File not found for backup: {original_path}")
        return None

    backup_path = original_path.with_suffix(original_path.suffix + ".backup")
    try:
        shutil.copy2(original_path, backup_path)
        print_success(f"Backup created successfully at: {backup_path}")
        return backup_path
    except Exception as e:
        print_error(f"Failed to create backup for {original_path}: {e}")
        return None

# --- ID Generation Functions ---
def generate_new_machine_id() -> str:
    """Generates a new 64-character hexadecimal string for machineId."""
    return uuid.uuid4().hex + uuid.uuid4().hex

def generate_new_device_id() -> str:
    """Generates a new standard UUID v4 string for devDeviceId."""
    return str(uuid.uuid4())

if __name__ == '__main__':
    # Quick test for the utility functions
    print_info("Testing common_utils.py...")

    print_info("Displaying detected VS Code paths:")
    try:
        vscode_paths = get_os_specific_vscode_paths()
        print_success(f"  State DB: {vscode_paths['state_db']}")
        print_success(f"  Storage JSON: {vscode_paths['storage_json']}")
    except SystemExit:
        print_warning("Could not retrieve VS Code paths on this system (expected if run in isolated env).")


    print_info("Generating sample IDs:")
    machine_id = generate_new_machine_id()
    device_id = generate_new_device_id()
    print_success(f"  Generated Machine ID: {machine_id} (Length: {len(machine_id)})")
    print_success(f"  Generated Device ID: {device_id}")

    # To test backup, you'd need a dummy file.
    # Example:
    # test_file = Path("dummy_test_file.txt")
    # with open(test_file, "w") as f:
    #     f.write("This is a test file for backup.")
    # backup_result = create_backup(test_file)
    # if backup_result:
    #     print_info(f"Backup test successful. Backup at: {backup_result}")
    #     if backup_result.exists():
    #         backup_result.unlink() # Clean up backup
    # if test_file.exists():
    #     test_file.unlink() # Clean up test file

    print_info("Testing message types:")
    print_success("This is a success message.")
    print_warning("This is a warning message.")
    print_error("This is an error message.")
    print_info("common_utils.py tests complete.")