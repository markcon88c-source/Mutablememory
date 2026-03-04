# base_force_source.py

class BaseForceSource:
    registry = []

    def get_forces(self):
        return {}
