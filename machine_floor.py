class MachineFloor:
    def __init__(self):
        self.machines = {}
        self.positions = {}

    def add_machine(self, name, machine, position=None):
        self.machines[name] = machine
        self.positions[name] = position
        machine.dock(self)

    def move_machine(self, name, new_position):
        if name in self.machines:
            self.positions[name] = new_position
            self.machines[name].move_to(new_position)

    def turn_on(self, name):
        if name in self.machines:
            self.machines[name].turn_on()

    def turn_off(self, name):
        if name in self.machines:
            self.machines[name].turn_off()

    def run_all(self):
        for machine in self.machines.values():
            machine.run()
