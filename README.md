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
| `bulk-admitted/` | **8,500+** | Pre-extracted via the data-extractor pipeline across **22 vendors / 1,180+ families**.  YAML ready, codegen admission is per-chip. |

Bulk-admitted breakdown (8 source families):

* **CMSIS-Pack catalog** — 7,700+ chips across 16 vendors (SiLabs,
  Nuvoton, Infineon, Cypress, TI, Renesas, Toshiba, Ambiq, ARM,
  + 7 community vendors).  Vendor packs auto-downloaded;
  per-chip provenance recorded.
* **STM32 cross-source merge** — 503 chips (CMSIS-SVD ⊕ STM32
  open-pin-data) with full pinmux + AF tables at schema 1.3.0.
* **Zephyr DTS** — 159 chips across nordic / atmel / ambiq /
  silabs / ti families.
* **Microchip ATDF** — 47 AVR-DA + SAM E70/V71.
* **CMSIS-SVD direct** — 110 STM32 + 8 Espressif + 2 NXP iMXRT.

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
