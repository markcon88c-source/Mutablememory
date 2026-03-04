# organs/heart.py

import time
import random

class HeartOrgan:
    """
    The HeartOrgan provides heartbeat timing, packet generation,
    and a stable pulse for the creature's internal clocks.
    """

    def __init__(self, bpm=60):
        self.bpm = bpm
        self.last_beat_time = time.time()
        self.last_packet = None

    def set_bpm(self, bpm):
        """Update the heart rate."""
        self.bpm = bpm

    def beat_due(self):
        """
        Returns True if enough time has passed for the next heartbeat.
        """
        interval = 60.0 / max(self.bpm, 1)
        now = time.time()
        return (now - self.last_beat_time) >= interval

    def beat(self):
        """
        Perform a heartbeat: update the timestamp and generate a packet.
        """
        self.last_beat_time = time.time()
        self.last_packet = self.generate_packet()
        return self.last_packet

    def generate_packet(self):
        """
        Heartbeat packet: a simple pulse with a random jitter value.
        """
        return {
            "pulse": 1,
            "jitter": random.uniform(-0.05, 0.05),
            "timestamp": time.time()
        }

    def get_last_packet(self):
        """
        Return the last generated heartbeat packet.
        """
        return self.last_packet
