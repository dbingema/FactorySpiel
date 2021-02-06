#
# wen gecklickt sollen 10 / 50 / 100 materialen gekauft werden
#

# kreiert die Materialien und zieht das Geld ab 
# und schickt sie dann unregelmaessig aufs band

import random

from material import Material

import cocos.actions as ac
import cocos




class Storage(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, levelInfo):
        super().__init__()
        self.levelInfo = levelInfo

        # liste der kreierten materialein
        self.materials = []
        self.materials_on_click = 10
        self.cell_size = self.levelInfo.cell_size


    def create_moving_material(self):
        # ein neues Material kreieren und ins Lager legen
        startPos = self.levelInfo.start
        segments = self.levelInfo.segments
        delay = self.levelInfo.beltDelay
        x = (startPos[0] + 0.5) * self.cell_size
        y = (startPos[1] + 0.5) * self.cell_size + random.randint(-5, 5)  # so ist mehr zufall dabei
        steps = [ac.MoveBy((segment[0] * self.cell_size, segment[1] * self.cell_size),
                        duration=(9*abs(segment[0] + segment[1]) * delay)) for segment in segments]
        actions = ac.RotateBy(0, 0)
        for step in steps:
            actions += step
        material = Material(x, y, actions, delay)
        self.parent.add(material) # gamelayer sollte es dazu addieren

    def send_material(self):
        # wird von game_layer aufgerufen
        # falls genug im Lager, einen aufs band legen
        if len(self.materials) > 0:
            # ein dumm rum liegendes material killen
            material = self.materials.pop()
            self.remove(material)
            # ein neues material mit actions machen und dem game layer uebergeben
            self.create_moving_material()
    
    def fill_up_storage(self):
        # lager auffuellen
        if genug geld:
            action = None
            delay = 0
            for index in range(self.materials_on_click):
                x, y = bisschen random # todo: hier felht noch was...
                material = Material(x, y, action, delay)
                self.materials.append(material)
                self.add(material)

    def on_mouse_press(self, x, y, buttons, mod):
        if self.levelInfo.storage_area.contains(x, y):
            self.fill_up_storage()





