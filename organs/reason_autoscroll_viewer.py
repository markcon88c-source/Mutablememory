# organs/reason_autoscroll_viewer.py

import random
import time
import os

FORCE_EMOJI = {
    "spark": "⚡",
    "drift": "🌬️",
    "echo": "🔊",
    "chaos": "🎰",
    "clarity": "💠",
    "memory": "🧠",
    "pressure": "🌩️"
}

REASON_EMOJI = {
    "success": "✨",
    "failure": "💀"
}

SLOT_EMOJI = ["🎰","🎲","⭐","💥","🔥","🌟","🌀","💫","⚡"]

class ReasonAutoViewer:
    def __init__(self, reason_organ):
        self.reason_organ = reason_organ
        self.words = list(reason_organ.atlas.keys())
        self.anim_speed = 0.02
        self.pause_between_words = 1.2
        self.pause_between_forces = 0.4

    def clear(self):
        os.system("clear")

    def line(self):
        print("=" * 60)

    def flicker(self, text, speed=None):
        if speed is None:
            speed = self.anim_speed
        for c in text:
            print(c, end="", flush=True)
            time.sleep(speed)
        print()

    def show_reason(self, symbol, reason, block):
        emoji = REASON_EMOJI["success"] if symbol == "✔" else REASON_EMOJI["failure"]
        print(f"  {emoji} {symbol} {reason}")
        print(f"      {block}")

    def slot_reveal(self, reasons):
        # Slot machine flicker
        for _ in range(12):
            r = random.choice(reasons)
            e = random.choice(SLOT_EMOJI)
            print(f"  {e} {r[0]}")
            time.sleep(0.04)

        # Final reveal
        final = random.choice(reasons)
        symbol = "✔" if final in reasons else "✖"
        print()
        print("  🎉 FINAL REVEAL 🎉")
        self.show_reason(symbol, final[0], final[1])
        print()

    def show_force(self, word, force):
        sheet = self.reason_organ.get_sheet(word)
        if not sheet or force not in sheet:
            return

        success = sheet[force]["success"]
        failure = sheet[force]["failure"]
        all_reasons = success + failure

        icon = FORCE_EMOJI.get(force, "❓")

        self.line()
        self.flicker(f" {icon} {force.upper()} — REVEAL {icon}", speed=0.01)
        self.line()

        self.slot_reveal(all_reasons)

    def show_word(self, word):
        self.clear()
        self.line()
        self.flicker(f" 🌈 WORD: {word.upper()} 🌈 ", speed=0.01)
        self.line()

        forces = ["spark","drift","echo","chaos","clarity","memory","pressure"]
        random.shuffle(forces)

        for force in forces:
            self.show_force(word, force)
            time.sleep(self.pause_between_forces)

    def run(self):
        while True:
            for word in self.words:
                self.show_word(word)
                time.sleep(self.pause_between_words)
