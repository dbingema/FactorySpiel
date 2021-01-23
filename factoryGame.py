#Was wir als naechstes machen sollen:
# tips / tutorial
# Geld System / transport

# Machine:
# - upgrades (viel spaeter)
# - vielleicht ein bisschen groesser machen?

# hier noch ein Kommentar...
# different test line

# import sys, os
import time
import random


from pyglet.image import load, ImageGrid, Animation
import pyglet.resource

import cocos
from cocos.director import director
import cocos.tiles
import cocos.scene
import cocos.actions as ac
import cocos.sprite
import cocos.euclid as eu

import cocos.collision_model as cm



class Background(cocos.layer.Layer):

    def __init__(self, layer):
        super(Background, self).__init__()
        tmx_map = cocos.tiles.load('img/factoryMap.tmx')
        self.bg = tmx_map[layer]
        self.bg.set_view(0,0, 640, 480)

    def get_background(self):
        return self.bg


class Actor(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Actor, self).__init__(image)
        self.position = eu.Vector2(x, y)
        self._cshape = cm.CircleShape(self.position, self.width * 0.25)

    @property
    def cshape(self):
        self._cshape.center = eu.Vector2(self.x, self.y)
        return self._cshape




class ConveyorBelt(Actor):

    def load_animation(self, imgage, delay):
        seq = ImageGrid(load(imgage), 4, 1)
        return Animation.from_image_sequence(seq, delay)

    def __init__(self, x, y, direction, delay):
        animation = self.load_animation('img/conveyorBelt.png', delay)

        # depending on direction, rotate image accordingly
        if direction == 'right':
            animation = animation.get_transform(rotate=0)
        if direction == 'left':
            animation = animation.get_transform(rotate=180)
        if direction == 'down':
            animation = animation.get_transform(rotate=90)
        if direction == 'up':
            animation = animation.get_transform(rotate=270)

        # now create actual instance
        super(ConveyorBelt, self).__init__(animation, x, y)




class Machine(Actor):

    def load_animation(self, imgage, delay):
        seq = ImageGrid(load(imgage), 1, 5)
        return Animation.from_image_sequence(seq, delay, loop=False)

    def __init__(self, x, y, conveyor_direction, delay):
        image = load('img/machine.png')
        self.delay = delay
        self.conveyor_direction = conveyor_direction

        # now create actual instance
        super(Machine, self).__init__(image, x, y)
        self.x, self.y = self.nearestSpot(x, y)


        # define collision box
        # increase size of collision box to hit sooner when conveyor belt is faster
        self.cshape.r = 0.25 / self.delay
        self.target = None

        # define timer for cool down period
        self.lastStamp = time.perf_counter()
        self.cooldown = 2.0

        #starte druck aufbau
        self.begin_reload()

        #so that machines are created in actual spots
    def nearestSpot(self, x, y):
        new_x = round((x - 16) / 32) * 32 + 16
        new_y = round((y - 16) / 32) * 32 + 16
        return new_x, new_y

     # make sure material is in a valid position (in front and not behind the machine)
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
                if (time.perf_counter() > self.lastStamp + self.cooldown):
                    self.parent.add(Piston(self.x, self.y,self.orientation, self.target, self, self.delay))
                    self.target = None

    def collide(self, material):
        if self.can_hit(material):
          self.target = material
          self.stamp()

    def begin_reload(self):
        self.lastStamp = time.perf_counter()
        # animation neu starten - ended von alleine
        animation = self.load_animation('img/machineReload.png', self.cooldown / 4)

        if self.conveyor_direction == 'up' or self.conveyor_direction == 'down':
            self.orientation = 'horizontal'
            animation = animation.get_transform(rotate=90)
        else:
            self.orientation = 'vertical'
            # self.rotation= 0 (default)

        self.image = animation


class Piston(cocos.sprite.Sprite):

    def load_animation(self, imgage, delay):
        seq = ImageGrid(load(imgage), 1, self.numFrames)
        return Animation.from_image_sequence(seq, delay, loop=False)

    def __init__(self, x, y, orientation, target, machine, delay):
        self.delay = delay / 2.38 #using universal delay calculate animation speed accordingly
        self.numFrames = 7
        self.target = target
        self.machine = machine
        animation = self.load_animation('img/piston.png', self.delay)

        # depending on direction, rotate image accordingly
        if orientation == 'horizontal':
            animation = animation.get_transform(rotate=90)

        # now create actual instance
        pos = eu.Vector2(x, y)
        super(Piston, self).__init__(animation, pos)

        self.do(ac.CallFunc(self.target.replace) +
                ac.Delay(self.numFrames * self.delay) +
                ac.CallFunc(self.machine.begin_reload) +
                ac.CallFunc(self.kill))

class Material(Actor):
    def __init__(self, x, y, actions, delay):
        super(Material, self).__init__('img/rawMaterial.png', x, y)
        self.x = x
        self.y = y
        self.processed = False
        self.cshape.r = 3
        self.value = 5
        self.score = 10
        self.delay = delay

        self.do(actions + ac.CallFunc(self.transport))

    def replace(self):
        self.do(ac.Delay(0.15) + ac.CallFunc(self.load_product))
        self.processed = True

    def load_product(self):
        self.image = load('img/chair3D.png')

    def transport(self):
        self.kill()
        # fahrrad kommt zum abholen



class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, levelInfo, hud):
        self.hud = hud

        super(GameLayer, self).__init__()
        w, h = cocos.director.director.get_window_size()
        self.width = w
        self.height = h
        self.money = self._money = 99999 #fuer tests viel geld
        self.score = self._score = 0
        self.levelInfo = levelInfo
        self.add(hud)
        self.machine_cost = 20
        self.material_cost = 1

        self.machines = []

        self.conveyorSpots = []

        w, h = director.get_window_size()
        cell_size = 32
        self.coll_man = cm.CollisionManagerGrid(0, w, 0, h, cell_size, cell_size)

        start = levelInfo.start
        segments = levelInfo.segments
        sign = lambda a: -1 if a < 0 else 1

        for segment in segments:
            x = segment[0]
            y = segment[1]
            steps = [(i,0) for i in range(0,x,sign(x))] if y == 0 else [(0,j) for j in range(0,y,sign(y))]
            direction = ('right' if x > 0 else 'left') if y == 0 else ('up' if y > 0 else 'down')

            for index, step in enumerate(steps):
                # index = 0: Ecke
                # index = 1: erste nach der Ecke
                # index = len(steps) - 1: letze vor der Ecke
                # definiere "an der Ecke" als neuen Typ und denke dann logic aus um den Ueberlapp zu verhindern
                self.create_conveyor_belt((start[0] + step[0] + 0.5) * 32,
                                        (start[1] + step [1] + 0.5) * 32, direction,
                                        corner = (index == 0 or index == 1 or index == len(steps) - 1) )
            start = (start[0] + segment[0], start[1] + segment[1])


        self.elapsedTime = 0
        self.timeStamp = 0

        self.schedule(self.game_loop)

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, val):
        self._money = val
        self.hud.update_money(val)

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
            conveyorSpotInfo = {'Corners': (x - 16, y - 16, x + 16, y + 16), 'Direction': direction}
            self.conveyorSpots.append(conveyorSpotInfo)
        # benutzen: conveyorSpotInfo['Direction'] == 'up'?
        conveyor_belt = ConveyorBelt(x, y, direction, delay)
        self.add(conveyor_belt)

    def create_machine(self, x, y, orientation, delay):
        if self.money >= self.machine_cost:
            self.money -= self.machine_cost
            machine = Machine(x, y, orientation, delay)
            self.machines.append(machine)
            self.add(machine)
            return True
        else:
            return False

    def create_material(self):
        if self.money >= self.material_cost:
            self.money -= self.material_cost
            startPos = self.levelInfo.start
            segments = self.levelInfo.segments
            delay = self.levelInfo.beltDelay
            x = (startPos[0] + 0.5) * 32
            y = (startPos[1] + 0.5) * 32 + random.randint(-3, 3) #so ist mehr zufall dabei
            steps = [ac.MoveBy((segment[0] * 32, segment[1] * 32), duration=(9*abs(segment[0] + segment[1]) * delay)) for segment in segments]
            actions = ac.RotateBy(0,0)
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
        for conveyorInfo in self.conveyorSpots:
            if self.coords_within(x, y, conveyorInfo['Corners']):
                if self.create_machine(x, y, conveyorInfo['Direction'], self.levelInfo.beltDelay):
                    self.conveyorSpots.remove(conveyorInfo) #no longer valid spot

    def remove(self, obj):
        if isinstance(obj, Material) and obj.processed:
            self.score += obj.score
            self.money += obj.value
        super(GameLayer, self).remove(obj)



class HUD(cocos.layer.Layer):
    def __init__(self):
        super(HUD, self).__init__()
        w, h = director.get_window_size()
        self.score_text = self._create_text(60, h-40)
        self.score_money = self._create_text(w-20, h-40)

    def _create_text(self, x, y):
        text = cocos.text.Label(font_size=18, font_name = 'Oswald', anchor_x='right', anchor_y='center')
        text.position = (x, y)
        self.add(text)
        return text

    def update_score(self, score):
        self.score_text.element.text = 'Score: %s' % score

    def update_money(self, money):
        self.score_money.element.text = 'Money: %s' % money


class DefineLevel(object):
    def __init__(self):
        self.start = (0, 5)
        self.segments = [(10, 0), (0, 8), (-3, 0), (0, -3)]
        self.layer = 'TileLayer1'
        self.beltDelay = 0.1 # groesser als 1.5 gibt probleme (ist sowieso zu langsam)



if __name__ == '__main__':

#    sys.path.append(os.path.abspath('/Users/SMSresults/Dropbox/Personal/Jungs/ScratchAndPythonHenrik/FactorySpiel'))
    pyglet.resource.path.append('img')
    pyglet.resource.reindex()
    cocos.director.director.init()

    levelInfo = DefineLevel()
    hud = HUD()

    game_layer = GameLayer(levelInfo, hud)
    background = game_layer.create_background()

    scene = cocos.scene.Scene(background, game_layer)
    director.run(scene)
