# Compatibility and Validation Status

This document describes the testing and validation performed for DozeGuard.

It separates automated source tests, native package validation, and real-world desktop and hardware testing. A successful package build does not automatically guarantee compatibility with every Linux desktop or laptop.

## Distribution Compatibility

| Distribution | Package format | Validation status |
|---|---|---|
| Fedora 44 | RPM | Manually tested |
| Ubuntu 24.04 | DEB | Manually tested |
| Ubuntu 26.04 | DEB | Manually tested |
| Debian 13 (Stable) | DEB | Manually tested |
| Arch Linux | Arch package | Not tested |

### Fedora

- Core and tray RPM packages built successfully.
- Package installation and dependency resolution tested.
- CLI commands verified.
- Graphical application launched successfully.
- Basic application functionality checked.

### Ubuntu

- Core and tray DEB packages installed successfully.
- Dependencies resolved through APT.
- CLI commands and session functionality tested.
- Graphical application launched successfully.
- Tray interactions and autostart behavior tested.

**Ubuntu 24.04 note:** PySide6 is not available through its standard repositories in the required form. A per-user virtual environment is available as an alternative for installing graphical support.

### Debian

- Core and tray DEB packages installed successfully.
- Dependencies resolved through APT.
- CLI commands and session functionality tested.
- Graphical application launched successfully.
- Tray interactions and autostart behavior tested.
- Installation and removal checked.

### Arch Linux

<blockquote>**Not tested.** Arch Linux packages have not yet been validated on a real Arch Linux installation. Installation, upgrades, desktop integration, and runtime behavior remain unverified.</blockquote>

The Arch package recipe exists, but its successful build alone should not be considered proof of runtime compatibility.

## Automated Testing

The automated test suite covers application logic, including:

- Session management.
- Daemon behavior.
- IPC communication.
- Sleep-inhibitor logic using mocked logind.
- Battery telemetry handling.
- Error handling and application behavior.

The latest reported working-tree snapshot passed **48 automated tests**.

These tests are not a substitute for testing actual sleep inhibition on physical hardware.

## Desktop Environment Compatibility

The graphical application requires PySide6 and a desktop environment that provides a compatible system tray host.

The following desktop environments have not been comprehensively validated for tray visibility, menus, notifications, and startup behavior:

- KDE Plasma
- GNOME
- XFCE
- Cinnamon

Tray behavior may vary depending on the desktop environment and its notification and system tray services.

No universal desktop compatibility guarantee is currently made.

## Sleep Inhibition and Lid Mode

DozeGuard uses `systemd-logind` over the system D-Bus to request sleep inhibition.

A working system bus and logind service are required.

Systems without a working `systemd-logind` service are unsupported for sleep prevention.

Lid Mode behavior also depends on:

- Laptop hardware and firmware.
- System power-management configuration.
- The desktop environment.
- Whether the system honors the requested sleep inhibitor during lid-close events.

A sleep inhibitor cannot override every hardware-level or firmware-level power action.

## Battery Handling

Battery information is obtained through `psutil`.

- When battery information is available, DozeGuard can report the detected battery state.
- When battery information is unavailable, it reports the state as unknown.
- Unknown battery telemetry does not prevent a session from starting.

Battery reporting and low-battery behavior can vary between hardware and have not been comprehensively validated across all supported distributions.

## Package Lifecycle

Native package validation includes checks for:

- Package installation.
- Dependency resolution.
- CLI entry points.
- Python imports.
- Desktop-entry placement.
- Autostart configuration where tested.
- Package removal.
- Upgrade behavior where tested.

Package removal does not currently stop an already-running per-user DozeGuard daemon.

Before uninstalling, run:

```bash
dozeguard shutdown
```

This releases the active inhibitor, stops the existing daemon, and removes its runtime socket.

User logs and state stored in XDG directories are retained after package removal.

## Testing Limitations

The following areas still require additional validation:

- Real suspend prevention across different laptop models.
- Lid-close behavior across different hardware and firmware configurations.
- Tray integration across desktop environments.
- Notifications and desktop startup behavior across different distributions.
- Arch Linux installation and runtime behavior.
- Package removal while a detached daemon is active.

## Summary

DozeGuard has been manually tested on Ubuntu, Fedora, and Debian.

Arch Linux remains untested.

Automated tests and package validation provide useful confidence, but actual sleep inhibition and lid behavior depend on the user's Linux environment and hardware.

**Testing status will be updated as additional distributions and desktop configurations are validated.**
