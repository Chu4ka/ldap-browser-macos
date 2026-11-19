<!-- SPDX-License-Identifier: Apache-2.0 -->
# Third-party software and source code

LDAP Browser is independently maintained and based on Apache Directory Studio at commit `4f9a5065b1d4897258ff0a838a62e59f20da9246`. Apache Directory Studio is a mark of the Apache Software Foundation. [Upstream source](https://github.com/apache/directory-studio/tree/4f9a5065b1d4897258ff0a838a62e59f20da9246)

## Files in the app

- `Contents/Eclipse/LICENSE` and `Contents/Eclipse/NOTICE` carry Apache Directory Studio's Apache-2.0 license and upstream attributions.
- `Contents/Eclipse/features` and `Contents/Eclipse/plugins` retain the original components and their license, about and notice files. The inventory `Eclipse-components.tsv` lists installed versions and where those files are found. `EPL-2.0.html` reproduces the Eclipse Platform license.
- `Contents/runtime/Contents/Home/LICENSE`, `ADDITIONAL_LICENSE_INFO`, `ASSEMBLY_EXCEPTION` and `legal/` cover the bundled Corretto runtime and its third-party components. The runtime adds software under the GPLv2 with the Classpath Exception where specified in its notices. Corretto also bundles async-profiler 4.6 under Apache-2.0. [Corretto distribution](https://github.com/corretto/corretto-11/releases/tag/11.0.33.1.1) · [async-profiler source](https://github.com/async-profiler/async-profiler/tree/v4.6)

## Source packages for this release

| Release asset | Contents and provenance |
| --- | --- |
| `LDAPBrowser-0.1.0-source.tar.gz` | Complete application source and packaging scripts, including all downstream modifications. |
| `corretto-11.0.33.1.1-source.tar.gz` | Corretto source and build scripts at commit `2da045a8705b995e7d5495dbf96b65dace1c3b92`, recorded by the vendor JDK. [GitHub source](https://github.com/corretto/corretto-11/commit/2da045a8705b995e7d5495dbf96b65dace1c3b92) |
| `eclipse-platform-sources-4.24.tar.xz` | Eclipse Platform 4.24 source for the RCP, SWT and Equinox components. [Eclipse 4.24](https://archive.eclipse.org/eclipse/downloads/drops4/R-4.24-202206070700/) |
| `LDAPBrowser-add-on-sources.zip` | Version-matched Eclipse ECF, EMF, Jetty, SAT4J, Servlet/JSP/EL, Orbit JNA and other source artifacts. Includes source for JNA native code and async-profiler. See `Eclipse-add-on-sources.tsv` for exact bundle versions and official origins. |

The embedded JDK is the vendor binary for Corretto 11.0.33.1.1. Its archive was verified against the published SHA-256. The source archive above is from the Git revision recorded by that binary. Its build metadata also contains the Corretto dirty-tree marker. The vendor's native build was not reproduced independently. [Vendor download and checksum](https://github.com/corretto/corretto-11/releases/tag/11.0.33.1.1)

Eclipse Babel Oxygen R0.15.1 French and German translations are included as editable properties in their installed fragments. [Eclipse Babel archive](https://archive.eclipse.org/technology/babel/babel_language_packs/R0.15.1/oxygen/oxygen.php)

The bundled Jakarta Servlet API 4.0 bundle maps to Maven artifact `jakarta.servlet:jakarta.servlet-api:4.0.4`. Its source is included in the add-on archive and made available under EPL-2.0. [Eclipse component metadata](https://download.eclipse.org/releases/2022-06/202206151000/buildInfo/archive/download.eclipse.org/releases/2022-06/202206151000/index/jakarta.servlet-api_4.0.0.html) · [Original Maven artifact](https://central.sonatype.com/artifact/jakarta.servlet/jakarta.servlet-api/4.0.4)

The LDAP client stack uses Apache Directory LDAP API 2.1.9 and Apache MINA 2.2.10 under Apache-2.0. Their bundled licenses are preserved in the plug-ins. The embedded ApacheDS distribution is omitted from the macOS client package. [Apache LDAP API 2.1.9 source](https://github.com/apache/directory-ldap-api/tree/2.1.9) · [Apache MINA 2.2.10 downloads and source](https://mina.apache.org/downloads-mina_2_2.html)
