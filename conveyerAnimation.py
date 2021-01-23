from pyglet.image import  load, ImageGrid, Animation
import cocos.tiles
import cocos
import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

class Actor(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Actor, self).__init__(image)
        self.position = eu.Vector2(x, y)
        
class ConveyorBelt(Actor):
    def load_animation(self, imgage):
        seq = ImageGrid(load(imgage), 4, 1)
        return Animation.from_image_sequence(seq, 0.1)

    def __init__(self, x, y):
        animation = self.load_animation('img/conveyorBelt.png')
        super(ConveyorBelt, self).__init__(animation, x, y)

class GameLayer(cocos.layer.Layer):

    def __init__(self):
        super(GameLayer, self).__init__()
        w, h = cocos.director.director.get_window_size()
        self.width = w
        self.height = h
        for i in range(50):
            self.create_conveyor_belt(100 + i * 32, 300)

    def create_conveyor_belt(self, x, y):
        conveyor_belt = ConveyorBelt(x, y)
        self.add(conveyor_belt)

    def create_background(self):
        tmx_file = cocos.tiles.load('img/factoryMap.tmx')
        bg = tmx_file['factoryTileset']
        bg.set_view(0, 0, bg.px_width, bg.px_height)
        return bg


        
if __name__ == '__main__':
    cocos.director.director.init(caption='Belt Test', 
                                 width=800, height=650)
    game_layer = GameLayer()
    bg = game_layer.create_background()
    main_scene = cocos.scene.Scene(bg)
#    main_scene = cocos.scene.Scene(game_layer)
    cocos.director.director.run(main_scene)
    
