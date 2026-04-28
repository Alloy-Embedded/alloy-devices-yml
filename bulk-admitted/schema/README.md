# Canonical device-data schema

This directory holds the JSON Schemas that every YAML in
`vendors/**/devices/*.yml` must validate against.

## Files

| Schema | Validates |
|---|---|
| `canonical_device/device.schema.json` | One MCU YAML (`vendors/<v>/<f>/devices/<d>.yml`) |
| `canonical_device/family.schema.json` | One family YAML (`vendors/<v>/<f>/family.yml`) |
| `canonical_device/vendor.schema.json` | One vendor YAML (`vendors/<v>/vendor.yml`) |

## Versioning rule (`lock-canonical-yaml-schema-v1`)

The schema's identity is the `schema_version` field that every
device YAML carries.  It evolves under semver:

| Bump | Example | Meaning | Existing YAMLs |
|---|---|---|---|
| **PATCH** | `1.2.0 → 1.2.1` | Purely additive new optional fields. | Continue to validate without modification. |
| **MINOR** | `1.2.x → 1.3.0` | Adds a required field with a documented backfill path. | Must be rewritten before the new schema is enforced. |
| **MAJOR** | `1.x.x → 2.0.0` | Incompatible restructuring of existing fields. | Both extractor and codegen pin to one major; the bump is coordinated. |

### Hard contracts

- Every device YAML MUST declare `schema_version` matching the
  bundled schema's version.
- alloy-data-extractor's `write_device_yaml(...)` refuses to
  write a payload missing `schema_version` or whose major
  differs from the bundled `SCHEMA_VERSION_CURRENT`.
- alloy-codegen's `parse_device(...)` refuses to load a YAML
  whose major differs from `IR_SCHEMA_VERSION` (raises
  `IRSchemaVersionMismatch`).
- alloy-devices-yml CI fails any PR that introduces or modifies
  a YAML that does not validate against `device.schema.json`.

### Bumping the schema

1. Edit `schema/canonical_device/device.schema.json`.
2. Update `IR_SCHEMA_VERSION` in alloy-codegen `bootstrap.py`
   and `SCHEMA_VERSION_CURRENT` in alloy-data-extractor
   `emit/canonical_yaml.py` to the new value.
3. For MINOR or MAJOR bumps, regenerate every YAML in this
   repo at the new version (typically by re-running the
   matching extractor) and commit them in the same PR as the
   schema change.
4. For MAJOR bumps, update the consumer in alloy-codegen so it
   accepts the new major.

### Validation locally

```sh
python tools/validate_all_yamls.py
```

The CI workflow at `.github/workflows/validate.yml` runs the
same check on every PR.
