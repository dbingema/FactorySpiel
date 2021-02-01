#
# Das Werkzeug der MAschine, mit dem aus den Rohstoffen das Produkt gemacht wird
#


from pyglet.image import load, ImageGrid, Animation

import cocos
import cocos.euclid as eu
import cocos.actions as ac


class Tool(cocos.sprite.Sprite):

    def load_animation(self, imgage, delay):
        seq = ImageGrid(load(imgage), 1, self.num_frames)
        return Animation.from_image_sequence(seq, delay, loop=False)

    def __init__(self, x, y, orientation, target, machine, delay, image):
        # using universal delay calculate animation speed accordingly
        self.delay = delay / 2.38
        self.num_frames = 7
        self.target = target
        self.machine = machine
        animation = self.load_animation(image, self.delay)

        # depending on direction, rotate image accordingly
        if orientation == 'horizontal':
            animation = animation.get_transform(rotate=90)

        # now create actual instance
        pos = eu.Vector2(x, y)
        super().__init__(animation, pos)

        self.do(ac.CallFunc(self.target.replace) +
                ac.Delay(self.num_frames * self.delay) +
                ac.CallFunc(self.machine.begin_reload) +
                ac.CallFunc(self.kill))
