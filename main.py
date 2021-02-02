# Haupt Programm

import pyglet.resource
from cocos.director import director
import cocos.scene

from defineLevel import DefineLevel
from hud import HUD
from gameLayer import GameLayer

if __name__ == '__main__':

	pyglet.resource.path.append('img')
	pyglet.resource.reindex()
	cocos.director.director.init(width = 1280, height = 960)

	levelInfo = DefineLevel()
	hud = HUD()

	game_layer = GameLayer(levelInfo, hud)
	background = game_layer.create_background()

	scene = cocos.scene.Scene(background, game_layer)
  
	director.run(scene)
