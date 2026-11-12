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
for openSUSE. Those GitHub Actions jobs have not yet run. The table records
earlier Phase 1/Phase 2 results; the current 1.0.0 tray package work is listed
below and is also local validation, not a GitHub Actions result.

## Current 1.0.0 tray and package validation

The current working-tree snapshot passed 48 automated tests. Debian 13 and
Ubuntu 24.04 core/tray DEBs built and passed isolated install, CLI, autostart
override, and removal checks. The Fedora 44 core/tray RPMs built and their
metadata and file ownership were inspected; they were not installed. Arch
core/tray packages built from a local source snapshot and their package
contents were inspected; package installation was not exercised. An initial
Arch dependency sync timed out, then the package build succeeded with download
timeouts disabled. GitHub Actions has not run for this working tree.

Ubuntu 24.04 does not provide PySide6 in its standard archive. The tray DEB
therefore recommends the distro binding when available; a per-user venv with
the `[tray]` extra is the documented route on 24.04. The launcher can delegate
to that venv. This path was smoke-tested headlessly, but not in a real desktop.

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

The package metadata uses version 1.0.0. The fallback source pins in the RPM
spec and PKGBUILD still identify the previously committed 1.0.0 source; the
current tray changes are uncommitted and cannot yet be referenced by an exact
source commit. CI builds from its checked-out commit. Before publishing the
native recipes, update both fallback pins to the commit containing these tray
and packaging changes. Debian builds use the selected source checkout and do
not have a separate source pin.
