def view_math_block(word, block):
    """
    Basic emoji viewer for a word + its math block.
    word: string
    block: dict with fields:
        - value (float)
        - packet (dict)
        - forces (dict)
        - resonance (list)
        - opposition (list)
    """

    print("\n" + "=" * 30)
    print("🔢 MATH BLOCK VIEWER")
    print("=" * 30 + "\n")

    # WORD
    print("📝 WORD")
    print(word)
    print()

    # BLOCK ID
    block_id = block.get("id", "unknown")
    print("🔗 ATTACHED MATH BLOCK")
    print(f"MB#{block_id}")
    print()

    # VALUE
    value = block.get("value", None)
    print("💠 VALUE")
    print(value)
    print()

    # PACKET
    print("📦 PACKET")
    packet = block.get("packet", {})
    for k, v in packet.items():
        print(f"• {k}: {v}")
    print()

    # FORCES
    print("⚡ FORCES")
    forces = block.get("forces", {})
    for k, v in forces.items():
        print(f"• {k}: {v}")
    print()

    # WORD RESONANCE
    print("❤️ WORD RESONANCE")
    for w in block.get("resonates_with", []):
        print(f"+ {w}")
    for w in block.get("opposes", []):
        print(f"- {w}")
    print()
