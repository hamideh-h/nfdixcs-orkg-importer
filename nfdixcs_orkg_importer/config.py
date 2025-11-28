"""
Configuration utilities for nfdixcs-orkg-importer.
Handles ORKG host selection, credentials, and mapping file paths.
"""

import os
from pathlib import Path


# -----------------------------
# ORKG SERVER CONFIGURATION
# -----------------------------

# Default ORKG host (production)
ORKG_HOST = os.getenv("ORKG_HOST", "https://orkg.org")

# ORKG credentials are expected as environment variables
ORKG_USER = os.getenv("ORKG_USER")
ORKG_PASSWORD = os.getenv("ORKG_PASSWORD")


# -----------------------------
# MAPPING FILES
# -----------------------------

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder containing YAML mappings
MAPPINGS_DIR = BASE_DIR / "config"

# Default mapping for template R1563436
DEFAULT_MAPPING_FILE = MAPPINGS_DIR / "R1563436_mapping.yaml"


# -----------------------------
# INPUT / OUTPUT DIRECTORY DEFAULTS
# -----------------------------

# Where JSON input files are expected to be located
INPUT_DIR = BASE_DIR / "input"

# Where logs or debug output can be written
OUTPUT_DIR = BASE_DIR / "output"


# -----------------------------
# Utility functions
# -----------------------------

def require_credentials():
    """Ensure ORKG_USER and ORKG_PASSWORD are provided."""
    if not ORKG_USER or not ORKG_PASSWORD:
        raise RuntimeError(
            "Missing ORKG credentials. "
            "Please set ORKG_USER and ORKG_PASSWORD environment variables."
        )
