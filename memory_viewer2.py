# memory_viewer2.py — Mythic Gradient + Story Viewer

def print_memory2(memory):
    print("\n🌈 MEMORY GRADIENT VIEWER (Story-Aware)")
    print("============================================================")

    # Show ascensions with mythic flavor
    if memory.promotions:
        print("\n🔥 TRANSITIONS")
        for msg in memory.promotions:
            # Story ascension detection
            if "Story" in msg:
                print(f"   📖 STORY SEED: {msg}")
            elif "Canon" in msg:
                print(f"   🕯️ CANON SHIFT: {msg}")
            elif "Archive" in msg:
                print(f"   🗃️ ARCHIVE ENTRY: {msg}")
            else:
                print(f"   ✨ {msg}")
        print("------------------------------------------------------------")

    # Display only levels that have items
    for idx, level in enumerate(memory.levels):
        if not level["items"]:
            continue

        level_name = level["name"]

        # Mythic glyphs for upper layers
        if level_name == "Canon":
            header = f"🕯️ L{idx+1}: {level_name}"
        elif level_name == "Archive":
            header = f"🗃️ L{idx+1}: {level_name}"
        elif level_name == "Story":
            header = f"📖 L{idx+1}: {level_name}"
        elif level_name == "Mythic":
            header = f"🔱 L{idx+1}: {level_name}"
        else:
            header = f"🔮 L{idx+1}: {level_name}"

        print(f"\n{header}")
        print("------------------------------------------------------------")

        for item in level["items"]:
            word = item["word"]
            gate = item["gate"]
            meaning = item["meaning_strength"]
            pol = item["polarity"]
            res = item["resonance"]

            # Movement glyphs
            if res > 0.15:
                motion = "🌱 rising"
            elif res < -0.15:
                motion = "🍂 falling"
            else:
                motion = "🌾 steady"

            # Polarity glyph
            if pol > 0.4:
                pol_glyph = "☀️"
            elif pol < -0.4:
                pol_glyph = "🌑"
            else:
                pol_glyph = "⚪"

            # Gate ring (circular progress)
            ring = _ring(gate)

            # Story layer special formatting
            if level_name == "Story":
                print(
                    f"   {ring}  {word:10}  ✍️ story-seed   "
                    f"meaning {meaning:.2f}  polarity {pol_glyph}"
                )
            else:
                print(
                    f"   {ring}  {word:10}  {motion:10}  "
                    f"meaning {meaning:.2f}  polarity {pol_glyph}"
                )

    print("============================================================\n")


def _ring(gate):
    """Circular gate progress indicator (17 gates → 8 segments)."""
    segments = int((gate / 17) * 8)
    return "◉" * segments + "○" * (8 - segments)
