#
# fliessband auf dem bildschirm
#


from actor import Actor
from pyglet.image import load, ImageGrid, Animation


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
