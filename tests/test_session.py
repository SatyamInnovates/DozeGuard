from core.session import Session

def test_new_session_is_not_active():
    assert Session().is_active() is False

def test_start_makes_it_active():
    s = Session()
    s.start(minutes=1)
    assert s.is_active() is True

def test_remaining_is_within_a_minute():
    s = Session()
    s.start(minutes=1)
    assert 0 < s.remaining() <= 60

def test_stop_makes_it_inactive():
    s = Session()
    s.start(minutes=1)
    s.stop()
    assert s.is_active() is False

def test_unlimited_has_no_remaining():
    s = Session()
    s.start()
    assert s.is_active() is True
    assert s.remaining() is None