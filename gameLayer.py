#
# Game Layer - das Kontrolle Zentrum fuer alles...
#

import random

import cocos
from cocos.director import director
import cocos.collision_model as cm
import cocos.tiles
import cocos.scene
import cocos.sprite
import cocos.actions as ac

from background import Background
from machine import Machine
from conveyorBelt import ConveyorBelt
from material import Material
from machineMenu import MachineMenu
# from storage import Storage

# helper functions
from helpers import *


class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, level_info, hud):
        self.hud = hud
        self.level_info = level_info

        # mache das lager
#        self.storage = Storage(self.level_info)

        super().__init__()
        w, h = cocos.director.director.get_window_size()
        self.width = w
        self.height = h
        self.money = self._money = 99999   # fuer tests viel geld
        self.score = self._score = 0
        self.add(hud)
        self.material_cost = self.level_info.material_cost
        self.machine_menu = None

        # wie oft ein material los geschickt wird
        self.material_sendoff = self.level_info.material_sendoff

        self.machines = []
        self.conveyor_belts = []
        self.machine_options = None

        w, h = director.get_window_size()
        # tile map ist 64 x 64 pixels pro tile
        self.cell_size = self.level_info.cell_size
        self.coll_man = cm.CollisionManagerGrid(0, w, 0, h,
                                                self.cell_size, self.cell_size)

        start = level_info.start
        segments = level_info.segments

        for segment in segments:
            x = segment[0]
            y = segment[1]
            steps = [(i, 0) for i in range(0, x, self.sign(x))] if y == 0 else \
                    [(0, j) for j in range(0, y, self.sign(y))]
            direction = ('right' if x > 0 else 'left') if y == 0 else ('up' if y > 0 else 'down')

            for step in steps:
                self.create_conveyor_belt((start[0] + step[0] + 0.5) * self.cell_size,
                                          (start[1] + step[1] + 0.5) * self.cell_size, direction)
            start = (start[0] + segment[0], start[1] + segment[1])

        self.elapsedTime = 0

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

    def create_background(self):
        layer = self.level_info.layer
        background = Background(layer)
        return background.get_background()

    def create_conveyor_belt(self, x, y, direction):
        delay = self.level_info.beltDelay
        conveyor_belt = ConveyorBelt(x, y, direction, delay)
        self.conveyor_belts.append(conveyor_belt)
        self.add(conveyor_belt)

    def create_machine(self, x, y, image_file, cost, tool_image):
        if self.money >= cost:
            self.money -= cost
            machine = Machine(x, y, self.level_info.beltDelay, image_file, tool_image)
            self.machines.append(machine)
            self.add(machine)

    def create_material(self):
        # ein neues Material kreieren und ins Lager legen
        start_pos = self.level_info.start
        segments = self.level_info.segments
        delay = self.level_info.beltDelay
        x = (start_pos[0] + 0.5) * self.cell_size
        y = (start_pos[1] + 0.5) * self.cell_size + random.randint(-5, 5)  # so ist mehr zufall dabei
        steps = [ac.MoveBy((segment[0] * self.cell_size, segment[1] * self.cell_size),
                           duration=(9*abs(segment[0] + segment[1]) * delay)) for segment in segments]
        actions = ac.RotateBy(0, 0)
        for step in steps:
            actions += step
        material = Material(x, y, actions, delay)
        self.add(material)  # gamelayer sollte es dazu addieren

    def game_loop(self, dt):
        self.coll_man.clear()
        for obj in self.get_children():
            if isinstance(obj, Material):
                if not obj.processed:
                    self.coll_man.add(obj)

        for machine in self.machines:
            material = next(self.coll_man.iter_colliding(machine), None)
            materials = self.coll_man.iter_colliding(machine)
            print(materials)
            if material is not None:
                machine.collide(material)

        self.elapsedTime += dt
#        delay = self.levelInfo.beltDelay
# kein zufall, sondern regelmaessig
#        if random.random() < 0.02:
        if self.elapsedTime > self.material_sendoff:
            self.elapsedTime = 0
#           if self.elapsedTime - self.timeStamp > (4.5 * delay):
            self.create_material()
#           self.storage.send_material()
#               self.timeStamp = self.elapsedTime

    #

    def on_mouse_press(self, x, y, buttons, mod):
        # upgrade?
        for machine in self.machines:         
            if get_bounding_box(machine).contains(x, y) and self.money >= machine.upgrade_cost:
                if machine.upgrade():
                    self.money -= machine.upgrade_cost

        # neue Maschine?
        # wo hat man hin geclickt?
        # etwa auf eine Maschine? Oder ein Fliessband?
        # Dann nix tun
        clicked_any_objects = [get_bounding_box(obj).contains(x, y) for obj in self.machines + self.conveyor_belts]

        if not any(clicked_any_objects):
            new_machine_pos = get_tile_center(x, y)
            self.machine_menu = MachineMenu(new_machine_pos, self.level_info)
            self.add(self.machine_menu)

    def remove(self, obj):
        if isinstance(obj, Material) and obj.processed:
            self.score += obj.score
            self.money += obj.value
        elif isinstance(obj, MachineMenu):
            self.machine_menu = None
        super().remove(obj)
