# ============================================================
# EXECUTIVE ORGAN — HEARTBEAT + FRAME COMPOSITOR + STORM BURST
# ============================================================

import time
import threading

class ExecutiveOrgan:
    def __init__(self, creature, heartbeat_interval=0.25):
        self.creature = creature
        self.heartbeat_interval = heartbeat_interval

        # Packet buffer for storm burst (medium = this heartbeat only)
        self.packet_buffer = []

        # Frame fence
        self.frame_ready = False

        # Thread control
        self.running = False
        self.thread = None

    # ------------------------------------------------------------
    # Called by viewers to submit raw packets for the storm burst
    # ------------------------------------------------------------
    def submit_packet(self, text):
        if text:
            self.packet_buffer.append(text)

    # ------------------------------------------------------------
    # Start the heartbeat loop
    # ------------------------------------------------------------
    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    # ------------------------------------------------------------
    # Stop the heartbeat loop
    # ------------------------------------------------------------
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    # ------------------------------------------------------------
    # Main heartbeat loop
    # ------------------------------------------------------------
    def loop(self):
        while self.running:
            start = time.time()

            # Tick all organs
            self.creature.tick_all()

            # Mark frame ready
            self.frame_ready = True

            # Render one clean frame
            self.render_frame()

            # Render storm burst
            self.render_storm()

            # Reset for next heartbeat
            self.packet_buffer = []
            self.frame_ready = False

            # Maintain heartbeat interval
            elapsed = time.time() - start
            remaining = self.heartbeat_interval - elapsed
            if remaining > 0:
                time.sleep(remaining)

    # ------------------------------------------------------------
    # Render the clean cinematic frame
    # ------------------------------------------------------------
    def render_frame(self):
        if not self.frame_ready:
            return

        # STREAMING LINE
        stream_line = self.creature.sentence_viewer.render_stream()
        if stream_line:
            print(stream_line)

        # HUD
        hud = self.creature.sentence_viewer.render_hud()
        if hud:
            print(hud)

    # ------------------------------------------------------------
    # Render the storm burst (raw packets from this heartbeat)
    # ------------------------------------------------------------
    def render_storm(self):
        if not self.packet_buffer:
            return

        print("\n--- Storm Burst ---")
        for pkt in self.packet_buffer:
            print(pkt)
        print("--- End Storm ---\n")
