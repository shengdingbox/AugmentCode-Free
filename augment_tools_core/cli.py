import click
from pathlib import Path

# Assuming other modules are in the same package (augment_tools_core)
from .common_utils import (
    get_os_specific_vscode_paths,
    print_info,
    print_success,
    print_error,
    print_warning
)
from .database_manager import clean_vscode_database
from .telemetry_manager import modify_vscode_telemetry_ids

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def main_cli():
    """
    AugmentCode-Free: VS Code Maintenance Tools.
    Provides utilities for cleaning VS Code databases and modifying telemetry IDs.
    """
    # Initial greeting or setup can go here if needed,
    # but typically click groups don't print on their own.
    # print_info("AugmentCode-Free Tools Initialized.") # Removed for cleaner CLI output
    pass

@main_cli.command("clean-db")
@click.option('--keyword', default='augment', show_default=True, help='Keyword to search for and remove from the database (case-insensitive).')
def clean_db_command(keyword: str):
    """Cleans the VS Code state database (state.vscdb) by removing entries matching the keyword."""
    print_info(f"Executing: Database Cleaning (keyword: '{keyword}')")
    paths = get_os_specific_vscode_paths()
    if not paths:
        print_error("Could not determine VS Code paths for your OS. Aborting.")
        return

    db_path_str = paths.get("state_db")
    if not db_path_str:
        print_error("VS Code state.vscdb path not found in OS-specific configuration. Aborting.")
        return
    
    db_path = Path(db_path_str)
    if not db_path.is_file(): # More specific check than exists()
        print_warning(f"Database file does not exist or is not a file at the expected location: {db_path}")
        print_error("Aborting database cleaning as the database file was not found.")
        return

    if clean_vscode_database(db_path, keyword):
        # Success/error messages are now primarily handled within clean_vscode_database
        print_info("Database cleaning process finished.") 
    else:
        print_error("Database cleaning process reported errors. Check previous messages.")

@main_cli.command("modify-ids")
def modify_ids_command():
    """Modifies VS Code telemetry IDs (machineId, devDeviceId) in storage.json."""
    print_info("Executing: Telemetry ID Modification")
    paths = get_os_specific_vscode_paths()
    if not paths:
        print_error("Could not determine VS Code paths for your OS. Aborting.")
        return

    storage_path_str = paths.get("storage_json")
    if not storage_path_str:
        print_error("VS Code storage.json path not found in OS-specific configuration. Aborting.")
        return

    storage_path = Path(storage_path_str)
    if not storage_path.is_file(): # More specific check
        print_warning(f"Storage file does not exist or is not a file at the expected location: {storage_path}")
        print_error("Aborting telemetry ID modification as the storage file was not found.")
        return

    if modify_vscode_telemetry_ids(storage_path):
        print_info("Telemetry ID modification process finished.")
    else:
        print_error("Telemetry ID modification process reported errors. Check previous messages.")

@main_cli.command("run-all")
@click.option('--keyword', default='augment', show_default=True, help='Keyword for database cleaning (case-insensitive).')
@click.pass_context # To call other commands
def run_all_command(ctx, keyword: str):
    """Runs all available tools: clean-db and then modify-ids."""
    print_info("Executing: Run All Tools")
    
    print_info("--- Step 1: Database Cleaning ---")
    # Using try-except to allow the second command to run even if the first fails
    try:
        ctx.invoke(clean_db_command, keyword=keyword)
    except Exception as e:
        print_error(f"An error occurred during database cleaning step: {e}")
        print_warning("Proceeding to the next step despite the error.")
    
    print_info("--- Step 2: Telemetry ID Modification ---")
    try:
        ctx.invoke(modify_ids_command)
    except Exception as e:
        print_error(f"An error occurred during telemetry ID modification step: {e}")

    print_success("All tools have finished their execution sequence.")

if __name__ == '__main__':
    # This makes the script runnable directly for development/testing.
    # Example: python -m augment_tools_core.cli clean-db
    # Or, if in the augment_tools_core directory: python cli.py clean-db
    # The typical way to distribute a click app is via an entry point in setup.py
    main_cli()