#
# Die Maschine, ruft eine piston auf was aus den Rohstoffen die Produkte macht
#

import time
import math

from pyglet.image import load, ImageGrid, Animation
import cocos

from actor import Actor
from tool import Tool


class Machine(Actor):

    def load_animation(self, imgage, delay):
        seq = ImageGrid(load(imgage), 1, 6)
        return Animation.from_image_sequence(seq, delay, loop=False)

    def __init__(self, x, y, delay, image_file, tool_image):
        image = load(image_file)

        # now create actual instance
        super().__init__(image, x, y)
        self.delay = delay
        self.toolImage = tool_image

        # define collision box
        # increase size of collision box to hit sooner
        # when conveyor belt is faster
        # self.cshape.r = 0.25 / self.delay
        self.cshape.r = 128
        self.target = None

        # define timer for cool down period
        self.last_stamp = time.perf_counter()
        self.cooldown = 2.0
        self.upgrade_cost = 10
        self.upgrade_level = 0
        self.stamping = False

        # starte druck aufbau
        self.reload_animation = None
        self.begin_reload()

    def stamp(self):
        # if collision then:
        # create piston
        if self.target is not None:
            if not self.target.processed:
                if time.perf_counter() > self.last_stamp + self.cooldown:
                    # distance = math.sqrt((self.x - self.target.x)**2 + (self.y - self.target.y)**2)
                    # if distance < self.hit_distance:
                    self.add(Tool(0, -32, self.target, self, self.delay, self.toolImage))
                    # reset last stamp so dass er nicht drauf haut waerend es eine piston schon gibt
                    self.stamping = True

    def collide(self, material):
        if self.target is None:
            self.target = material
        else:
            if self.target.processed:
                self.target = material
            else:
                distance = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
                if distance > self.cshape.r:
                    self.target = material

        if not self.stamping:
            x, y = self.target.x - self.x, self.target.y - self.y
            angle = -math.atan2(y, x)
            self.rotation = math.degrees(angle) - 95
            self.stamp()

    def begin_reload(self):
        self.stamping = False
        if self.reload_animation is not None:
            self.remove(self.reload_animation)
        self.last_stamp = time.perf_counter()
        # animation neu starten - ended von alleine
        animation = self.load_animation('img/machineReload.png', self.cooldown / 5)
        # punkte oben drauf legen
        self.reload_animation = cocos.sprite.Sprite(animation)
        self.add(self.reload_animation)
        self.target = None

    def set_cooldown(self, val):
        self.cooldown = val
        self.begin_reload()

    def upgrade(self):
        if self.upgrade_level == 0:
            # noch kein upgrade bislang
            self.set_cooldown(1)
            self.upgrade_level = 1
            upgrade_image = cocos.sprite.Sprite('img/upgrade.png', (0, 0), opacity=200)
            self.add(upgrade_image)
            return True
        else:
            # bei max level - nix tun
            return False
