
# memory_viewer.py — expressive, mythic-safe memory viewer

def print_memory(memory):
    print("\n🧠 MEMORY SPINE")
    print("============================================================")

    # Show ascensions first
    if memory.promotions:
        print("\n🌟 ASCENSIONS")
        for msg in memory.promotions:
            print(f"   {msg}")
        print("------------------------------------------------------------")

    # Display each L-level
    for idx, level in enumerate(memory.levels):
        level_name = level["name"]
        print(f"\n📚 L{idx+1}: {level_name}")
        print("------------------------------------------------------------")

        if not level["items"]:
            print("   (no items)")
            continue

        for item in level["items"]:
            word = item["word"]
            gate = item["gate"]
            meaning = item["meaning_strength"]
            pol = item["polarity"]
            res = item["resonance"]

            # Movement arrow
            if res > 0.15:
                arrow = "↑"
            elif res < -0.15:
                arrow = "↓"
            else:
                arrow = "→"

            # Polarity sign
            pol_sign = "+" if pol >= 0 else "-"

            # Star bar (10 stars representing 17 gates)
            star_count = int((gate / 17) * 10)
            stars = "⭐" * star_count + "░" * (10 - star_count)

            # Final line
            print(
                f"   {word:10} {arrow}  L{idx+1}.{gate:02}   "
                f"{stars}   meaning {meaning:.2f}   pol {pol_sign}{abs(pol):.2f}"
            )

    print("============================================================\n")
