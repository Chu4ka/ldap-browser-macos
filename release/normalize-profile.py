#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Drop build-only repositories and neutralize Tycho's installation path before signing."""
import gzip
import sys
from pathlib import Path
from xml.sax.saxutils import escape


app = Path(sys.argv[1])
built_app = Path(sys.argv[2]).resolve()
neutral_app = "/Applications/LDAP Browser.app"
p2 = app / "Contents" / "Eclipse" / "p2"

for prefs in p2.rglob("org.eclipse.equinox.p2.*.repository.prefs"):
    lines = prefs.read_text().splitlines(keepends=True)
    # Eclipse stores these repositories as individual properties on one line each.
    portable_lines = [line for line in lines if not line.startswith(r"repositories/file\:")]
    if portable_lines != lines:
        prefs.write_text("".join(portable_lines))

for profile in p2.rglob("*.profile.gz"):
    with gzip.open(profile, "rt", encoding="utf-8") as stream:
        text = stream.read()
    # The profile still describes the installed product, which p2 can relocate.
    # Using the target's suffix preserves its rollback bookkeeping.
    text = text.replace(escape(str(built_app), {"'": "&apos;"}), escape(neutral_app))
    if str(Path.home()) in text or str(built_app) in text:
        raise SystemExit(f"Build-machine location remains in {profile.name}")
    with gzip.open(profile, "wt", encoding="utf-8") as stream:
        stream.write(text)
