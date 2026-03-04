#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========== ANSI + EMOJI BRUSH-UP VIEWER ==========

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"

# 256-color foreground
def fg(code: int) -> str:
    return f"\x1b[38;5;{code}m"

# Story-type → base color + emoji
STORY_TYPES = {
    "mythic":  {"color": 208, "emoji": "🪨"},
    "forest":  {"color": 34,  "emoji": "🌲"},
    "dream":   {"color": 99,  "emoji": "💜"},
    "song":    {"color": 51,  "emoji": "🌀"},
    "river":   {"color": 33,  "emoji": "🌊"},
    "symbol":  {"color": 244, "emoji": "⚪"},
    "system":  {"color": 250, "emoji": "💻"},
}

# Force → color
FORCE_COLORS = {
    "drift":      33,   # blue
    "resonance":  51,   # cyan
    "stability":  208,  # orange
    "memory":     99,   # purple
    "chaos":      196,  # red
}

def style_word(word: str, story_type: str, force: float) -> str:
    """Color + bold/dim a word based on story-type + force intensity."""
    st = STORY_TYPES.get(story_type, STORY_TYPES["system"])
    color = fg(st["color"])
    if force >= 0.75:
        return f"{st['emoji']} {BOLD}{color}{word}{RESET}"
    elif force <= 0.40:
        return f"{st['emoji']} {DIM}{color}{word}{RESET}"
    else:
        return f"{st['emoji']} {color}{word}{RESET}"

def bar(name: str, force_name: str, value: float, width: int = 14) -> str:
    """Mini force bar."""
    blocks = int(round(value * width))
    color = fg(FORCE_COLORS[force_name])
    bar_str = color + ("█" * blocks or " ") + RESET
    return f"{name:<11} {bar_str}"

def render_brushup_cycle(cycle: dict) -> None:
    """
    cycle = {
      "chosen": {"word": "stone", "story_type": "mythic", "force": 0.91},
      "candidates": [
          {"word": "forest", "story_type": "forest", "force": 0.42},
          {"word": "echo",   "story_type": "song",   "force": 0.37},
          {"word": "river",  "story_type": "river",  "force": 0.55},
      ],
      "forces": {
          "drift": 0.45,
          "resonance": 0.82,
          "stability": 0.93,
          "memory": 0.38,
          "chaos": 0.06,
      },
      "sentence": {
          "text": "echo ignites stone",
          "leaning": {
              "mythic": 0.68,
              "forest": 0.41,
              "dream": 0.22,
          }
      },
      "source_bucket": {
          "story_type": "mythic",
          "words": ["stone", "spark", "shadow", "feather", "key", "blade", "flame"]
      }
    }
    """
    chosen = cycle["chosen"]
    candidates = cycle["candidates"]
    forces = cycle["forces"]
    sentence = cycle["sentence"]
    source = cycle["source_bucket"]

    # ---------- TICKER ----------
    print()
    print(f"{BOLD}[BRUSH-UP]{RESET} chosen:", end=" ")
    print(style_word(chosen["word"], chosen["story_type"], chosen["force"]))
    print("vs ", end="")
    cand_strs = []
    for c in candidates:
        cand_strs.append(style_word(c["word"], c["story_type"], c["force"]))
    print(", ".join(cand_strs))
    print()

    # ---------- FORCE MINI-GRAPHS ----------
    print("⚡ Forces")
    print("──────────────")
    print(bar("Drift:", "drift", forces["drift"]))
    print(bar("Resonance:", "resonance", forces["resonance"]))
    print(bar("Stability:", "stability", forces["stability"]))
    print(bar("Memory:", "memory", forces["memory"]))
    print(bar("Chaos:", "chaos", forces["chaos"]))
    print()

    # ---------- SENTENCE CONTEXT ----------
    print("🧩 Sentence")
    print("──────────────")
    print(f"Text: {sentence['text']}")
    # dominant leaning
    leaning = sentence["leaning"]
    dominant_type = max(leaning, key=leaning.get)
    dom_val = leaning[dominant_type]
    dom_st = STORY_TYPES.get(dominant_type, STORY_TYPES["system"])
    dom_color = fg(dom_st["color"])
    parts = []
    for st_name, val in leaning.items():
        st = STORY_TYPES.get(st_name, STORY_TYPES["system"])
        color = fg(st["color"])
        if st_name == dominant_type:
            parts.append(f"{BOLD}{color}{st_name}({val:.2f}){RESET}")
        else:
            parts.append(f"{color}{st_name}({val:.2f}){RESET}")
    print("Story-type leaning:", ", ".join(parts))
    print()

    # ---------- SOURCE BUCKET ----------
    st_name = source["story_type"]
    st = STORY_TYPES.get(st_name, STORY_TYPES["system"])
    header_color = fg(st["color"])
    print(f"📖 SOURCE BUCKET: {header_color}{st_name.upper()}{RESET}")
    print("────────────────────────────────────────────")
    for w in source["words"]:
        # fake a mid force for display; you’ll plug real forces here
        print(" ", style_word(w, st_name, 0.6))
    print()


if __name__ == "__main__":
    # demo cycle
    demo_cycle = {
        "chosen": {"word": "stone", "story_type": "mythic", "force": 0.91},
        "candidates": [
            {"word": "forest", "story_type": "forest", "force": 0.42},
            {"word": "echo",   "story_type": "song",   "force": 0.37},
            {"word": "river",  "story_type": "river",  "force": 0.55},
        ],
        "forces": {
            "drift": 0.45,
            "resonance": 0.82,
            "stability": 0.93,
            "memory": 0.38,
            "chaos": 0.06,
        },
        "sentence": {
            "text": "echo ignites stone",
            "leaning": {
                "mythic": 0.68,
                "forest": 0.41,
                "dream": 0.22,
            }
        },
        "source_bucket": {
            "story_type": "mythic",
            "words": ["stone", "spark", "shadow", "feather", "key", "blade", "flame"]
        }
    }

    render_brushup_cycle(demo_cycle)
