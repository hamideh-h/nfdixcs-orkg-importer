"""
Main importer for NFDIxCS → ORKG using template R1563436.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .mapping import TemplateMapping, load_mapping
from .orkg_client import get_orkg_client


class NFDIxCSORKGImporter:
    """
    Loads a JSON file, maps its fields to an ORKG template instance,
    saves the instance, and adds additional statements (like contributor roles).
    """

    def __init__(
        self,
        host: str | None = None,
        creds: Tuple[str, str] | None = None,
        mapping_file: str | Path | None = None,
    ) -> None:

        # Load mapping
        if mapping_file is None:
            raise ValueError("mapping_file must be provided")

        self.mapping: TemplateMapping = load_mapping(mapping_file)

        # ORKG client
        self.orkg = get_orkg_client(host=host, creds=creds)

        # Materialize template
        self.orkg.templates.materialize_template(self.mapping.template_id)
        self.tp = self.orkg.templates

        # Get template function
        self.template_fn = getattr(self.tp, self.mapping.template_function, None)
        if self.template_fn is None:
            raise RuntimeError(
                f"Template function '{self.mapping.template_function}' not found "
                f"after materializing template {self.mapping.template_id}"
            )

    # -----------------------------------------------------------
    # INTERNAL helper: build kwargs for template function
    # -----------------------------------------------------------

    def _build_kwargs(self, record: Dict[str, Any]) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {}

        for json_key, tpl_param in self.mapping.fields.items():
            if json_key not in record:
                continue

            # Must not include contributor_roles in kwargs (template ignores it)
            if tpl_param == "contributor_roles":
                continue

            value = record[json_key]
            kwargs[tpl_param] = value

        return kwargs

    # -----------------------------------------------------------
    # INTERNAL helper: add contributor roles via statements
    # -----------------------------------------------------------

    def _add_contributor_roles(self, main_id: str, contributors: Any) -> None:
        """
        contributors may be:
        - a string
        - a list of strings
        - a list of objects with fields: name, role, orcid, affiliation
        """

        if not contributors:
            return

        if isinstance(contributors, str):
            contributors = [contributors]

        # P183174 = Contributor Roles
        predicate = "P183174"

        for entry in contributors:

            # Simple case: a string
            if isinstance(entry, str):
                label = entry

            # Object case
            elif isinstance(entry, dict):
                parts = []
                if "name" in entry:
                    parts.append(entry["name"])
                if "role" in entry:
                    parts.append(f"({entry['role']})")
                if "orcid" in entry:
                    parts.append(f"[ORCID: {entry['orcid']}]")
                if "affiliation" in entry:
                    parts.append(f"[{entry['affiliation']}]")
                label = " ".join(parts).strip()

            else:
                continue

            # Create resource of class C123120 (Contributor Roles)
            contrib_res = self.orkg.resources.create(
                label=label,
                classes=["C123120"],
            )
            contrib_id = contrib_res["id"]

            # Create statement linking main resource → contributor
            self.orkg.statements.create(
                subject=main_id,
                predicate=predicate,
                object=contrib_id,
            )

    # -----------------------------------------------------------
    # PUBLIC: Import one record
    # -----------------------------------------------------------

    def import_one(self, record: Dict[str, Any]) -> str:
        """
        Import a single JSON record and return the ORKG resource ID.
        """

        kwargs = self._build_kwargs(record)

        # Create template instance
        instance = self.template_fn(**kwargs)

        # Save it to ORKG
        res = instance.save()
        main_id = res["id"]

        # Now manually add contributor roles
        if "contributor_roles" in record:
            self._add_contributor_roles(main_id, record["contributor_roles"])

        return main_id

    # -----------------------------------------------------------
    # PUBLIC: Import from file with multiple records
    # -----------------------------------------------------------

    def import_file(self, json_path: str | Path) -> List[str]:
        """
        Import a JSON file structured as:
        {
            "records": [ { ... }, { ... }, ... ]
        }
        """

        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        records = data.get("records", [])

        if not isinstance(records, list):
            raise ValueError("Input JSON must contain a list under 'records'.")

        created_ids: List[str] = []

        for record in records:
            main_id = self.import_one(record)
            created_ids.append(main_id)

        return created_ids
