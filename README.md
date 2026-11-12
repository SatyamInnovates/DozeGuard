# DozeGuard

DozeGuard keeps a Linux session awake for a chosen period by holding a sleep
inhibitor. The command line interface works without the optional Qt tray.

## Compatibility

See [COMPATIBILITY.md](COMPATIBILITY.md) for the tested and untested distro,
package, and desktop combinations. Sleep inhibition uses `systemd-logind` over
the system D-Bus; a working system bus and logind service are required to
start a session. DozeGuard has no non-systemd inhibition backend.

Battery telemetry comes from psutil. If battery state cannot be read,
DozeGuard reports it as unknown and allows the session to start. The optional
tray requires PySide6 and a desktop session that provides a tray host; no
GNOME, KDE Plasma, XFCE, or Cinnamon tray compatibility is currently claimed.

## Install from source

Use Python 3.10 or newer and install the package into a virtual environment:

```sh
python3 -m venv ~/.venvs/dozeguard
~/.venvs/dozeguard/bin/pip install '.[tray]'
~/.venvs/dozeguard/bin/dozeguard status
```

Omit `[tray]` for CLI-only use. Package recipes are provided in `debian/`,
`dozeguard.spec`, and `PKGBUILD`. The tray is a separate optional package in
native package builds. Ubuntu 24.04 does not provide the PySide6 binding from
its standard archive. From a DozeGuard source checkout, install the optional
tray into the well-known per-user venv:

```sh
python3 -m venv ~/.local/share/dozeguard/tray-venv
~/.local/share/dozeguard/tray-venv/bin/pip install '.[tray]'
~/.local/share/dozeguard/tray-venv/bin/dozeguard-tray --enable-autostart
```

The packaged launcher detects this venv and uses it for the window and tray.
CLI-only installations remain independent of PySide6.

For native package installs, the tray package pulls in the core application:

```sh
sudo apt install dozeguard-tray       # Debian or Ubuntu
sudo dnf install dozeguard-tray       # Fedora
sudo pacman -S dozeguard-tray         # Arch Linux
```

## Use

```sh
dozeguard start 30
dozeguard start       # until stopped
dozeguard status
dozeguard stop
dozeguard shutdown   # stop the daemon and remove its runtime socket
dozeguard-tray        # open the window and tray icon
dozeguard-tray --background  # tray only, for desktop login startup
dozeguard-tray --disable-autostart
dozeguard-tray --enable-autostart
```

The normal Applications-menu launcher opens the DozeGuard window and exposes
the tray icon when the desktop provides a tray host. Closing the window leaves
the tray active; use its menu to reopen the window or quit. If tray support is
unavailable, a normal launch still opens the window. A background launch exits
without opening a window when no tray host is available.
The tray requests notifications through Qt's system-tray notification API;
delivery depends on the desktop's tray and notification services.

Installing the native `dozeguard-tray` package installs the Applications-menu
entry and an XDG system-wide autostart entry. It starts in background mode at
login by default. Disable it for the current user with
`dozeguard-tray --disable-autostart`; re-enable it with
`dozeguard-tray --enable-autostart`. These commands write only DozeGuard's
`~/.config/autostart/dozeguard-tray.desktop` override and refuse to replace an
unmanaged file at that path. Removing the package removes its system-wide
desktop files and preserves user configuration. The tray frontend uses a
per-user runtime lock to prevent duplicate tray processes.

The daemon starts on demand and runs as the current user. Its socket is under
`$XDG_RUNTIME_DIR/dozeguard/` when that variable names a private directory
owned by the user. Otherwise it uses `~/.local/run/dozeguard/`. Logs are under
`$XDG_STATE_HOME/dozeguard/` or `~/.local/state/dozeguard/`. Both directories
are user-private. The tray frontend starts only the tray at login; it does not
start the sleep-inhibition daemon unless a user starts a session.

`stop` ends an active keep-awake session but leaves the daemon available for
later commands. `shutdown` asks the existing daemon to release its inhibitor,
exit, and remove its socket. It does not start a daemon when none is running.

## Development

```sh
python3 -m pip install -e '.[test]'
python3 -m pytest
```

The test suite mocks logind and battery hardware. It does not prove actual
suspend prevention or tray behavior; those require a real logind session and
desktop sessions such as KDE Plasma, GNOME, XFCE, and Cinnamon.
