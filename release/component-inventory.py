#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Inventory the preserved disclosure files in each Eclipse plug-in and feature."""
import sys
import zipfile
from pathlib import Path


def is_disclosure(name):
    file_name = Path(name).name.lower()
    return file_name in {"about.html", "license.html", "epl-2.0.html", "epl-v10.html"} or file_name.startswith(
        ("license", "notice", "copying", "third-party", "third_party")
    )


def disclosure_files(component):
    if component.is_dir():
        return sorted(
            str(path.relative_to(component)) for path in component.rglob("*")
            if path.is_file() and is_disclosure(path.name)
        )
    with zipfile.ZipFile(component) as bundle:
        return sorted(name for name in bundle.namelist() if is_disclosure(name))


eclipse = Path(sys.argv[1]) / "Contents" / "Eclipse"
print("Type\tComponent and version\tIncluded notices")
for kind in ("features", "plugins"):
    for item in sorted((eclipse / kind).iterdir()):
        print(f"{kind}\t{item.name}\t{', '.join(disclosure_files(item))}")
