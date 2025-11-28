import sys
from pathlib import Path

from nfdixcs_orkg_importer.importer import NFDIxCSORKGImporter
from nfdixcs_orkg_importer.config import DEFAULT_MAPPING_FILE


def main():
    # -----------------------------------------
    # 1. Check CLI arguments
    # -----------------------------------------
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_json_file>")
        sys.exit(1)

    json_path = Path(sys.argv[1])

    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        sys.exit(1)

    # -----------------------------------------
    # 2. Create importer
    # -----------------------------------------
    importer = NFDIxCSORKGImporter(
        mapping_file=DEFAULT_MAPPING_FILE
    )

    # -----------------------------------------
    # 3. Import the JSON records
    # -----------------------------------------
    print(f"Importing records from: {json_path}")

    try:
        created_ids = importer.import_file(json_path)
    except Exception as e:
        print(f"Import failed: {e}")
        sys.exit(1)

    # -----------------------------------------
    # 4. Report results
    # -----------------------------------------
    print("\nSuccessfully created ORKG resources:")
    for rid in created_ids:
        print(f" - {rid}")

    print("\nDone.")


if __name__ == "__main__":
    main()
