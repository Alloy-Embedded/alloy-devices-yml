# alloy-devices-yml

Canonical device-data catalog for the
[alloy-codegen](https://github.com/Alloy-Embedded/alloy-codegen)
ecosystem.

This repository holds **data only**: one schema-validated YAML
file per admitted MCU.  Code generators (alloy-codegen for C++,
future siblings for Rust / Zig / docs) consume this catalog and
emit language-specific artifacts.

## Coverage at a glance

| Tree | Devices | Notes |
|---|---|---|
| `vendors/` | 17 | Codegen-admitted (DEVICE_REGISTRY).  Every chip here passes the codegen parity gate. |
| `bulk-admitted/` | 4,400+ | Pre-extracted via the data-extractor pipeline.  YAML ready, codegen admission per-chip. |

Bulk-admitted breakdown (8 source families across 22 vendors):

* **CMSIS-SVD** — 110 STM32 + 8 Espressif + 2 NXP iMXRT
* **STM32 open-pin-data** + CMSIS-SVD merge — 503 chips with full pinmux
* **Microchip ATDF** — 47 chips (AVR-DA, SAM E70/V71)
* **Zephyr DTS** — 159 chips (Nordic / Atmel SAM / Ambiq Apollo / SiLabs Gecko / TI cc13xx)
* **CMSIS-Pack catalog** — 3,650+ chips across SiLabs / Cypress / Infineon /
  Nuvoton / TI / Renesas / Toshiba / 12 more vendors

See `bulk-admitted/index.yml` for the per-chip catalog with
provenance, and `bulk-admitted/README.md` for the
promote-to-codegen workflow.

```
alloy-data-extractor (Python ETL)
       │ generates YAML
       ▼
alloy-devices-yml          ← you are here
       │ consumed by
       ▼
alloy-codegen           (C++ generator)
alloy-codegen-rust      (future)
alloy-codegen-zig       (future)
```

## Layout

```
schema/canonical_device/
    device.schema.json       # per-MCU canonical IR schema
    family.schema.json       # per-family catalog schema
    vendor.schema.json       # per-vendor metadata schema

vendors/<vendor>/
    vendor.yml               # vendor-level metadata
    <family>/
        family.yml           # family catalog (packages, IPs)
        devices/
            <device>.yml     # per-MCU canonical IR

index.yml                    # top-level catalog (every triple + provenance)
```

## Schema validation

Every committed `*.yml` is validated against
`schema/canonical_device/*.schema.json` in CI.  Local validation:

```bash
pip install jsonschema PyYAML
python -m alloy_codegen.canonical_device_yaml validate \
    vendors/st/stm32g0/devices/stm32g071rb.yml
```

## Adding a new MCU

The recommended path is via the
[alloy-data-extractor](https://github.com/Alloy-Embedded/alloy-data-extractor)
ETL pipeline — it produces YAML files automatically from vendor
sources (CMSIS-SVD, ATDF, MCUXpresso, Zephyr DTS, etc.).

For one-off contributions:

1. Author `vendors/<vendor>/<family>/devices/<device>.yml`
   following an existing device as template.
2. `schema_version: "1.2.0"` (matches alloy-codegen IR version).
3. Run schema validation locally.
4. Open a PR.

## Schema versioning

The `schema_version` field on every YAML matches
`alloy_codegen.bootstrap.IR_SCHEMA_VERSION`.  Migrations are
handled by alloy-codegen consumers; older YAMLs validate against
older schema revisions until the data repo migrates them.

## License

MIT — same as alloy-codegen.
