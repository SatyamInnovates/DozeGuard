# DozeGuard

**Keep your Linux laptop awake. Even with the lid closed.**

DozeGuard is a Linux desktop application that keeps your computer awake whenever you want.

it is mainly designed for long tasks like downloading a game, or a agent working and a lot of things.

**Why i build DozeGuard**

I noticed a problem where while my agent is working or my games are downloading it takes time till then I go somewhere and laptop sleeps and the work gets disrupt but changing system settings are not recommended.

Heading out? Start DozeGuard, activate Lid Mode, and close your laptop without automatically interrupting your running tasks. Your coding agents and background processes can keep working while you're away.

With a simple desktop window, convenient system tray controls, and dedicated Lid Mode, DozeGuard puts you in control and solved these questions.


**Close the lid. Keep the work going.**

<img width="1912" height="988" alt="image" src="https://github.com/user-attachments/assets/525ca985-bb0c-4af6-abd8-284dd850b8fd" />


I built Linux utility in Python that communicates with systemd-logind to prevent automatic system suspension, with a CLI and desktop tray interface


## Features

- **Lid Mode:** keep you laptop awake when lid is closed so your task can be complete.
- **Keep Awake Mode:** Prevent automatic sleep for a selected duration or until you manually stop the session.
- **Desktop Application:** Start and manage sessions through a simple app.
- **System Tray:** A small sqaure box will appear in your task manager or panel(if you have one).
- **Background Operation:** You don't need to open the app for it to be working it works on background
- **Battery Awareness:** Battery information is used for safety. Unknown battery information does not prevent a session from starting.
- **CLI Fallback:** Manage things from terminal if the graphical interface is unavailable.

## Why DozeGuard instead of changing system settings?

Linux and even other OS give you setting to change that controls what happends when you close your laptop lid. So why build DozeGuard?

The problem is that changing those settings usually changes your system's general behavior. For example, you might disable suspend on lid close, but then your laptop will also stay awake when you don't actually need it.

I wanted something temporary and flexible.

With DozeGuard i can just start it and let my things done then it will stop as you don't need your laptop to be awake when you don't want it.

Instead of permanently changing my power settings, I can control when I want my laptop to stay awake.

Also It's not recommended to change these settings.

**The idea is simple: control when your laptop stays awake, rather than changing how it behaves all the time.**

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

Only install the file which is for your distro.(eg: rpm files is for fedora)

After downloading, extract the ZIP folder then  open your terminal inside the extracted folder and run command some installation commands given below.

### Ubuntu / Debian

Download `.deb` package:

```bash
sudo apt install ./dozeguard_[0-9]*_all.deb ./dozeguard-tray_[0-9]*_all.deb
```
Then it will ask for confirmation and you just to select Y.

### Fedora

Download both `.rpm` packages:

```bash
sudo dnf install ./dozeguard-[0-9]*.rpm ./dozeguard-tray-*.rpm
```
It's an rpm package so you can uninstall it also with one command.

### Arch Linux

<blockquote>**Not tested yet:** Arch Linux packages have not been tested on a real Arch Linux. i don't guarantee if the installation will be smooth.</blockquote>

Download `.pkg.tar.zst` package:

```bash
sudo pacman -U ./dozeguard-[0-9]*.pkg.tar.zst ./dozeguard-tray-*.pkg.tar.zst
```

## Let's start

After installation, open **DozeGuard** from your desktop's Applications menu.

Or

(Now you can use DozeGuard from your root, you won't have to open the extrated folder terminal to use it)
You can also launch it using below command from your terminal:

```bash
dozeguard-tray
```

After launching the app or useing the above command you will get a DozeGuard window and also a icon in your task-bar from where you can control the DozeGaurd.

From the application, you can manage your keep-awake sessions.

### System Tray
<img width="336" height="192" alt="image" src="https://github.com/user-attachments/assets/13a75fc2-0c4d-4cdb-8e4c-78776fddbe3d" />


DozeGuard runs in the background while you work.

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

Lid Mode is designed for situations where you want to close your laptop lid without interferring your tasks.


You don't have to enable it. It's already enabled

For example:
- Continue downloads with the lid closed.
- Keep long-running tasks active.
- Leave coding agents and background processes running while you're away.

Actual lid-close behavior depends on your system's power-management configuration, hardware, and firmware. DozeGuard cannot override every hardware-level power behavior.

It can be very useful as when you are travelling somewhere then you can start the session close the lid and keep in your bag it will work fine!!

## ⌨️ CLI Fallback

The graphical application is the best way to use DozeGuard, but a command-line interface is also available(if GUI get's doesn't work).

If the DozeGuard window or system tray is unavailable, you can still manage sessions from the terminal.

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

**Note:** Packages from GitHub Releases are the best way to install as it's very easy. Source installation is only for developers.

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

##  Development

Install development dependencies:

```bash
python3 -m pip install -e '.[test]'
```

Run the test suite:

```bash
python3 -m pytest
```

Automated tests use mocked logind and battery hardware. Actual sleep-inhibition and desktop behavior require testing on a running Linux system.

## Uninstallation

Remove DozeGuard from your device.

Open  terminal and run below command.

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

**Important:** Your screen may still dim, turn off, or lock automatically according to your desktop environment's power-management settings. This does not mean the laptop has stopped the task and sleep.

The laptop should remain awake while the DozeGuard session is active.


**Proof of work**

### Lid-Close Sleep Prevention Test

I tested it.

- **DozeGuard ON:** Laptop lid closed for 10 minutes; background loop continued running.
- **DozeGuard OFF:** Laptop lid closed for around 2 minutes and few seconds; background loop showed a -2m 54s timestamp gap.

So basically it worked great.




The project is not yet complete there is many things to do like make it more reliable and also make it access for other OS.
