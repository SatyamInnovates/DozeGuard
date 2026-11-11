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

Omit `[tray]` for CLI-only use. Distribution packages should install the
runtime dependencies using native package dependencies; package recipes are
provided in `debian/`, `dozeguard.spec`, and `PKGBUILD`. The Qt tray remains an
optional PySide6 extra because Qt 6 bindings are not packaged under one
consistent name across the target Debian and Ubuntu releases.

## Use

```sh
dozeguard start 30
dozeguard start       # until stopped
dozeguard status
dozeguard stop
dozeguard shutdown   # stop the daemon and remove its runtime socket
dozeguard-tray        # optional GUI frontend
```

The daemon starts on demand and runs as the current user. Its socket is under
`$XDG_RUNTIME_DIR/dozeguard/` when that variable names a private directory
owned by the user. Otherwise it uses `~/.local/run/dozeguard/`. Logs are under
`$XDG_STATE_HOME/dozeguard/` or `~/.local/state/dozeguard/`. Both directories
are user-private. DozeGuard does not install or enable an automatic startup
service.

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
