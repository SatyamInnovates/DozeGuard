# DozeGuard

**Keep your Linux laptop awake. Even with the lid closed.**

DozeGuard is a Linux desktop application that keeps your computer awake when you need it most.

Downloading large files? Running long-running tasks? Working with AI coding agents? DozeGuard helps keep everything running without your laptop automatically going to sleep.

Heading out? Start DozeGuard, close your laptop lid, put it in your bag, and let your coding agents keep working while you're on the move. Stay productive without having to keep your laptop open.

With a simple desktop window, convenient system tray controls, and dedicated Lid Mode, DozeGuard puts you in control of when your laptop stays awake.

**Close the lid. Keep the work going.**

## ✨ Features

- **Lid Mode:** Keep your laptop awake when the lid is closed, subject to system power-management and hardware behavior.
- **Keep Awake Mode:** Prevent automatic sleep for a selected duration or until you manually stop the session.
- **Desktop Application:** Start and manage sessions through a straightforward graphical interface.
- **System Tray:** Access DozeGuard while you work without keeping its main window open.
- **Background Operation:** Close the application window while keeping DozeGuard accessible from the system tray.
- **CLI Fallback:** Manage sessions from the terminal if the graphical interface is unavailable.
- **Fully Reliable** I have tested it on other machines and even tested with battery fallback.(it stops working if your laptop get's too low)
## 🖥️ Compatibility

DozeGuard uses `systemd-logind` through the system D-Bus to request sleep inhibition.

A working system bus and logind service are required.

| Distribution | Status |
|---|---|
| Ubuntu | Tested |
| Fedora | Tested |
| Debian | Tested |
| Arch Linux | Not tested |

The graphical application requires PySide6 and a desktop environment with a compatible system tray host.

Tray behavior may vary depending on your desktop environment and its notification services.

See [COMPATIBILITY.md](COMPATIBILITY.md) for more information.

## 📦 Installation

Download the appropriate packages from the [GitHub Releases](https://github.com/SatyamInnovates/DozeGuard/releases) page.

For the complete graphical experience, install both the core and tray packages.

### Ubuntu / Debian

Download the two `.deb` packages and install them:

```bash
sudo apt install ./dozeguard_*.deb ./dozeguard-tray_*.deb
```

### Fedora

Download both `.rpm` packages:

```bash
sudo dnf install ./dozeguard-*.rpm ./dozeguard-tray-*.rpm
```

### Arch Linux

<blockquote>**Experimental — Not tested:** Arch Linux packages have not yet been tested on a real Arch Linux installation. Installation and runtime behavior are not guaranteed.</blockquote>

Download both `.pkg.tar.zst` packages:

```bash
sudo pacman -U ./dozeguard-*.pkg.tar.zst ./dozeguard-tray-*.pkg.tar.zst
```

Check the filenames before installation to ensure you select the correct package versions.

## 🚀 Getting Started

After installation, open **DozeGuard** from your desktop's Applications menu.

You can also launch it using:

```bash
dozeguard-tray
```

The main window opens, and DozeGuard attempts to provide a system tray icon when a compatible tray host is available.

From the application, you can manage your keep-awake sessions and use Lid Mode.

### System Tray

DozeGuard can continue running in the background while you work.

- Open the main window from the tray.
- Manage your active session.
- Quit DozeGuard when you're finished.

To launch directly in tray-only mode:

```bash
dozeguard-tray --background
```

### Lid Mode

**Close your laptop. Keep your work running.**

Lid Mode is designed for situations where you want to close your laptop without automatically interrupting an active task.

For example:

- Continue downloads with the lid closed.
- Keep long-running tasks active.
- Leave background work running while your laptop is closed.

Actual lid-close behavior depends on your system's power-management configuration, hardware, and firmware. DozeGuard cannot override every hardware-level power behavior.

## ⌨️ CLI Fallback

The graphical application is the primary way to use DozeGuard, but a command-line interface is also available.

If the graphical interface or system tray is unavailable, you can still manage sessions from the terminal.

Start a 30-minute session:

```bash
dozeguard start 30
```

Keep the computer awake until manually stopped:

```bash
dozeguard start
```

Check the current session:

```bash
dozeguard status
```

Stop the active session:

```bash
dozeguard stop
```

Shut down the background daemon:

```bash
dozeguard shutdown
```

The CLI works independently of the graphical application and does not require PySide6.

## 🛠️ Install from Source

For users who prefer installing directly from source, Python 3.10 or newer is required.

Create a virtual environment:

```bash
python3 -m venv ~/.venvs/dozeguard
```

Install DozeGuard with graphical support:

```bash
~/.venvs/dozeguard/bin/pip install '.[tray]'
```

For CLI-only installation:

```bash
~/.venvs/dozeguard/bin/pip install .
```

## 🧪 Development

Install development dependencies:

```bash
python3 -m pip install -e '.[test]'
```

Run the test suite:

```bash
python3 -m pytest
```

Automated tests use mocked logind and battery hardware. Actual sleep-inhibition and desktop behavior require testing on a running Linux system.

## 🗑️ Uninstallation

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

If a keep-awake session is active, shut down the daemon before uninstalling:

```bash
dozeguard shutdown
```

---

**DozeGuard** — Your laptop, your control.

[GitHub Repository](https://github.com/SatyamInnovates/DozeGuard)
