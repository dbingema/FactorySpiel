#
# Definiert die Details fuer den Level - wo das FOerderband liegt etc.
#


class DefineLevel():

    def __init__(self):
        self.start = (0, 5)
        self.segments = [(20, 0)] #, (0, 8), (-3, 0), (0, -3)]
        self.layer = 'TileLayer1'
        # belt delay groesser als 1.5 gibt probleme (ist sowieso zu langsam)
        self.beltDelay = 0.1
        self.machines = ['img/machine.png']
        self.numMachines = len(self.machines)  # eine Maschine
