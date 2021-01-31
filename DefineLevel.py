#
# Definiert die Details fuer den Level - wo das FOerderband liegt etc.
#


class DefineLevel(object):
    def __init__(self):
        self.start = (0, 5)
        self.segments = [(20, 0)]#, (0, 8), (-3, 0), (0, -3)]
        self.layer = 'TileLayer1'
        self.beltDelay = 0.1 # groesser als 1.5 gibt probleme (ist sowieso zu langsam)
        self.machines = ['img/machine.png']
        self.numMachines = len(self.machines)  # eine Maschine
        


