#
# Definiert die Details fuer den Level - wo das FOerderband liegt etc.
#

import cocos

class DefineLevel():

    def __init__(self):
        # tile size in tile map
        self.cell_size = 64

        # belt delay groesser als 1.5 gibt probleme (ist sowieso zu langsam)
        self.beltDelay = 0.1
        self.start = (0, 5)
        self.segments = [(10, 0), (0, 6), (-3, 0), (0, -3)]

        # Aussehen der Fabrik
        self.layer = 'TileLayer1'
        # x,y,w,h
#        self.storage_area = cocos.rect.Rect((self.start[0] - 1) * self.cell_size,
#                                            (self.start[1] - 1) * self.cell_size,
#                                            2 * self.cell_size, 3 * self.cell_size)

        # aufgaben, maschinen
        self.machines = [{'image' : 'img/yellow_machine.png', 'tool': 'img/piston.png', 'cost' : 15},
                         {'image' : 'img/red_machine.png', 'tool': 'img/red_piston.png', 'cost' : 20},
                         {'image' : 'img/green_machine.png', 'tool': 'img/piston.png', 'cost' : 25},
                         {'image' : 'img/machine.png', 'tool': 'img/piston.png', 'cost' : 30}]
        self.numMachines = len(self.machines)  # wie viele Maschinen

        # roh stoffe Kosten und Frequenz aufs Band
        self.material_cost = 0
        self.material_sendoff = 1