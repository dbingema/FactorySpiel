#
# Menu fuer Optionen zum Auswaehlen welche Maschine man bauen moechte
#
# zeige alle Maschinen die man hin bauen kann (Maschinen Menu):
# wieviele Maschinen Optionen gibt es? --> Level Info
# finde Positionen fuer Maschinen Optionen (center: x,y)
# speichere Positionen fuer Optionen (und cancel) - temporaer - und Breite,
# Hoehe (als rect: x1, y1, x2, y2)
# male Maschinen Optionen auf x,y +/- Kreis um Maus Klick

import math

import cocos
from pyglet.image import load


class MachineMenu(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, pos, level_info):

        super().__init__()
        self.pos = pos
        self.level_info = level_info

        # Positionen
        self.center_x, self.center_y = self.pos
        cancel = cocos.sprite.Sprite('cancel.png',
                                     position=(self.center_x, self.center_y),
                                     opacity=200)
        self.add(cancel)

        circle = cocos.sprite.Sprite('whiteCircle.png',
                                     position=(self.center_x, self.center_y),
                                     opacity=80, scale=0.7)
        self.add(circle)

        w2, h2 = cancel.width/2, cancel.height/2
        self.machineOptions = {"cancel": (self.center_x-w2, self.center_y-h2,
                                          self.center_x+w2, self.center_y+h2, 0, None)}

        num_machines = len(self.level_info.machines)
        menu_radius = 110

        angle_increase = 2*math.pi/num_machines

        for index, machine in enumerate(self.level_info.machines):
            # liste enthaelt die images: machine = ein pfad und bild
            # auch fuer das Tool: ein bild
            imgage = machine['image']
            image = load(imgage)
            # w,h, = groesse von bild = 64 breit, 192 hoch
            w2, h2 = image.width/2, image.height/2
            # bild hin malen
            # neue position
            # durch winkel und radius position rechnen
            xi = self.center_x + menu_radius * math.cos(index * angle_increase)
            yi = self.center_y + menu_radius * math.sin(index * angle_increase)
            # kleines bild hinzufuegen
            option_shadow = cocos.sprite.Sprite('img/machine_shadow.png',
                                                (xi, yi), scale=0.5,
                                                opacity=70)
            self.add(option_shadow)
            option = cocos.sprite.Sprite(image, (xi, yi), scale=0.6)
            self.add(option)
            # optoin hinzufuegen zu liste mit file namen als key
            w2, h2 = option.width/2, option.height/2
            self.machineOptions[imgage] = (xi-w2, yi-h2, xi+w2, yi+h2, machine['cost'], machine['tool'])

    def on_mouse_release(self, x, y, buttons, mod):
        # hier wird das pop up menu ausgewertet
        # schauen welches man ausgwewaehlt hat
        for option, info in self.machineOptions.items():
            x1, y1, x2, y2, cost, tool = info
            if cocos.rect.Rect(x1, y1, x2-x1, y2-y1).contains(x, y):
                if option != "cancel":
                    self.parent.create_machine(self.center_x, self.center_y,
                                               option, cost, tool)

        self.kill()
