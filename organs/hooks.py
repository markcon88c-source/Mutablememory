HOOK_THRESHOLD = 0.8

def compute_hook(pressures):
    sym = pressures["symbolic"]
    alt = pressures["alert"]

    if sym > HOOK_THRESHOLD and sym > alt:
        return True
    return False
