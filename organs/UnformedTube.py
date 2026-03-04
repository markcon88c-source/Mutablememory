class UnformedTube:
    """
    Stores sentences or inputs that the creature refuses to form.
    """

    def __init__(self):
        self.buffer = []

    def add(self, raw_input, forces, stability):
        self.buffer.append({
            "input": raw_input,
            "forces": forces,
            "stability": stability
        })

    def get_all(self):
        return self.buffer
