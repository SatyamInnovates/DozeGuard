# DozeGuard

**Keep your Linux PC awake. Stay focused on what matters.**

Ever had your computer go to sleep while downloading a large file, watching something, running a long task, or working on something important?

That's what DozeGuard is for.

DozeGuard is a Linux desktop application that keeps your computer awake for a period you choose. It runs quietly in your system tray, gives you a simple window to manage your sessions, and lets you get back to work without worrying about automatic sleep.

## What you get

- **Simple desktop window:** Start and manage your keep-awake sessions without using the terminal.
- **System tray integration:** Keep DozeGuard accessible from your desktop while you work.
- **Flexible sessions:** Choose a specific duration or keep your computer awake until you stop the session.
- **Background operation:** Close the window without ending the active tray session.
- **CLI fallback:** Manage sessions from the terminal if the graphical interface isn't available.

## Compatibility

DozeGuard uses `systemd-logind` through the system D-Bus to prevent automatic sleep. A working system bus and logind service are required.

| Distribution | Status |
|---|---|
| Ubuntu | Tested |
| Fedora | Tested |
| Debian | Distribution CI passed; manual testing pending |
| Arch Linux | Not tested; experimental |

The graphical application requires PySide6 and a desktop environment that supports a system tray host. Tray behavior can vary between desktop environments.

See [COMPATIBILITY.md](COMPATIBILITY.md) for more details.

## Installation

Download the appropriate packages from [GitHub Releases](https://github.com/SatyamInnovates/DozeGuard/releases).

The graphical application is provided as a separate package. Install both the core and tray packages for the complete DozeGuard experience.

### Ubuntu and Debian

Download both `.deb` packages and run:

```bash
sudo apt install ./dozeguard_*.deb ./dozeguard-tray_*.deb
```

### Fedora

Download both `.rpm` packages and run:

```bash
sudo dnf install ./dozeguard-*.rpm ./dozeguard-tray-*.rpm
```

### Arch Linux

<blockquote>**Experimental:** Arch Linux packages have not yet been tested on a real Arch installation. Use them at your own discretion.</blockquote>

Download both `.pkg.tar.zst` packages and run:

```bash
sudo pacman -U ./dozeguard-*.pkg.tar.zst ./dozeguard-tray-*.pkg.tar.zst
```

Check the downloaded filenames before running the commands to avoid selecting the wrong package versions.

## Getting started

After installation, open **DozeGuard** from your desktop's Applications menu.

You can also launch it from the terminal:

```bash
dozeguard-tray
```

The application opens its window and provides a system tray icon when a compatible tray host is available.

Once running, you can:

1. Choose how long you want to keep your computer awake.
2. Start your session.
3. Minimize or close the window while DozeGuard remains accessible from the tray.
4. Stop the session whenever you're finished.

You can also launch DozeGuard in tray-only mode:

```bash
dozeguard-tray --background
```

## CLI fallback

Prefer the terminal, or having trouble launching the graphical application? DozeGuard also provides a command-line interface.

Start a 30-minute session:

```bash
dozeguard start 30
```

Keep your computer awake until stopped:

```bash
dozeguard start
```

Check the current session:

```bash
dozeguard status
```

Stop the session:

```bash
dozeguard stop
```

Shut down the background daemon:

```bash
dozeguard shutdown
```

The CLI works independently of the graphical application and does not require PySide6.

## Install from source

For users who want to install DozeGuard directly from the source code, Python 3.10 or newer is required.

Create a virtual environment:

```bash
python3 -m venv ~/.venvs/dozeguard
```

Install DozeGuard with graphical support:

```bash
~/.venvs/dozeguard/bin/pip install '.[tray]'
```

For CLI-only use:

```bash
~/.venvs/dozeguard/bin/pip install .
```

## Development

Install the development dependencies:

```bash
python3 -m pip install -e '.[test]'
```

Run the tests:

```bash
python3 -m pytest
```

Automated tests cover application logic using mocked logind and battery hardware. Actual sleep-inhibition and desktop tray behavior require testing on a running Linux desktop.

## Uninstallation

Remove DozeGuard using your distribution's package manager.

**Ubuntu / Debian**

```bash
sudo apt remove dozeguard-tray dozeguard
```

**Fedora**

```bash
sudo dnf remove dozeguard-tray dozeguard
```

**Arch Linux**

```bash
sudo pacman -R dozeguard-tray dozeguard
```

If a keep-awake session is active, stop the daemon before uninstalling:

```bash
dozeguard shutdown
```

---

**DozeGuard** — A small desktop utility to keep your Linux computer awake.

[GitHub Repository](https://github.com/SatyamInnovates/DozeGuard)
