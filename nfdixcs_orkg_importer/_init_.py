"""
nfdixcs_orkg_importer

Package for importing NFDIxCS versioning metadata into ORKG
using the NFDIxCS Versioning Schema template (R1563436).
"""

from .importer import NFDIxCSORKGImporter
from .mapping import TemplateMapping, load_mapping

__all__ = [
    "NFDIxCSORKGImporter",
    "TemplateMapping",
    "load_mapping",
]

__version__ = "0.1.0"
