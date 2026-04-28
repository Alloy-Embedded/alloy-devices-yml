# Changelog

## 2026-04-28 — Initial population

* Schemas imported from alloy-codegen
  (`schema/canonical_device/{device,family,vendor}.schema.json`).
* Bootstrap snapshot of every (vendor, family, device) triple
  alloy-codegen admitted at the time of the split:
  - `espressif/esp32/{esp32, esp32-wroom32}`
  - `espressif/esp32c3/esp32c3`
  - `espressif/esp32s3/esp32s3`
  - `microchip/avr-da/avr128da32`
  - `microchip/same70/{atsame70n21b, atsame70q21b}`
  - `nordic/nrf52/nrf52840`
  - `nxp/imxrt1060/{mimxrt1062, mimxrt1064}`
  - `raspberrypi/rp2040/{pico, rp2040}`
  - `st/stm32f4/{stm32f401re, stm32f405rg}`
  - `st/stm32g0/{stm32g030f6, stm32g071rb, stm32g0b1re}`

  17 devices total.  Each YAML is the byte-deterministic output
  of `alloy_codegen.canonical_device_yaml.serialize_device(...)`
  applied to the resolved IR for that triple.
