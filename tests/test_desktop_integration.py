import sys
import types

import pytest

import desktop_integration
from desktop_integration import TrayInstanceLock, set_autostart_enabled
from tray import (
    parse_arguments,
    should_run_background,
    should_show_window,
    user_tray_venv_python,
)


def test_normal_and_background_launch_modes():
    assert parse_arguments([]).background is False
    assert parse_arguments(["--background"]).background is True
    assert should_show_window(False) is True
    assert should_show_window(True) is False
    assert should_run_background(False) is False


@pytest.mark.parametrize(("arguments", "expected_background"), [([], False), (["--background"], True)])
def test_entry_point_dispatches_normal_and_background_modes(
    arguments, expected_background, tmp_path, monkeypatch
):
    import tray

    monkeypatch.setattr(tray, "_delegate_to_user_tray_venv", lambda _argv: None)
    monkeypatch.setattr(tray, "runtime_directory", lambda: tmp_path / "runtime")
    modes = []
    monkeypatch.setattr(
        tray,
        "_run_qt",
        lambda background, _argv, **_kwargs: modes.append(background) or 0,
    )

    assert tray.main(arguments) == 0
    assert modes == [expected_background]


def test_autostart_disable_and_enable_use_managed_user_override(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    path = set_autostart_enabled(False)
    assert path.exists()
    assert "Hidden=true" in path.read_text()
    assert "X-DozeGuard-Managed=true" in path.read_text()

    set_autostart_enabled(True)
    assert "Hidden=false" in path.read_text()
    assert "Exec=" in path.read_text()
    assert "-m tray --background" in path.read_text()


def test_autostart_does_not_overwrite_unmanaged_user_entry(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    path = set_autostart_enabled(False)
    path.write_text("[Desktop Entry]\nName=My custom entry\n")
    with pytest.raises(FileExistsError):
        set_autostart_enabled(False)
    assert "My custom entry" in path.read_text()


def test_autostart_command_does_not_import_or_require_pyside(tmp_path, monkeypatch):
    import tray

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    assert tray.main(["--disable-autostart"]) == 0
    assert "Hidden=true" in (tmp_path / "config/autostart/dozeguard-tray.desktop").read_text()


def test_user_override_quotes_python_paths_for_xdg_exec(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setattr(desktop_integration.sys, "executable", "/home/user/Doze Guard/bin/python")
    path = set_autostart_enabled(True)
    assert 'Exec="/home/user/Doze Guard/bin/python" -m tray --background' in path.read_text()


def test_optional_tray_venv_uses_xdg_data_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    assert user_tray_venv_python() == tmp_path / "data/dozeguard/tray-venv/bin/python"


def test_tray_lock_prevents_duplicate_instances(tmp_path):
    path = tmp_path / "runtime" / "tray.lock"
    first = TrayInstanceLock.acquire(path)
    assert first is not None
    assert TrayInstanceLock.acquire(path) is None
    first.close()
    second = TrayInstanceLock.acquire(path)
    assert second is not None
    second.close()


def test_background_missing_tray_support_exits_without_gui():
    assert should_run_background(False) is False
    assert should_run_background(True) is True


def test_background_launch_without_tray_host_exits_before_creating_window(monkeypatch):
    import tray

    class FakeApplication:
        def __init__(self, _argv):
            self.exec_called = False

        def setApplicationName(self, _name):
            pass

        def exec(self):
            self.exec_called = True
            return 0

    application = FakeApplication(["dozeguard-tray"])

    class FakeTrayIcon:
        @staticmethod
        def isSystemTrayAvailable():
            return False

    qt_core = types.ModuleType("PySide6.QtCore")
    qt_core.QTimer = object
    qt_gui = types.ModuleType("PySide6.QtGui")
    qt_gui.QColor = qt_gui.QIcon = qt_gui.QPixmap = object
    qt_widgets = types.ModuleType("PySide6.QtWidgets")
    qt_widgets.QApplication = lambda _argv: application
    qt_widgets.QSystemTrayIcon = FakeTrayIcon
    for name in (
        "QLabel", "QMainWindow", "QMenu", "QPushButton", "QVBoxLayout", "QWidget"
    ):
        setattr(qt_widgets, name, object)
    pyside6 = types.ModuleType("PySide6")
    pyside6.__path__ = []
    monkeypatch.setitem(sys.modules, "PySide6", pyside6)
    monkeypatch.setitem(sys.modules, "PySide6.QtCore", qt_core)
    monkeypatch.setitem(sys.modules, "PySide6.QtGui", qt_gui)
    monkeypatch.setitem(sys.modules, "PySide6.QtWidgets", qt_widgets)

    assert tray._run_qt(True, ["--background"]) == 0
    assert application.exec_called is False


def test_autostart_desktop_entry_uses_background_mode():
    from pathlib import Path

    desktop = Path(__file__).parents[1] / "dozeguard-tray-autostart.desktop"
    text = desktop.read_text()
    assert "Exec=dozeguard-tray --background" in text
    assert "TryExec=dozeguard-tray" in text


def test_packaging_metadata_keeps_pyside_optional():
    from pathlib import Path

    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

    root = Path(__file__).parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    assert any(dep.startswith("PySide6") for dep in project["optional-dependencies"]["tray"])
    assert not any(dep.startswith("PySide6") for dep in project["dependencies"])


def test_tray_desktop_files_are_owned_by_optional_packages():
    from pathlib import Path

    root = Path(__file__).parents[1]
    deb_tray = (root / "debian/dozeguard-tray.install").read_text()
    deb_core = (root / "debian/dozeguard.install").read_text()
    assert "dozeguard-tray.desktop" in deb_tray
    assert "desktop" not in deb_core
    assert "etc/xdg/autostart/dozeguard-tray.desktop" in (root / "debian/rules").read_text()
    assert "rm -f /etc/xdg/autostart/dozeguard-tray.desktop" in (
        root / "debian/dozeguard-tray.postrm"
    ).read_text()
    assert "python3-pyside6" in (root / "debian/control").read_text()
    assert "python3-pyside6" in (root / "dozeguard.spec").read_text()
    assert "pyside6" in (root / "PKGBUILD").read_text()
    assert "Exec=dozeguard-tray\n" in (root / "dozeguard-tray.desktop").read_text()
