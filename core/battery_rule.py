



def should_stop(percent,plugged_in,floor=30):
    if percent is None:
        return False
    if plugged_in:
        return False

    return percent <= floor

    