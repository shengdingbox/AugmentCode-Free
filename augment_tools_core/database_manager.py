import sqlite3
import shutil
from pathlib import Path
import logging
from .common_utils import print_info, print_success, print_warning, print_error, create_backup

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_vscode_database(db_path: Path, keyword: str = "augment") -> bool:
    """
    Cleans the VS Code SQLite database by removing entries containing a specific keyword.

    Args:
        db_path: Path to the VS Code state.vscdb SQLite database.
        keyword: The keyword to search for in the 'key' column of 'ItemTable'.
                 Entries containing this keyword will be removed.

    Returns:
        True if the database was cleaned successfully or if no cleaning was needed,
        False otherwise.
    """
    if not db_path.exists():
        print_error(f"Database file not found: {db_path}")
        return False

    print_info(f"Attempting to clean VS Code database: {db_path}")
    print_info(f"Target keyword for cleaning: '{keyword}'")

    backup_path = None
    try:
        # 1. Create a backup
        print_info("Backing up database...")
        backup_path = create_backup(db_path)
        if not backup_path:
            # Error message already printed by create_backup
            return False
        print_success(f"Database backed up successfully to: {backup_path}")

        # 2. Connect to the SQLite database
        print_info(f"Connecting to database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print_success("Successfully connected to the database.")

        # 3. Find and count entries to be deleted
        query_select = f"SELECT key FROM ItemTable WHERE key LIKE ?"
        like_pattern = f"%{keyword}%"
        
        print_info(f"Searching for entries with keyword '{keyword}'...")
        cursor.execute(query_select, (like_pattern,))
        entries_to_delete = cursor.fetchall()
        
        num_entries_to_delete = len(entries_to_delete)

        if num_entries_to_delete == 0:
            print_success(f"No entries found with keyword '{keyword}'. Database is already clean.")
            conn.close()
            return True

        print_warning(f"Found {num_entries_to_delete} entries containing '{keyword}':")
        for i, entry in enumerate(entries_to_delete):
            print_info(f"  {i+1}. {entry[0]}")

        # Confirm before deletion (optional, but good for safety)
        # confirm = input(f"Proceed with deleting these {num_entries_to_delete} entries? (yes/no): ").strip().lower()
        # if confirm != 'yes':
        #     print_info("Deletion cancelled by user.")
        #     conn.close()
        #     return True # Or False, depending on desired behavior for cancellation

        # 4. Delete the entries
        print_info(f"Deleting {num_entries_to_delete} entries...")
        query_delete = f"DELETE FROM ItemTable WHERE key LIKE ?"
        cursor.execute(query_delete, (like_pattern,))
        conn.commit()
        
        deleted_rows = cursor.rowcount
        if deleted_rows == num_entries_to_delete:
            print_success(f"Successfully deleted {deleted_rows} entries containing '{keyword}'.")
        else:
            # This case should ideally not happen if the select and delete use the same criteria
            # and there are no concurrent modifications.
            print_warning(f"Attempted to delete {num_entries_to_delete} entries, but {deleted_rows} were reported deleted by the database.")
            # We can still consider it a partial success if some rows were deleted.
            if deleted_rows > 0:
                 print_success(f"Partial success: {deleted_rows} entries deleted.")
            else:
                 print_error("No entries were deleted despite being found. Check database permissions or logs.")
                 # Attempt to restore backup if no rows were deleted despite being found
                 raise sqlite3.Error("Mismatch in expected deletions and actual deletions, and no rows were deleted.")


        # 5. Close the connection
        conn.close()
        print_success("Database cleaning process completed.")
        return True

    except sqlite3.Error as e:
        print_error(f"SQLite error occurred: {e}")
        if backup_path and backup_path.exists():
            print_warning(f"Attempting to restore database from backup: {backup_path}")
            try:
                shutil.copy2(backup_path, db_path)
                print_success("Database successfully restored from backup.")
            except Exception as restore_e:
                print_error(f"Failed to restore database from backup: {restore_e}")
                print_error(f"The original database {db_path} might be corrupted or in an inconsistent state.")
                print_error(f"The backup is available at: {backup_path}")
        return False
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        # Similar backup restoration logic could be added here if deemed necessary
        # For now, focusing on SQLite errors for restoration.
        return False

if __name__ == '__main__':
    # This is for direct testing of this module, not part of the CLI.
    print_info("Running database_manager.py directly for testing.")
    
    # --- IMPORTANT ---
    # For testing, you MUST provide a valid path to a VS Code state.vscdb file.
    # It's highly recommended to use a COPY of your actual state.vscdb for testing
    # to avoid accidental data loss in your VS Code setup.
    #
    # Example:
    # test_db_path = Path.home() / "AppData" / "Roaming" / "Code" / "User" / "globalStorage" / "state.vscdb" # Windows
    # test_db_path = Path.home() / ".config" / "Code" / "User" / "globalStorage" / "state.vscdb" # Linux
    # test_db_path = Path.home() / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "state.vscdb" # macOS

    # Create a dummy database for testing if you don't want to use a real one
    dummy_db_path = Path("./test_state.vscdb")
    
    # Create a copy for testing to avoid modifying the original dummy
    test_dummy_db_path = Path("./test_state_copy.vscdb")

    if dummy_db_path.exists():
        dummy_db_path.unlink() # Delete if exists from previous run

    conn_test = sqlite3.connect(dummy_db_path)
    cursor_test = conn_test.cursor()
    cursor_test.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value BLOB)")
    test_data = [
        ("storage.testKey1", b"testValue1"),
        ("augment.testKey2", b"testValue2"),
        ("another.augment.key", b"testValue3"),
        ("noKeywordHere", b"testValue4"),
        ("prefix.augment", b"testValue5"),
    ]
    cursor_test.executemany("INSERT OR IGNORE INTO ItemTable VALUES (?, ?)", test_data)
    conn_test.commit()
    conn_test.close()
    print_success(f"Created dummy database at {dummy_db_path} with test data.")

    # Make a copy to test on
    shutil.copy2(dummy_db_path, test_dummy_db_path)
    print_info(f"Copied dummy database to {test_dummy_db_path} for cleaning test.")

    print_info("\n--- Test Case 1: Cleaning with default keyword 'augment' ---")
    if clean_vscode_database(test_dummy_db_path, keyword="augment"):
        print_success("Test Case 1: Cleaning successful.")
    else:
        print_error("Test Case 1: Cleaning failed.")

    # Verify content after cleaning
    conn_verify = sqlite3.connect(test_dummy_db_path)
    cursor_verify = conn_verify.cursor()
    cursor_verify.execute("SELECT key FROM ItemTable")
    remaining_keys = [row[0] for row in cursor_verify.fetchall()]
    print_info(f"Remaining keys in {test_dummy_db_path}: {remaining_keys}")
    expected_keys = ["storage.testKey1", "noKeywordHere"]
    assert all(k in remaining_keys for k in expected_keys) and len(remaining_keys) == len(expected_keys), \
        f"Test Case 1 Verification Failed! Expected {expected_keys}, got {remaining_keys}"
    print_success("Test Case 1: Verification successful.")
    conn_verify.close()


    print_info("\n--- Test Case 2: Cleaning with a keyword that finds nothing ('nonexistent') ---")
    # Re-copy the original dummy db for a fresh test
    shutil.copy2(dummy_db_path, test_dummy_db_path)
    if clean_vscode_database(test_dummy_db_path, keyword="nonexistent"):
        print_success("Test Case 2: Cleaning reported success (as expected, no items to clean).")
    else:
        print_error("Test Case 2: Cleaning failed.")
    
    conn_verify_2 = sqlite3.connect(test_dummy_db_path)
    cursor_verify_2 = conn_verify_2.cursor()
    cursor_verify_2.execute("SELECT COUNT(*) FROM ItemTable")
    count_after_no_keyword = cursor_verify_2.fetchone()[0]
    assert count_after_no_keyword == len(test_data), \
        f"Test Case 2 Verification Failed! Expected {len(test_data)} items, got {count_after_no_keyword}"
    print_success("Test Case 2: Verification successful (no items were deleted).")
    conn_verify_2.close()

    print_info("\n--- Test Case 3: Database file does not exist ---")
    non_existent_db_path = Path("./non_existent_db.vscdb")
    if non_existent_db_path.exists():
        non_existent_db_path.unlink() # Ensure it doesn't exist
        
    if not clean_vscode_database(non_existent_db_path):
        print_success("Test Case 3: Handled non-existent database file correctly (returned False).")
    else:
        print_error("Test Case 3: Failed to handle non-existent database file.")

    # Clean up dummy files
    if dummy_db_path.exists():
        dummy_db_path.unlink()
    if test_dummy_db_path.exists():
        test_dummy_db_path.unlink()
    print_info("\nCleaned up dummy database files.")
    print_success("All database_manager tests completed.")
