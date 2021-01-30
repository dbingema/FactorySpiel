#
# Das Ding an dem gearbeitet wird, erst ist es Rohstoff, dann PRodukt.
#


from pyglet.image import load

import cocos.actions as ac


import Actor






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