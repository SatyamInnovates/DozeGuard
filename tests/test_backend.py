from types import SimpleNamespace

from backends import linux


def test_unknown_battery_is_not_reported_as_charging(monkeypatch):
    monkeypatch.setattr(linux.psutil, "sensors_battery", lambda: None)
    assert linux.read_battery() == (None, None)


def test_battery_read_error_is_unknown(monkeypatch):
    def fail():
        raise OSError("sysfs unavailable")
    monkeypatch.setattr(linux.psutil, "sensors_battery", fail)
    assert linux.read_battery() == (None, None)


def test_battery_reading_passes_through_values(monkeypatch):
    monkeypatch.setattr(
        linux.psutil, "sensors_battery",
        lambda: SimpleNamespace(percent=42.5, power_plugged=False),
    )
    assert linux.read_battery() == (42.5, False)
