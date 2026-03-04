# pressures_organ.py
from organs.base_organ import BaseOrgan
from organs.base_force_source import BaseForceSource

class PressuresOrgan(BaseOrgan, BaseForceSource):
    def __init_subclass__(cls):
        BaseForceSource.registry.append(cls)

    def __init__(self, creature):
        self.creature = creature

    def get_forces(self):
        return {
            "symbolic": 0.2,
            "chaos": 0.05,
            "drift": 0.02,
            "source": "PressuresOrgan"
        }
