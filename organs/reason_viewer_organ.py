# organs/reason_viewer_organ.py

import random
import time

class ReasonViewerOrgan:
    def __init__(self, reason_organ):
        self.reason_organ = reason_organ
        self.words = list(reason_organ.atlas.keys())
        self.index = 0
        self.anim_speed = 0.02  # casino flicker speed

    # ---------------------------------------------------------
    # Utility: casino flicker effect
    # ---------------------------------------------------------
    def flicker(self, text):
        for char in text:
            print(char, end="", flush=True)
            time.sleep(self.anim_speed)
        print()

    # ---------------------------------------------------------
    # Utility: draw a horizontal rule
    # ---------------------------------------------------------
    def line(self):
        print("=" * 60)

    # ---------------------------------------------------------
    # Show a single reason with MathBlock
    # ---------------------------------------------------------
    def show_reason(self, symbol, reason, block):
        print(f"  {symbol} {reason}")
        print(f"      {block}")

    # ---------------------------------------------------------
    # Flip-card reveal for a force
    # ---------------------------------------------------------
    def reveal_force(self, word, force):
        sheet = self.reason_organ.get_sheet(word)
        if not sheet or force not in sheet:
            print("No data for this force.")
            return

        success = sheet[force]["success"]
        failure = sheet[force]["failure"]

        self.line()
        self.flicker(f" {force.upper()} — FLIP CARD ")
        self.line()

        # Casino-style random reveal
        for _ in range(10):
            r = random.choice(success + failure)
            print(f"  ▣ {r[0]}")
            time.sleep(0.05)

        self.line()
        print(" FINAL REVEAL")
        self.line()

        # Final chosen reason
        final = random.choice(success + failure)
        symbol = "✔" if final in success else "✖"
        self.show_reason(symbol, final[0], final[1])

    # ---------------------------------------------------------
    # Show full sheet for a word
    # ---------------------------------------------------------
    def show_sheet(self, word):
        sheet = self.reason_organ.get_sheet(word)
        if not sheet:
            print("No sheet found.")
            return

        self.line()
        self.flicker(f" REASON SHEET — {word.upper()} ")
        self.line()

        for force, groups in sheet.items():
            print(f"\n{force.upper()} (Success):")
            for reason, block in groups["success"]:
                self.show_reason("✔", reason, block)

            print(f"\n{force.upper()} (Failure):")
            for reason, block in groups["failure"]:
                self.show_reason("✖", reason, block)

        self.line()

    # ---------------------------------------------------------
    # Scroll through words
    # ---------------------------------------------------------
    def scroll(self, direction):
        if direction == "next":
            self.index = (self.index + 1) % len(self.words)
        else:
            self.index = (self.index - 1) % len(self.words)

        word = self.words[self.index]
        self.flicker(f"→ {word}")

    # ---------------------------------------------------------
    # Main interactive loop (optional)
    # ---------------------------------------------------------
    def run(self):
        print("Reason Viewer Active.")
        print("Commands: [n]ext, [p]rev, [s]heet, [f]orce, [q]uit")

        while True:
            cmd = input("> ").strip().lower()

            if cmd == "q":
                break

            elif cmd == "n":
                self.scroll("next")

            elif cmd == "p":
                self.scroll("prev")

            elif cmd == "s":
                self.show_sheet(self.words[self.index])

            elif cmd == "f":
                force = input("Force (spark/drift/echo/chaos/clarity/memory/pressure): ").strip().lower()
                self.reveal_force(self.words[self.index], force)
