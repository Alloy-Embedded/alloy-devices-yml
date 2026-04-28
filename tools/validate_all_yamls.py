#!/usr/bin/env python3
"""Validate every YAML in alloy-devices-yml against its schema.

Used by `lock-canonical-yaml-schema-v1` as the gate that every
PR runs in CI.  Mirrors the inline validator in
`.github/workflows/validate.yml` so contributors can run the
same check locally.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    schemas_dir = repo / "schema" / "canonical_device"
    schemas = {
        "device": json.loads((schemas_dir / "device.schema.json").read_text(encoding="utf-8")),
        "family": json.loads((schemas_dir / "family.schema.json").read_text(encoding="utf-8")),
        "vendor": json.loads((schemas_dir / "vendor.schema.json").read_text(encoding="utf-8")),
    }
    validators = {kind: Draft202012Validator(schema) for kind, schema in schemas.items()}

    failures: list[str] = []

    def _check(path: Path, kind: str) -> None:
        text = path.read_text(encoding="utf-8")
        payload = yaml.safe_load(text)
        errors = sorted(
            validators[kind].iter_errors(payload), key=lambda e: list(e.absolute_path)
        )
        if errors:
            failures.append(str(path))
            print(f"FAIL {path}", file=sys.stderr)
            for err in errors[:5]:
                where = "/".join(str(p) for p in err.absolute_path) or "<root>"
                print(f"  • {where}: {err.message}", file=sys.stderr)
            return
        if kind == "device" and "schema_version" not in payload:
            failures.append(str(path))
            print(f"FAIL {path}: missing required `schema_version`", file=sys.stderr)
            return
        print(f"OK   {path}")

    for path in sorted((repo / "vendors").glob("**/devices/*.yml")):
        _check(path, "device")
    for path in sorted((repo / "vendors").glob("**/family.yml")):
        _check(path, "family")
    for path in sorted((repo / "vendors").glob("*/vendor.yml")):
        _check(path, "vendor")

    if failures:
        print(f"\n{len(failures)} YAML(s) failed validation.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
