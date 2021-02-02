#
# Definiert die Details fuer den Level - wo das FOerderband liegt etc.
#


class DefineLevel():

    def __init__(self):
        self.start = (0, 5)
        self.segments = [(10, 0), (0, 8), (-3, 0), (0, -3)]
        self.layer = 'TileLayer1'
        # belt delay groesser als 1.5 gibt probleme (ist sowieso zu langsam)
        self.beltDelay = 0.1
        self.machines = [{'image' : 'img/yellow_machine.png', 'tool': 'img/piston.png', 'cost' : 15},
                         {'image' : 'img/red_machine.png', 'tool': 'img/red_piston.png', 'cost' : 20},
                         {'image' : 'img/green_machine.png', 'tool': 'img/piston.png', 'cost' : 25},
                         {'image' : 'img/machine.png', 'tool': 'img/piston.png', 'cost' : 30}]
        self.numMachines = len(self.machines)  # wie viele Maschinen
