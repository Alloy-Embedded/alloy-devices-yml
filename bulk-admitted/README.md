# bulk-admitted/

Auto-generated YAMLs from `alloy-data-extract bulk ...` runs.

These devices have **canonical YAML** but **no codegen-side
emitter coverage yet** — alloy-codegen still admits only the 17
devices in its `DEVICE_REGISTRY`, and the YAMLs in this tree
are not consumed by any codegen pipeline today.

This tree exists to:

1. **Prove the bulk-extraction pipeline at scale.** 120 chips
   across STM32 (110), Espressif (8), NXP iMXRT (2) extracted
   in a single CLI run with 100% pass rate.
2. **Pre-populate the catalog** so downstream alloy-codegen
   admission of any chip in this tree is trivial: just admit
   it to `DEVICE_REGISTRY` and the YAML is already there.
3. **Surface coverage gaps** to reviewers — every device in
   `bulk-report.json` with status `EXTRACT_FAILED` /
   `SCHEMA_INVALID` is a parser/template gap waiting to be
   patched.

## Layout

```
bulk-admitted/
├─ schema/                 # symlink-ish copy of ../schema for
│                          # in-tree schema validation.
├─ vendors/<v>/<f>/devices/<d>.yml
├─ bulk-report.json        # one row per chip with status +
│                          # error message.
└─ index.yml               # catalog summary (vendor / family /
                          # device count + first 1000 entries).
```

## Regenerating

```sh
alloy-data-extract bulk \
  --vendor st \
  --pack-root /path/to/cmsis-svd-data/data/STMicro \
  --output-root bulk-admitted \
  --report bulk-admitted/bulk-report.json
```

The current snapshot was produced from the cached
`cmsis-svd-data` (master), `espressif-svd` (master), and
`nxp-mcux-soc-svd` mirrors as of 2026-04-28.

## Promoting a chip into alloy-codegen admission

1. Add the device to `alloy_codegen.bootstrap.DEVICE_REGISTRY`.
2. Move its YAML from `bulk-admitted/vendors/...` to
   `vendors/<v>/<f>/devices/<d>.yml` (the codegen-consumed
   tree).
3. Run the codegen parity gate to validate the YAML
   round-trips through normalize unchanged.
