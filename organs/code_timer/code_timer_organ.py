#!/usr/bin/env python3
import time
from organs.code_refresh.code_refresh_organ import refresh_all_code

def timed_code_refresh(hours=12):
    """
    Refreshes all organ code every <hours>.
    Default: 12 hours.
    """
    seconds = hours * 3600

    while True:
        cache = refresh_all_code()
        print("[Timer] Code refreshed for:", list(cache.all().keys()))
        time.sleep(seconds)


def main():
    import sys
    hours = int(sys.argv[2]) if len(sys.argv) >= 3 else 12
    timed_code_refresh(hours)
