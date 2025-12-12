### Status: Work in Progress (Active Development)

This repository is under active development and not yet production-ready. 
The core architecture and main functionality are implemented; stability,
evaluation, and documentation are still evolving.

# nfdixcs-orkg-importer

A lightweight Python importer that converts structured **NFDIxCS Versioning metadata** into  
the **Open Research Knowledge Graph (ORKG)** using the template:

**R1563436 – NFDIxCS Versioning Schema**

This project lets you take JSON exports from your Software / research data metadata and automatically create  
proper ORKG resources that follow the exact versioning model based on NFDIxCS_versioning_schema (https://orkg.org/templates/R1563436).

---

# 1. What this project does

This importer reads JSON files describing research object versions — datasets, software, workflows —  
and writes them into ORKG as **structured, template-based metadata records**.

It ensures:

- The ORKG resource uses the correct template: `R1563436`
- Required fields (identifier, contributor roles) are present
- Optional fields (concept DOI, version string, relations, provenance, dates) are mapped correctly
- Contributor roles are created and linked properly (via P183174), 

In other words:  
**You feed it a JSON file → it creates fully structured NFDIxCS metadata in ORKG automatically.**

---

# 2. What is the NFDIxCS Versioning Schema in ORKG?

ORKG uses *templates* to impose semantic structure.  
Template **R1563436** defines how to describe **a specific version** of a research object and relate it to other versions and resources.

Its field set (property shapes) is:

| Field | Predicate | Type | Card. |
|------|-----------|------|------|
| Identifier | P37134 | unique identifier | **1..1** |
| Concept Identifier | P183159 | unique identifier | 0..1 |
| version | version | Version class | 0..∞ |
| Relations | P183160 | Versioning Relation Type | 0..∞ |
| Contributor Roles | P183174 | Contributor Roles class (C123120) | **1..∞** |
| provenance support | P105031 | literal text | 0..∞ |
| date metadata | P91006 | xsd:date | 0..∞ |

This template encodes the NFDIxCS and DataCite concepts of:

- **versioned DOIs**  
- **concept DOIs**  
- **semantic versions**  
- **typed relations between versions**  
- **provenance & metadata dates**  
- **structured contributor roles (name + role + ORCID + affiliation)**

The importer writes metadata into ORKG **exactly according to this schema**.

---

# 3. Why this importer exists

we can 

- versioned datasets/software/workflows
- internal logs and provenance metadata
- contributor-role assignments
- DOIs and concept DOIs
- version-in-time / version-in-space metadata

**publish into ORKG**, 
This importer solves that:

✔ Reads structured JSON  
✔ Applies the ORKG schema  
✔ Automatically builds correct ORKG resources  
✔ Fills all versioning fields  
✔ Adds contributor roles properly and reliably  
✔ Ensures consistent metadata across all versions and objects

---

# 4. Project structure
