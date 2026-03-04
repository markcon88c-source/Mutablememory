# organs/noise_baseline.py
# Simple noise baseline organ for EmergenceViewer

class NoiseBaseline:
    def __init__(self, initial_value=0.0):
        self.value = float(initial_value)

    def update(self, sample):
        """
        Optionally update baseline from a new noise sample.
        """
        try:
            self.value = float(sample)
        except Exception:
            pass

    def get(self, *args, **kwargs):
        """
        EmergenceViewer may call get() with extra arguments.
        We ignore them and return the baseline.
        """
        return self.value
