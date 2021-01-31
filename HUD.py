#
# Das HUD - heads up display: zeigt score an und das verdientte GEld
#


import cocos
from cocos.director import director
import cocos.sprite


class HUD(cocos.layer.Layer):
    
    def __init__(self):
        super().__init__()
        w, h = director.get_window_size()
        # create HUD background
        rectangle = cocos.sprite.Sprite('blackBar.png', position=(w/2, h-32),
                                        opacity=100)
        self.add(rectangle)
        self.score_text = self._create_text(20, h-25)
        self.money_text = self._create_text(20, h-55)

    def _create_text(self, x, y):
        text = cocos.text.Label(font_size=14, font_name='Oswald',
                                anchor_x='left', anchor_y='center')
        text.position = (x, y)
        self.add(text)
        return text

    def update_score(self, score):
        self.score_text.element.text = f'Score: {score}'

    def update_money(self, money):
        self.money_text.element.text = f'Money: {money}'
