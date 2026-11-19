#!/usr/bin/env python3
"""Check the product launcher, JVM and native Eclipse fragments using Apple's lipo."""
import plistlib
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

app = Path(sys.argv[1]).resolve()
contents = app / "Contents"
with (contents / "Info.plist").open("rb") as stream:
    launcher = plistlib.load(stream)["CFBundleExecutable"]


def verify(path, label):
    archs = subprocess.check_output(["/usr/bin/lipo", "-archs", str(path)], text=True).split()
    if "arm64" not in archs:
        raise SystemExit(f"Missing arm64 in {label}: {archs}")
    print(f"{label}: {' '.join(archs)}")


verify(contents / "MacOS" / launcher, launcher)
runtime = contents / "runtime" / "Contents" / "Home"
for component in ["bin/java", "lib/server/libjvm.dylib", "lib/jli/libjli.dylib"]:
    verify(runtime / component, component)

# Check loose Mach-O helpers as well as the native libraries inside the two platform fragments.
mach_magic = {bytes.fromhex(x) for x in (
    "feedface", "cefaedfe", "feedfacf", "cffaedfe", "cafebabe", "bebafeca", "cafebabf", "bfbafeca"
)}
for item in sorted(contents.rglob("*")):
    if item.is_symlink() or not item.is_file() or item.suffix == ".class":
        continue
    with item.open("rb") as stream:
        magic = stream.read(4)
    if magic in mach_magic and "Mach-O" in subprocess.check_output(["/usr/bin/file", "-b", str(item)], text=True):
        verify(item, str(item.relative_to(contents)))

for legal in [contents / "Eclipse" / "LICENSE", contents / "Eclipse" / "NOTICE",
              runtime / "LICENSE", runtime / "ADDITIONAL_LICENSE_INFO", runtime / "ASSEMBLY_EXCEPTION"]:
    if not legal.is_file() or not legal.stat().st_size:
        raise SystemExit(f"Missing license or notice: {legal}")
if not (runtime / "legal" / "java.base").is_dir():
    raise SystemExit("Missing Corretto module licenses")
plugins = contents / "Eclipse" / "plugins"
with tempfile.TemporaryDirectory() as temp:
    for fragment in ["org.eclipse.swt.cocoa.macosx.aarch64", "org.eclipse.equinox.launcher.cocoa.macosx.aarch64"]:
        found = list(plugins.glob(fragment + "_*"))
        if len(found) != 1:
            raise SystemExit(f"Expected one {fragment}, found {found}")
        item = found[0]
        suffixes = (".jnilib", ".dylib", ".so")
        if item.is_dir():
            paths = [p for p in item.rglob("*") if p.is_file() and p.name.endswith(suffixes)]
            for path in paths:
                verify(path, path.name)
        else:
            with zipfile.ZipFile(item) as jar:
                paths = [name for name in jar.namelist() if name.endswith(suffixes)]
                for name in paths:
                    path = Path(temp) / "native"
                    path.write_bytes(jar.read(name))
                    verify(path, name)
        if not paths:
            raise SystemExit(f"No native libraries in {item.name}")
