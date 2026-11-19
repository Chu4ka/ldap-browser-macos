#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
kit=$(cd "$(dirname "$0")" && pwd)
source_app=$1
jdk=$2
dest=$3
mkdir "$dest"
app="$dest/LDAP Browser.app"
/usr/bin/ditto "$source_app" "$app"
/usr/bin/ditto "$jdk" "$app/Contents/runtime"
python3 - "$app" <<'PY'
from pathlib import Path
import plistlib
import sys

contents = Path(sys.argv[1]) / 'Contents'
plist = contents / 'Info.plist'
with plist.open('rb') as stream:
    info = plistlib.load(stream)
if info['CFBundleExecutable'] != 'LDAPBrowser':
    raise SystemExit('Unexpected launcher from Tycho')
info.update(CFBundleIdentifier='org.ldapbrowser.macos', CFBundleDisplayName='LDAP Browser',
            CFBundleName='LDAP Browser', CFBundleShortVersionString='0.1.0',
            CFBundleVersion='1')
if info.get('Eclipse') == ['-keyring', '~/.eclipse_keyring']:
    del info['Eclipse']
with plist.open('wb') as stream:
    plistlib.dump(info, stream)

ini = contents / 'Eclipse' / 'LDAPBrowser.ini'
text = ini.read_text()
if text.splitlines().count('-vmargs') != 1 or '-vm' in text.splitlines():
    raise SystemExit('Unexpected launcher ini')
text = '-eclipse.keyring\n@user.home/.LDAPBrowser/secure_storage\n' + text
ini.write_text(text.replace('-vmargs\n', '-vm\n../runtime/Contents/Home/lib/jli/libjli.dylib\n-vmargs\n', 1))
PY
python3 "$kit/normalize-profile.py" "$app" "$source_app"
legal="$app/Contents/Resources/Legal"
mkdir "$legal"
cp "$app/Contents/Eclipse/LICENSE" "$legal/LICENSE-Studio.txt"
cp "$app/Contents/Eclipse/NOTICE" "$legal/NOTICE-Studio.txt"
cp "$kit/THIRD-PARTY.md" "$legal/THIRD-PARTY.md"
cp "$kit/Eclipse-add-on-sources.tsv" "$legal/Eclipse-add-on-sources.tsv"
for feature in "$app"/Contents/Eclipse/features/org.eclipse.platform_*/epl-2.0.html; do
    cp "$feature" "$legal/EPL-2.0.html"
done
python3 "$kit/component-inventory.py" "$app" > "$legal/Eclipse-components.tsv"
/usr/bin/codesign --force --sign - --timestamp=none "$app"
/usr/bin/codesign --verify --strict "$app"
python3 "$kit/verify.py" "$app"
(cd "$dest" && /usr/bin/ditto -c -k --norsrc --keepParent "LDAP Browser.app" LDAPBrowser-macos-arm64.zip)
