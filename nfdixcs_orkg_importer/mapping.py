"""
Load and represent the YAML field-mapping for an ORKG template.
This tells the importer which JSON fields map to which ORKG
template parameters.
"""

from dataclasses import dataclass
from typing import Dict, Any
import yaml
from pathlib import Path


@dataclass
class TemplateMapping:
    """Represents one ORKG template mapping file."""
    template_id: str
    template_function: str
    fields: Dict[str, Any]


def load_mapping(path: str | Path) -> TemplateMapping:
    """
    Load a YAML mapping file (e.g. R1563436_mapping.yaml)
    and return a TemplateMapping instance.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Mapping file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Basic validation
    if "template_id" not in data:
        raise ValueError("Mapping file missing 'template_id'")
    if "template_function" not in data:
        raise ValueError("Mapping file missing 'template_function'")
    if "fields" not in data:
        raise ValueError("Mapping file missing 'fields' block")

    return TemplateMapping(
        template_id=data["template_id"],
        template_function=data["template_function"],
        fields=data["fields"],
    )
