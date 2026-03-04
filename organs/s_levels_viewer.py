# organs/s_levels_viewer.py
# Casino-style S-Levels viewer with:
# - Top 5 fixed header block
# - 12-word rotating sample (from main)
# - 4-line visible reel window
# - No blinking (static frame)
# - Cursor-up rewrite only

from typing import Dict, Any
import sys


class SLevelsViewer:
    def __init__(self, favorite_word: str = None):
        self.tick = 0
        self.favorite_word = favorite_word

        # scrolling state
        self.reel_index = 0
        self.window_size = 4   # visible scrolling lines
        self.speed = 1         # scroll speed

        # frame printed once
        self.frame_drawn = False

        # number of fixed header lines
        self.header_size = 5

    def _progress_bar(self, micro: int, score: float) -> str:
        filled = micro
        partial = int(score * 10)
        bar = "█" * filled + "▒" * partial
        return bar.ljust(27)

    def _format_entry(self, word: str, entry: Dict[str, Any]) -> str:
        lvl = entry["level"]
        micro = entry["micro"]
        score = entry["score"]
        stype = entry.get("story_type", "unknown")
        bar = self._progress_bar(micro, score)
        return f"{word:<12} [{stype:<7}]  L{lvl}-{micro:02d}  {bar}  ({score:+.2f})"

    def _draw_frame_once(self):
        """Draw the static frame only once."""
        print("\n   🎰 S-Levels Reel:")
        print("   ┌──────────────────────────────────────────────────────────────┐")

        # header block (fixed)
        for _ in range(self.header_size):
            print("   │                                                              │")

        # scrolling block (visible window)
        for _ in range(self.window_size):
            print("   │                                                              │")

        print("   └──────────────────────────────────────────────────────────────┘")
        self.frame_drawn = True

    def _move_cursor_up(self, n: int):
        sys.stdout.write(f"\033[{n}A")

    def step(self, s_state: Dict[str, Any]):
        self.tick += 1

        levels = s_state.get("levels", {})
        if not levels:
            return

        # sort by S-level → micro → score
        sorted_words = sorted(
            levels.items(),
            key=lambda kv: (kv[1]["level"], kv[1]["micro"], kv[1]["score"]),
            reverse=True
        )

        # convert to formatted lines
        reel = [self._format_entry(word, entry) for word, entry in sorted_words]
        if not reel:
            return

        # draw frame once
        if not self.frame_drawn:
            self._draw_frame_once()

        # split into header + scrollable
        header = reel[:self.header_size]
        scrollable = reel[self.header_size:] if len(reel) > self.header_size else [" "]

        # compute scrolling window
        window = []
        for i in range(self.window_size):
            idx = (self.reel_index + i) % len(scrollable)
            window.append(scrollable[idx])

        # total lines inside frame = header_size + window_size
        total_inside = self.header_size + self.window_size

        # move cursor to top of inside area
        self._move_cursor_up(total_inside + 1)

        # rewrite header block
        for line in header:
            print(f"   │ {line:<60} │")

        # rewrite scrolling block
        for line in window:
            print(f"   │ {line:<60} │")

        # advance reel
        self.reel_index = (self.reel_index + self.speed) % len(scrollable)
