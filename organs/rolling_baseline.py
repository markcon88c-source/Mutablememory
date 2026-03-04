# organs/rolling_baseline.py
# Rolling baseline for EmergenceViewer — smooths noise over time

class RollingBaseline:
    def __init__(self, window=50):
        self.window = window
        self.values = []

    def update(self, value):
        """
        Add a new value to the rolling window.
        """
        try:
            v = float(value)
        except Exception:
            return

        self.values.append(v)
        if len(self.values) > self.window:
            self.values.pop(0)

    def get(self, *args, **kwargs):
        """
        EmergenceViewer may call get() with extra arguments.
        We ignore them and return the rolling average.
        """
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)
