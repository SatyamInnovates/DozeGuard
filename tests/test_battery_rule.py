
from core.battery_rule import should_stop


def test_stop_when_battery_reaches_floor():
    assert should_stop(30, False, 30) is True



def test_continue_when_battery_above_floor():
    assert should_stop(50, False, 30) is False


def test_continue_when_charger_connected():
    assert should_stop(20, True, 30) is False


def test_continue_when_battery_unknown():
    assert should_stop(None, False, 30) is False


def test_custom_battery_floor():
    assert should_stop(20, False, 20) is True
    assert should_stop(25, False, 20) is False


# junks files