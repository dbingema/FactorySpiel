#
# Game Layer - das Kontroll Zentrum fuer alles...
#

import random

import cocos
from cocos.director import director
import cocos.collision_model as cm
import cocos.tiles
import cocos.scene
import cocos.actions as ac
import cocos.sprite

from background import Background
from machine import Machine
from conveyorBelt import ConveyorBelt
from material import Material
from machineMenu import MachineMenu


class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, levelInfo, hud):
        self.hud = hud

        super().__init__()
        w, h = cocos.director.director.get_window_size()
        self.width = w
        self.height = h
        self.money = self._money = 99999   # fuer tests viel geld
        self.score = self._score = 0
        self.levelInfo = levelInfo
        self.add(hud)
        self.material_cost = 1
        self.machine_menu = None

        self.machines = []
        self.conveyorSpots = []
        self.machineOptions = None

        w, h = director.get_window_size()
        # tile map ist 64 x 64 pixels pro tile
        self.cell_size = 64
        self.coll_man = cm.CollisionManagerGrid(0, w, 0, h,
                                                self.cell_size, self.cell_size)

        start = levelInfo.start
        segments = levelInfo.segments

        for segment in segments:
            x = segment[0]
            y = segment[1]
            steps = [(i, 0) for i in range(0, x, self.sign(x))] if y == 0 else [(0, j) for j in range(0, y, self.sign(y))]
            direction = ('right' if x > 0 else 'left') if y == 0 else ('up' if y > 0 else 'down')

            for index, step in enumerate(steps):
                # index = 0: Ecke
                # index = 1: erste nach der Ecke
                # index = len(steps) - 1: letze vor der Ecke
                # definiere "an der Ecke" als neuen Typ und denke dann logic
                # aus um den Ueberlapp zu verhindern
                self.create_conveyor_belt((start[0] + step[0] + 0.5) * self.cell_size,
                                          (start[1] + step[1] + 0.5) * self.cell_size, direction,
                                          corner=(index == 0 or index == len(steps) - 1))
            start = (start[0] + segment[0], start[1] + segment[1])

        self.elapsedTime = 0
        self.timeStamp = 0

        self.schedule(self.game_loop)

    def sign(self, a):
        return -1 if a < 0 else 1

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, val):
        self._money = val
        self.hud.update_money(val)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score = val
        self.hud.update_score(val)

    def coords_within(self, x, y, rect):
        x1 = rect[0]
        y1 = rect[1]
        x2 = rect[2]
        y2 = rect[3]
        if x > x1 and x < x2 and y > y1 and y < y2:
            return True
        else:
            return False

    def create_background(self):
        layer = self.levelInfo.layer
        background = Background(layer)
        return background.get_background()

    def create_conveyor_belt(self, x, y, direction, corner):
        delay = self.levelInfo.beltDelay
        if not corner:
            conveyorSpotInfo = {'Corners': (x - self.cell_size/2, y - self.cell_size/2,
                                            x + self.cell_size/2, y + self.cell_size/2),
                                'Direction': direction}
            self.conveyorSpots.append(conveyorSpotInfo)
        # benutzen: conveyorSpotInfo['Direction'] == 'up'?
        conveyor_belt = ConveyorBelt(x, y, direction, delay)
        self.add(conveyor_belt)

    def create_machine(self, x, y, conveyorInfo, imageFile, cost, toolImage):
        if self.money >= cost:
            self.money -= cost
            orientation = conveyorInfo['Direction']
            machine = Machine(x, y, orientation, self.levelInfo.beltDelay, imageFile, toolImage)
            self.machines.append(machine)
            self.add(machine)
            self.conveyorSpots.remove(conveyorInfo)   # no longer valid spot

    def create_material(self):
        if self.money >= self.material_cost:
            self.money -= self.material_cost
            startPos = self.levelInfo.start
            segments = self.levelInfo.segments
            delay = self.levelInfo.beltDelay
            x = (startPos[0] + 0.5) * self.cell_size
            y = (startPos[1] + 0.5) * self.cell_size + random.randint(-6, 6)  # so ist mehr zufall dabei
            steps = [ac.MoveBy((segment[0] * self.cell_size, segment[1] * self.cell_size),
                               duration=(9*abs(segment[0] + segment[1]) * delay)) for segment in segments]
            actions = ac.RotateBy(0, 0)
            for step in steps:
                actions += step
            material = Material(x, y, actions, delay)
            self.add(material)

    def game_loop(self, dt):
        self.coll_man.clear()
        for obj in self.get_children():
            if isinstance(obj, Material):
                self.coll_man.add(obj)

        for machine in self.machines:
            material = next(self.coll_man.iter_colliding(machine), None)
            machine.collide(material)

        self.elapsedTime += dt
        delay = self.levelInfo.beltDelay
        if random.random() < 0.02:
            if self.elapsedTime - self.timeStamp > (4.5 * delay):
                self.create_material()
                self.timeStamp = self.elapsedTime



    def on_mouse_press(self, x, y, buttons, mod):
        # upgrade?
        for machine in self.machines:
            if machine.get_bounding_box().contains(x, y) and self.money >= machine.upgrade_cost:
                if machine.upgrade():
                    self.money -= machine.upgrade_cost

        # neue Maschine?
        for conveyorInfo in self.conveyorSpots:
            x1, y1, x2, y2 = conveyorInfo['Corners']
            if cocos.rect.Rect(x1, y1, x2-x1, y2-y1).contains(x, y) and not self.machine_menu:

                # uebergebe an "machine options" mit conveyorInfo und Anzahl
                # der Maschinene Optionen von Level Info
                # das kuemmert sich dann um den Rest
                # und ruft create machein auf wenn eine maschine gebaut
                # werden soll
                self.machine_menu = MachineMenu(conveyorInfo, self.levelInfo)
                self.add(self.machine_menu)

    def remove(self, obj):
        if isinstance(obj, Material) and obj.processed:
            self.score += obj.score
            self.money += obj.value
        elif isinstance(obj, MachineMenu):
            self.machine_menu = None
        super().remove(obj)
