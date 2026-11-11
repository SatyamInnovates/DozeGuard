# DozeGuard

DozeGuard keeps a Linux session awake for a chosen period by holding a sleep
inhibitor. The command line interface works without the optional Qt tray.

## Compatibility

The CLI, per-user Unix socket, and battery reporting target Fedora, Ubuntu,
Debian, Linux Mint, Arch Linux, and openSUSE. Sleep inhibition currently uses
`systemd-logind` over the system D-Bus. A working system bus and logind service
are required to start an active session. DozeGuard does **not** currently
provide a non-systemd inhibition backend, so installations without logind are
not supported for sleep prevention.

Battery telemetry comes from psutil. On systems without a readable battery,
DozeGuard reports battery and power state as unknown and allows the session to
start, preserving desktop behavior. The tray requires PySide6 and a desktop
session that provides a system tray host. Tray support is optional and can be
unavailable or hidden depending on desktop settings and extensions.

## Install from source

Use Python 3.10 or newer and install the package into a virtual environment:

```sh
python3 -m venv ~/.venvs/dozeguard
~/.venvs/dozeguard/bin/pip install '.[tray]'
~/.venvs/dozeguard/bin/dozeguard status
```

Omit `[tray]` for CLI-only use. Distribution packages should install the
runtime dependencies using native package dependencies; package recipes are
provided in `debian/`, `dozeguard.spec`, and `PKGBUILD`.

## Use

```sh
dozeguard start 30
dozeguard start       # until stopped
dozeguard status
dozeguard stop
dozeguard-tray        # optional GUI frontend
```

The daemon starts on demand and runs as the current user. Its socket is under
`$XDG_RUNTIME_DIR/dozeguard/` when that variable names a private directory
owned by the user. Otherwise it uses `~/.local/run/dozeguard/`. Logs are under
`$XDG_STATE_HOME/dozeguard/` or `~/.local/state/dozeguard/`. Both directories
are user-private. DozeGuard does not install or enable an automatic startup
service.

## Development

```sh
python3 -m pip install -e '.[test]'
python3 -m pytest
```

The test suite mocks logind and battery hardware. It does not prove actual
suspend prevention or tray behavior; those require a real logind session and
desktop sessions such as KDE Plasma, GNOME, XFCE, and Cinnamon.
