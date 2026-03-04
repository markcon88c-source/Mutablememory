import time
import sys
from viewer.viewer_registry import get_all_viewers

SCROLL_SPEED = 0.08        # seconds per line (slow crawl)
VIEWER_DURATION = 2.5      # seconds each viewer stays on screen

def clear():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def scroll_lines(lines):
    for line in lines:
        print(line)
        time.sleep(SCROLL_SPEED)

def run_viewers(creature):
    viewers = get_all_viewers()

    while True:
        for viewer in viewers:
            clear()
            lines = viewer.render(creature)   # viewer returns a list of lines
            scroll_lines(lines)
            time.sleep(VIEWER_DURATION)
