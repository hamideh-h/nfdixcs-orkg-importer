from orkg import ORKG
import inspect
import requests
import json

EMAIL = "hamideh.hajiabadi@kit.edu"
PASSWORD = "Test123456?"

# 1. Connect to ORKG
orkg = ORKG(host="https://orkg.org", creds=(EMAIL, PASSWORD))

# 2. Materialize your template so the function appears
orkg.templates.materialize_template("R1563436")
tp = orkg.templates

print([n for n in dir(tp) if "nfdixcs" in n.lower()])
print("docstring:", tp.nfdixcs_versioning_schema.__doc__)  # will be None, that's fine

# 3. Fetch the raw template definition from the REST API
resp = requests.get(
    "https://orkg.org/api/templates/R1563436",
    headers={
        "Accept": "application/vnd.orkg.template.v1+json;charset=UTF-8"
    },
)
resp.raise_for_status()
tpl = resp.json()

# 4. Inspect the template JSON
print("=== BASIC INFO ===")
print("ID:   ", tpl.get("id"))
print("Label:", tpl.get("label"))
print("Target class:", tpl.get("target_class"))

print("\n=== PROPERTIES ===")
for prop in tpl.get("properties", []):
    # Depending on backend version, keys might be slightly different.
    pid = prop.get("id")
    path = prop.get("path") or {}
    pred_id = path.get("id")
    pred_label = path.get("label")

    min_count = prop.get("min_count")
    max_count = prop.get("max_count")
    datatype = prop.get("datatype")   # for literal properties
    clazz = prop.get("class")         # for resource properties
    nested_template = prop.get("template_id")

    print(f"- property {pid}: {pred_label} ({pred_id})")
    print(f"    cardinality: {min_count}..{max_count}")
    print(f"    datatype:    {datatype}")
    print(f"    class:       {clazz}")
    print(f"    nested tpl:  {nested_template}")

print("\n=== FULL JSON (if you want to inspect everything) ===")
print(json.dumps(tpl, indent=2))


# 3. Create ONE test instance of the template
import datetime

print("\n=== CREATING TEST TEMPLATE INSTANCE (DRY RUN) ===")

fn = tp.nfdixcs_versioning_schema

# Try to build an instance using the inferred keyword names.
instance = fn(
    # Resource label
    label="TEST: NFDIxCS Versioning Schema instance",

    # Required: Identifier (P37134)
    identifier="https://doi.org/10.1234/test.v1",

    # Optional: Concept Identifier (P183159)
    concept_identifier="https://doi.org/10.1234/test",

    # Optional: version (Version)
    version="v1.0.0",

    # Optional: Relations
    relations=[],  # you can also try a string later, e.g. "IsNewVersionOf: https://doi.org/..."

    # Required: Contributor Roles (P183174)
    contributor_roles="H. Hajiabadi (Data curation)",

    # Optional: provenance support
    provenance_support="See Git tag v1.0.0; internal changelog",

    # Optional: date metadata (xsd:date)
    date_metadata=datetime.date.today(),
)

print("\n=== TEMPLATE INSTANCE (INTERNAL REPRESENTATION) ===")
instance.pretty_print()



