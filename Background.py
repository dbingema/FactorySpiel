#
# ist das hintergrund fuer das spiel
# 

import cocos




class Background(cocos.layer.Layer):

    def __init__(self, layer):
        super(Background, self).__init__()
        tmx_map = cocos.tiles.load('img/factoryMap.tmx')
        self.bg = tmx_map[layer]
        self.bg.set_view(0,0, 640, 480)

    def get_background(self):
        return self.bg