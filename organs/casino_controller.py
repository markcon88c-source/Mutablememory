# organs/casino_controller.py

import time
from organs.casino_force_core import CasinoForceCore
from organs.casino_viewer import CasinoViewer

class CasinoController:
    def __init__(self, seed=None):
        self.core = CasinoForceCore(seed=seed)
        self.viewer = CasinoViewer()

    def spin(self):
        result = self.core.spin()
        self.viewer.show_spin(result)
        return result

    def auto(self, delay=3.5):
        """
        Infinite auto-spin loop.
        Spins every `delay` seconds.
        Stops cleanly with CTRL+C.
        """
        print("\n🎰 AUTO-SPIN MODE — Press CTRL+C to stop\n")
        try:
            while True:
                result = self.core.spin()
                self.viewer.show_spin(result)
                time.sleep(delay)
        except KeyboardInterrupt:
            print("\n🛑 Auto-spin stopped.\n")
