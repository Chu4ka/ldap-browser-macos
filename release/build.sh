#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
[[ $(uname -sm) == 'Darwin arm64' ]] || { echo "Requires native macOS arm64" >&2; exit 1; }
base=$(mktemp -d /private/tmp/ldap-browser-build.XXXXXXXX)
echo "Build directory: $base"
mkdir "$base/java" "$base/maven" "$base/build-home"
fetch() {
    curl --disable --fail --location --proto '=https' --proto-redir '=https' --retry 2 --output "$base/$2" "$1"
}
fetch https://corretto.aws/downloads/resources/11.0.33.1.1/amazon-corretto-11.0.33.1.1-macosx-aarch64.tar.gz jdk.tar.gz
fetch https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.8.8/apache-maven-3.8.8-bin.tar.gz maven.tar.gz
(
    cd "$base"
    echo '79b8a95fb1cf6424b0053c75bcc260b20e54becc1b6062e3918215edd796db7a  jdk.tar.gz' | shasum -a 256 -c -
    echo '332088670d14fa9ff346e6858ca0acca304666596fec86eea89253bd496d3c90deae2be5091be199f48e09d46cec817c6419d5161fb4ee37871503f472765d00  maven.tar.gz' | shasum -a 512 -c -
    tar -xzf jdk.tar.gz --strip-components 1 -C java
    tar -xzf maven.tar.gz --strip-components 1 -C maven
)
export JAVA_HOME="$base/java/Contents/Home"
export MAVEN_SKIP_RC=1
export MAVEN_OPTS="-Xmx2g -Duser.home=$base/build-home -Declipse.p2.mirrors=false"
maven="$base/maven/bin/mvn"
# Maven generates files in the checked-out source tree.
cd "$repo"
args=(-B -ntp "-Dmaven.repo.local=$base/build-home/repository" -DskipTests)
"$maven" -version
"$maven" "${args[@]}" -f pom-first.xml clean install
# The upstream integration fixtures depend on the legacy LDAP test API.
"$maven" "${args[@]}" -pl '!tests,!tests/test.integration.core,!tests/test.integration.ui' clean package
app=product/target/products/org.apache.directory.studio.product/macosx/cocoa/aarch64/LDAPBrowser.app
bash "$repo/release/package.sh" "$app" "$base/java" "$base/result"
echo "Result: $base/result/LDAPBrowser-macos-arm64.zip"
