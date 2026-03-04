# main_support/five_stack_viewer.py

import sys
import json

def smooth_clear():
    sys.stdout.write("\033[2J\033[H")  # safer for Termux than alt buffer
    sys.stdout.flush()

def pretty(obj):
    if isinstance(obj, dict):
        return json.dumps(obj, indent=2)
    return str(obj)

def render(packet):
    smooth_clear()

    print(f"Iteration: {packet.get('router', {}).get('iteration', '?')}\n")

    print("=== SENTENCE METABOLIC VIEWER ===")
    print(pretty(packet.get("english_field") or packet.get("sentence") or "(no sentence)"))
    print()

    print("=== LANGUAGE VIEWER ===")
    print(pretty(packet.get("language", "(no language)")))
    print()

    print("=== NARRATIVE VIEWER ===")
    story = packet.get("story")
    print(pretty(story.get("event") if story else "(no story)"))
    print()

    print("=== BRUSH-UP VIEWER ===")
    print(pretty(packet.get("brushup", "(no brushup)")))
    print()

    print("=== EMERGENCE VIEWER ===")
    print(pretty(packet.get("emergence", "(no emergence)")))
    print()
