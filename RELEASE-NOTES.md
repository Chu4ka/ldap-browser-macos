# LDAP Browser v0.1.0

> Неофициальная сборка на базе Apache Directory Studio для Mac с Apple Silicon

Version 0.1.0 is the first Apple silicon macOS release of LDAP Browser, an independent fork of Apache Directory Studio. It bundles Corretto `11.0.33.1.1` and uses Eclipse Platform `4.24`. The LDAP client uses Apache LDAP API `2.1.9` and MINA `2.2.10`. The macOS package omits the embedded ApacheDS server feature, whose server archive contains older copies of these libraries. [Upstream source](https://github.com/apache/directory-studio/tree/4f9a5065b1d4897258ff0a838a62e59f20da9246)

- The app uses its own default workspace and Equinox secure storage file under `~/.LDAPBrowser`. The Equinox provider may still share a master key through macOS Keychain.
- The upstream Apache Directory Studio p2 update sites are omitted, and automatic updates are disabled. Download future versions from GitHub Releases.
- The app is ad hoc signed and ships without Developer ID signing or Apple notarization. macOS may block it on first launch.

## Downloads

| Asset | Contents |
| --- | --- |
| `LDAPBrowser-macos-arm64.zip` | Apple silicon macOS app with bundled Java |
| `LDAPBrowser-0.1.0-source.tar.gz` | Application source, downstream changes, and build and packaging scripts |
| `corretto-11.0.33.1.1-source.tar.gz` | Source for the bundled Corretto runtime |
| `eclipse-platform-sources-4.24.tar.xz` | Eclipse Platform source |
| `LDAPBrowser-add-on-sources.zip` | Sources for the bundled add-on components |
| `SHA256.txt` | SHA-256 checksums for the release assets |

Run `shasum -a 256 LDAPBrowser-macos-arm64.zip` and compare the result with the corresponding entry in `SHA256.txt`. Extract the ZIP and move `LDAP Browser.app` to Applications. License and source details are in `release/THIRD-PARTY.md` in the source archive and in the app bundle at `Contents/Resources/Legal/THIRD-PARTY.md`.

## Compatibility and testing

The packaged client launched natively on macOS 27.2.1 (Apple silicon) with its bundled JVM. A local read-only LDAP test used an anonymous bind and found one expected record, which the SWT search editor displayed. The ZIP was extracted and the app signature and native architecture were checked again.

The release build excludes the upstream integration test modules. Authentication, LDAPS, StartTLS and compatibility across macOS versions and LDAP servers remain unverified. The inherited certificate trust override can accept a previously trusted certificate across hosts. This preview retains Eclipse 4.24 and other older upstream components. [Apache LDAP API security notices](https://directory.apache.org/api/)
