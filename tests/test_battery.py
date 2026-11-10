from core.battery_rule import should_stop


def test_high_battery_keep_going():
    assert should_stop(80,False) is False

def test_low_battery_stops():
    assert should_stop(20,False) is True

def test_low_batttery_but_plugges_in_keep_gooing():
    assert should_stop(20,True) is False

def test_exactly_at_floor():
    assert should_stop(30,False) is True

def test_no_battery_reading():
    assert should_stop(None,False) is False
