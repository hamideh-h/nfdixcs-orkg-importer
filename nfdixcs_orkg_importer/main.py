# python
import sys
import argparse
from pathlib import Path

from nfdixcs_orkg_importer.importer import NFDIxCSORKGImporter
from nfdixcs_orkg_importer.config import DEFAULT_MAPPING_FILE


def main():
    parser = argparse.ArgumentParser(description="Import JSON records into ORKG using the NFDIxCS importer.")
    parser.add_argument("json_file", help="Path to the JSON file to import")
    parser.add_argument(
        "--mapping",
        help="Path to the mapping file (overrides default)",
        default=str(DEFAULT_MAPPING_FILE),
    )
    args = parser.parse_args()

    json_path = Path(args.json_file)
    if not json_path.exists() or not json_path.is_file():
        print(f"Error: JSON file not found: {json_path}")
        sys.exit(1)

    mapping_path = Path(args.mapping)
    if not mapping_path.exists():
        print(f"Warning: mapping file not found: {mapping_path}. Continuing with provided value.")

    importer = NFDIxCSORKGImporter(mapping_file=str(mapping_path))

    print(f"Importing records from: {json_path}")

    try:
        created_ids = importer.import_file(str(json_path))
        if created_ids is None:
            created_ids = []
    except Exception as e:
        print(f"Import failed: {e}")
        sys.exit(1)

    if created_ids:
        print("\nSuccessfully created ORKG resources:")
        for rid in created_ids:
            print(f" - {rid}")
    else:
        print("\nNo resources created.")

    print("\nDone.")


if __name__ == "__main__":
    main()
