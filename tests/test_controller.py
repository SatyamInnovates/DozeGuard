
from controller import Controller


def test_start_starts_session_and_inhibitor(monkeypatch):
    c = Controller()


    started = []

    monkeypatch.setattr(c.inhibitor, "start", lambda: started.append(True))

    assert c.start(minutes=30) is True
    assert c.session.is_active()
    assert started == [True]

    c.stop()


def test_stop_stops_session_and_inhibitor(monkeypatch):
    c = Controller()

    stopped = []

    monkeypatch.setattr(c.inhibitor, "start", lambda: None)
    monkeypatch.setattr(c.inhibitor, "stop", lambda: stopped.append(True))

    c.start(minutes=30)
    c.stop()

    assert not c.session.is_active()
    assert stopped == [True]




def test_duplicate_start_does_not_start_inhibitor_twice(monkeypatch):
    c = Controller()

    started = []

    monkeypatch.setattr(c.inhibitor, "start", lambda: started.append(True))

    assert c.start(minutes=30) is True
    assert c.start(minutes=30) is False

    assert len(started) == 1

    c.stop()





def test_inhibitor_failure_resets_session(monkeypatch):
    c = Controller()

    def failing_start():
        raise RuntimeError("Inhibitor failed")

    monkeypatch.setattr(c.inhibitor, "start", failing_start)

    try:
        c.start(minutes=30)
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass

    assert not c.session.is_active()


def test_timer_expiration_releases_inhibitor(monkeypatch):
    c = Controller()

    stopped = []

    monkeypatch.setattr(c.inhibitor, "start", lambda: None)
    monkeypatch.setattr(c.inhibitor, "stop", lambda: stopped.append(True))

    c.start(minutes=0.001)

    import time
    time.sleep(0.1)

    assert not c.is_active()
    assert stopped == [True]
