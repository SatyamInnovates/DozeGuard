



def should_stop(percent, plugged_in, floor=30):
    # Preserve desktop behavior: unknown battery telemetry does not block a
    # session, but callers must keep it distinct from a charging battery.
    if percent is None:
        return False
    if plugged_in is True:
        return False

    return percent <= floor
