#!/bin/bash
# Start a read-only sample directory in the foreground on the IPv4 loopback interface.
set -euo pipefail
kit=$(cd "$(dirname "$0")" && pwd)
base=$(mktemp -d /private/tmp/studio-ldap.XXXXXXXX)
mkdir "$base/data"
cat > "$base/slapd.conf" <<EOF
include /etc/openldap/schema/core.schema
include /etc/openldap/schema/cosine.schema
pidfile "$base/slapd.pid"
argsfile "$base/slapd.args"
database ldif
suffix "dc=studio,dc=test"
directory "$base/data"
readonly on
access to * by * read
EOF
/usr/sbin/slapadd -f "$base/slapd.conf" -l "$kit/fixture.ldif"
echo "Anonymous LDAP: 127.0.0.1:13839; base dc=studio,dc=test; Ctrl+C to stop. Data: $base"
exec /usr/libexec/slapd -f "$base/slapd.conf" -h ldap://127.0.0.1:13839/ -d 256
