# LDAP Browser

> Неофициальная сборка на базе Apache Directory Studio для Mac с Apple Silicon

LDAP Browser is a desktop client for browsing, searching, and editing LDAP directories on Apple silicon Macs. It is an independent fork of Apache Directory Studio at commit `4f9a5065b1d4897258ff0a838a62e59f20da9246`. [Upstream source](https://github.com/apache/directory-studio/tree/4f9a5065b1d4897258ff0a838a62e59f20da9246)

The macOS package is a client edition. It includes the LDAP browser, LDIF editor, schema editor and the OpenLDAP configuration tools. The embedded ApacheDS server feature is omitted because the server bundle carries older copies of LDAP API and MINA. Its upstream source is retained.

## Install and open

1. Download `LDAPBrowser-macos-arm64.zip` and `SHA256.txt` from the same GitHub release. Run `shasum -a 256 LDAPBrowser-macos-arm64.zip` and compare the result with the corresponding line in `SHA256.txt`.
2. Extract the ZIP, move `LDAP Browser.app` to Applications, and open it. The app bundles Amazon Corretto 11, so a separate Java installation is unnecessary.
3. In the **Connections** view, create an LDAP connection with the host, port, encryption, and authentication settings for your directory.

The app is ad hoc signed and ships without Developer ID signing or Apple notarization. macOS may block it on first launch. This release uses an older Studio and Eclipse codebase and has limited test coverage.

By default, LDAP Browser uses `~/.LDAPBrowser` for its workspace and `~/.LDAPBrowser/secure_storage` for its Equinox secure storage file. The Equinox provider may still share a master key through macOS Keychain. The upstream Studio p2 update sites are omitted and automatic updates are disabled.

## Build from source

The build requires an Apple silicon Mac with Apple command-line developer tools, Python 3, and internet access. Run the build script from the source root.

```sh
bash release/build.sh
```

The script downloads and verifies Corretto `11.0.33.1.1` and Maven `3.8.8`, builds against Eclipse Platform `4.24` with Tycho `2.3.0`, and prints the path to the resulting `LDAPBrowser-macos-arm64.zip`. The release build skips Maven tests and excludes the upstream integration test modules, which depend on the legacy LDAP test API. Pass the extracted app's path to the verification script to check its native components and bundled license files.

```sh
python3 release/verify.py "/Applications/LDAP Browser.app"
```

For a local smoke test, run `bash release/local-ldap.sh` on a Mac with the macOS OpenLDAP tools. Connect anonymously to `127.0.0.1` on port `13839` and browse `dc=studio,dc=test`. The sample directory is read-only. Press Ctrl+C in the terminal to stop it.

## License and attribution

The fork is licensed under Apache-2.0. The app includes Eclipse, Corretto, and other components under their respective licenses. See the license and notices for upstream attribution, bundled notices, and the corresponding source archives. [LICENSE](LICENSE) · [NOTICE](NOTICE) · [Third-party software and source code](release/THIRD-PARTY.md)
