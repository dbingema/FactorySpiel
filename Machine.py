#
# Die Maschine, ruft eine piston auf was aus den Rohstoffen die Produkte macht
#

import time

from pyglet.image import load, ImageGrid, Animation
import cocos

from actor import Actor
from tool import Tool


class Machine(Actor):

    def load_animation(self, imgage, delay):
        seq = ImageGrid(load(imgage), 1, 6)
        return Animation.from_image_sequence(seq, delay, loop=False)

    def __init__(self, x, y, conveyor_direction, delay, imageFile, toolImage):
        image = load(imageFile)

        # now create actual instance
        super().__init__(image, x, y)
        self.x, self.y = self.nearestSpot(x, y)
        self.delay = delay
        self.toolImage = toolImage
        self.conveyor_direction = conveyor_direction

        if conveyor_direction in ('up', 'down'):
            self.orientation = 'horizontal'
            self.rotation = 90
        else:
            self.orientation = 'vertical'

        # define collision box
        # increase size of collision box to hit sooner
        # when conveyor belt is faster
        self.cshape.r = 0.25 / self.delay
        self.target = None

        # define timer for cool down period
        self.lastStamp = time.perf_counter()
        self.cooldown = 2.0
        self.upgrade_cost = 10
        self.upgrade_level = 0

        # starte druck aufbau
        self.reload_animation = None
        self.begin_reload()

        # so that machines are created in actual spots
    def nearestSpot(self, x, y):
        new_x = round((x - 16) / 32) * 32 + 16
        new_y = round((y - 16) / 32) * 32 + 16
        return new_x, new_y

    def get_bounding_box(self):
        # original breite hoehe
        w, h = self.width, self.height
        if self.orientation == 'horizontal':
            w, h = h, w
        return cocos.rect.Rect(self.x - w/2, self.y - h/2, w, h)

    # make sure material is in a valid position
    # (in front and not behind the machine)
    def can_hit(self, material):
        if self.conveyor_direction == 'up':
            if material and material.y < self.y:
                return True
        if self.conveyor_direction == 'down':
            if material and material.y > self.y:
                return True
        if self.conveyor_direction == 'right':
            if material and material.x < self.x:
                return True
        if self.conveyor_direction == 'left':
            if material and material.x > self.x:
                return True

    def stamp(self):
        # if collision then:
        # create piston
        if self.target is not None:
            if not self.target.processed:
                if time.perf_counter() > self.lastStamp + self.cooldown:
                    self.parent.add(Tool(self.x, self.y, self.orientation,
                                         self.target, self, self.delay, self.toolImage))
                    self.target = None

    def collide(self, material):
        if self.can_hit(material):
            self.target = material
            self.stamp()

    def begin_reload(self):
        if self.reload_animation is not None:
            self.remove(self.reload_animation)
        self.lastStamp = time.perf_counter()
        # animation neu starten - ended von alleine
        animation = self.load_animation('img/machineReload.png',
                                        self.cooldown / 5)

        # punkte oben drauf legen
        self.reload_animation = cocos.sprite.Sprite(animation)
        self.add(self.reload_animation)

    def upgrade(self):
        if self.upgrade_level == 0:
            # noch kein upgrade bislang
            self.cooldown = 1.0
            self.upgrade_level = 1
            upgrade_image = cocos.sprite.Sprite('img/upgrade.png', (0, 0), opacity=200)
            self.add(upgrade_image)
            return True
        else:
            # bei max level - nix tun
            return False
