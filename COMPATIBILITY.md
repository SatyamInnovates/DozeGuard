# Compatibility and validation status

This report separates source tests, native package checks, and real desktop or
hardware behavior. A passing package build does not establish suspend or tray
compatibility.

## Distribution status

| Distribution | Source tests | Native package validation | Status |
|---|---|---|---|
| Fedora | 29 tests passed on the Fedora 44 development host during Phase 1 | RPM built, dependency resolution checked, installed, CLI and imports checked, and removed in Fedora 45 container | Package build and basic lifecycle tested; not a Fedora desktop-session test |
| Ubuntu 24.04 | Not run separately in Phase 2 | DEB built, dependencies resolved, installed, CLI and imports checked, desktop entry present, and removed | Package build and basic lifecycle tested |
| Debian stable (13) | Not run separately in Phase 2 | DEB built, dependencies resolved, installed, CLI and imports checked, upgraded from 0.1.0-1 to 0.1.0-2, and removed | Package build and basic lifecycle tested |
| Arch Linux | Not run separately in Phase 2 | PKGBUILD built from its pinned source commit, installed, CLI and imports checked, and removed | Package build and basic lifecycle tested; upgrade not exercised |
| openSUSE Tumbleweed | 29 tests passed in a clean container using distro Python packages and a venv | RPM build attempted; failed because the openSUSE Python RPM macros selected Python 3.14 while the container's `python3-devel` resolved to Python 3.13 | Source tests pass; current RPM spec is Fedora-compatible but not openSUSE-buildable in this environment |
| Linux Mint | Not tested directly | No native package build or install test | Untested; Ubuntu CI is not evidence of Mint compatibility |

The GitHub Actions workflow now defines distro test jobs and package
build/install/remove jobs for Debian, Ubuntu, Fedora, and Arch, and source tests
for openSUSE. Those GitHub Actions jobs have not yet run. The results above are
local isolated-container checks plus the Phase 1 Fedora host test; they are not
GitHub Actions results.

## Desktop, power, and hardware status

- KDE Plasma, GNOME, XFCE, and Cinnamon tray visibility, menus, notifications,
  and startup behavior have not been tested in real sessions. No tray
  compatibility claim is made for these desktops.
- Sleep inhibition requires an accessible system D-Bus and
  `systemd-logind`. Systems without logind, including non-systemd setups, are
  unsupported for sleep prevention.
- The tests mock logind and battery telemetry. Suspend prevention and battery
  reporting on real laptop hardware have not been validated across the target
  distributions.
- Unknown battery telemetry permits a session and is shown as unknown. This
  preserves the existing application policy.

## Package lifecycle limits

Package tests check installation, command entry points, imports, desktop-entry
placement, upgrade behavior where noted, and removal of package-owned files.
They do not test uninstalling while a detached DozeGuard daemon is active.
Package removal does not currently signal per-user daemons. Run
`dozeguard shutdown` before uninstalling; this releases any active inhibitor,
stops the daemon, and removes its runtime socket. Package removal still retains
user logs and state under XDG directories.

The planned release version is 1.0.0. Historical validation entries above refer
to packages built as version 0.1.0; they are not evidence that version 1.0.0
packages have been built or installed. RPM and Arch recipes are pinned to source commit
`1a74da5a27c86c9fe18c6fe4556091780bc64ee6`. Debian packages are built from the
selected source checkout and have no separate source commit pin. Package
version metadata is aligned to 1.0.0. Package build and installation results
for this release source revision should be recorded separately from the
historical Phase 2 validation above.
