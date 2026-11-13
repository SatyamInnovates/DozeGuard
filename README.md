# DozeGuard

**Keep your Linux laptop awake. Even with the lid closed.**

DozeGuard is a Linux desktop application that keeps your computer awake when you need it most.

Downloading large files? Running long-running tasks? Working with AI coding agents? DozeGuard helps keep your work running without your laptop automatically going to sleep.

Heading out? Start DozeGuard, activate Lid Mode, and close your laptop without automatically interrupting your running tasks. Your coding agents and background processes can keep working while you're away.

With a simple desktop window, convenient system tray controls, and dedicated Lid Mode, DozeGuard puts you in control of when your laptop stays awake.

**Close the lid. Keep the work going.**

<img width="1912" height="988" alt="image" src="https://github.com/user-attachments/assets/525ca985-bb0c-4af6-abd8-284dd850b8fd" />

## Features

- **Lid Mode:** keep you laptop awake when lid is closed so your task can be complete.
- **Keep Awake Mode:** Prevent automatic sleep for a selected duration or until you manually stop the session.
- **Desktop Application:** Start and manage sessions through a simple app.
- **System Tray:** A small sqaure box will appear in your task manager or panel(if you have one).
- **Background Operation:** You don't need to open the app for it to be working it works on background
- **Battery Awareness:** Battery information is used for safety. Unknown battery information does not prevent a session from starting.
- **CLI Fallback:** Manage things from terminal if the graphical interface is unavailable.

## Compatibility

DozeGuard uses `systemd-logind` through the system D-Bus to request sleep inhibition.

It is developed in Fedora 44 KDE so if you use Fedora it will be the best.

A working system bus and logind service are required to start a session. Systems without a working logind service are not supported.

### Tested distributions

| Distribution | Status |
|---|---|
| Ubuntu | Tested |
| Fedora | Tested |
| Debian | Tested |
| Arch Linux | Not tested |

important: I have not tested it on Arch because of some issues so there can be bugs so use the ones which is tested.

The graphical application requires PySide6 and a desktop environment with a compatible system tray host.(package will install all of these)

Tray behavior and notifications may vary depending on your desktop environment.


See [COMPATIBILITY.md](COMPATIBILITY.md) for more information.

## 📦 Installation

Download the package from the [GitHub Releases](https://github.com/SatyamInnovates/DozeGuard/releases).

Only install the file which is for your Distro.

After downloading, extract the ZIP archive, open a terminal inside the extracted folder, and run command below.

### Ubuntu / Debian

Download `.deb` package:

```bash
sudo apt install ./dozeguard_[0-9]*_all.deb ./dozeguard-tray_[0-9]*_all.deb
```

### Fedora

Download both `.rpm` packages:

```bash
sudo dnf install ./dozeguard-[0-9]*.rpm ./dozeguard-tray-*.rpm
```

### Arch Linux

<blockquote>**Experimental — Not tested:** Arch Linux packages have not been tested on a real Arch Linux. i don't guarantee if the installation will be smooth. Use at your own discretion.</blockquote>

Download `.pkg.tar.zst` package:

```bash
sudo pacman -U ./dozeguard-[0-9]*.pkg.tar.zst ./dozeguard-tray-*.pkg.tar.zst
```

## Let's start

After installation, open **DozeGuard** from your desktop's Applications menu.

Or

You can also launch it using:

```bash
dozeguard-tray
```

The main window appears from where when you first start a session the system tray icon will also come in the taskbar or panel and from there you can control it without opening the window.

From the application, you can manage your keep-awake sessions.

### System Tray
<img width="336" height="192" alt="image" src="https://github.com/user-attachments/assets/13a75fc2-0c4d-4cdb-8e4c-78776fddbe3d" />


DozeGuard can continue running in the background while you work.

- Right click on the square box.
- Manage your active session.
- Quit DozeGuard when you're finished.

It will be yellow when session isn't working and turn into green when session is working.

If you want to launch directly in tray-only mode:

```bash
dozeguard-tray --background
```

### Lid Mode

**Close your laptop. Keep your work running.**

Lid Mode is designed for situations where you want to close your laptop without automatically interrupting an active task.

You don't have to enable it. It's already enabled

For example:
- Continue downloads with the lid closed.
- Keep long-running tasks active.
- Leave coding agents and background processes running while you're away.

Actual lid-close behavior depends on your system's power-management configuration, hardware, and firmware. DozeGuard cannot override every hardware-level power behavior.

## ⌨️ CLI Fallback

The graphical application is the best way to use DozeGuard, but a command-line interface is also available.

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

**Note:** Packages from GitHub Releases are the recommended installation method. Source installation is only for developers.

Python 3.10 or newer is required.

Create a virtual environment:

```bash
python3.11 -m venv ~/.venvs/dozeguard
```

Install DozeGuard with gui:

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

Remove DozeGuard.

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


##important:
### Screen Lock vs. System Suspend

DozeGuard prevents system suspend while an active sleep-inhibition session is running.

**Important:** Your screen may still dim, turn off, or lock automatically according to your desktop environment's power-management settings. This does not mean the laptop has entered system suspend.

The laptop should remain awake while the DozeGuard session is active.




The project is not yet complete there is many things to do like make it more reliable and also make it access for other OS.
