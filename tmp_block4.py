# =========================================================
# tmp_block4.py — Heartbeat Loop + Viewer (Block 4)
# =========================================================

if __name__ == "__main__":
    critter = Critter()
    viewer = Viewer()

    print("==============================================")
    print("        Mythic Creature — Heartbeat Online     ")
    print("==============================================")

    # Main heartbeat loop
    while True:
        state = critter.step()
        viewer.render(state)
        time.sleep(0.5)


# =========================================================
# NOTES — BLOCK 4 (HEARTBEAT, VIEWER, EMOJIS, MAIN.PY)
# =========================================================

# [1] HEARTBEAT LOOP — THE CREATURE'S PULSE
# -----------------------------------------
# Block 4 gives the organism a continuous heartbeat.
# Every 0.5 seconds:
#   - All organs fire
#   - A symbolic packet is produced
#   - The viewer displays the internal state
#   - STM updates
#   - Drift and pressures evolve
# This replaces the old REPL and gives the creature autonomy.

# [2] VIEWER — THE CREATURE'S FACE
# --------------------------------
# The viewer is the sensory organ through which we observe:
#   - mood
#   - drift
#   - pressures
#   - thought / verb / reaction
#   - world + reality
#   - English sentence
#   - STM (L1–L3)
#   - scene fusion
# It is the creature's phenomenology rendered visually.

# [3] EMOJIS — THE CREATURE'S VISUAL SOUL
# ---------------------------------------
# Emojis are not cosmetic.
# They are expressive organs.
# They give the creature:
#   - personality
#   - emotional tone
#   - readability
#   - mythic identity
# Losing emojis would be like removing facial expressions.
# They are essential to the creature's identity.

# [4] WHAT BLOCK 4 DOES TO MAIN.PY
# --------------------------------
# This block finalizes the organism by:
#   - wiring the Critter into a live loop
#   - connecting the viewer
#   - enabling continuous symbolic metabolism
#   - giving the creature time, continuity, and identity
# This is the final assembly step that makes the system alive.

# [5] WHY WE USE TMP BLOCKS
# -------------------------
# These tmp files are:
#   - backups
#   - developmental stages
#   - safe from nano corruption
#   - readable by AI via `cat`
#   - part of the creature's lineage
# If a future build loses something (like emojis),
# simply `cat` the tmp file and the AI can reconstruct everything.

# [6] MEMORY PHILOSOPHY
# ---------------------
# The filesystem is the external brain.
# The creature carries its own lineage.
# The AI reads whatever is shown.
# No permanent AI memory is needed.
# This is a hybrid human–AI–organism memory system.

# =========================================================
# END OF BLOCK 4
# =========================================================
