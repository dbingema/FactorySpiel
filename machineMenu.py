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
# from gameLayer import GameLayer.create_machine
from pyglet.image import load


class MachineMenu(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, conveyorInfo, levelInfo):

        super().__init__()
        self.conveyorInfo = conveyorInfo
        self.levelInfo = levelInfo

        # Positionen
        x1, y1, x2, y2 = self.conveyorInfo['Corners']
        self.center_x, self.center_y = (x1+x2)/2, (y1+y2)/2
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
                                          self.center_x+w2, self.center_y+h2)}

        numMachines = len(self.levelInfo.machines)
        menuRadius = 60

        angleIncrease = 2*math.pi/numMachines

        for index, machine in enumerate(self.levelInfo.machines):
            # liste enthaelt die images: machine = ein pfad und bild
            image = load(machine)
            # w,h, = groesse von bild = 32 breit, 96 hoch
            w2, h2 = image.width/2, image.height/2
            # bild hin malen
            # neue position
            # durch winkel und radius position rechnen
            xi = self.center_x + menuRadius * math.cos(index * angleIncrease +
                                                       0.25*math.pi)
            yi = self.center_y + menuRadius * math.sin(index * angleIncrease +
                                                       0.25*math.pi)
            # kleines bild hinzufuegen
            option_shadow = cocos.sprite.Sprite('img/machine_shadow.png', (xi, yi), scale = 0.5, opacity = 100)
            self.add(option_shadow)
            option = cocos.sprite.Sprite(image, (xi, yi), scale=0.6)
            self.add(option)
            # optin hinzufuegen zu liste mit file namen als key
            w2, h2 = option.width/2, option.height/2
            self.machineOptions[machine] = (xi-w2, yi-h2, xi+w2, yi+h2)

    def on_mouse_release(self, x, y, buttons, mod):
        # hier wird das pop up menu ausgewertet
        # schauen welches man ausgwewaehlt hat
        for option, rect in self.machineOptions.items():
            x1, y1, x2, y2 = rect
            if cocos.rect.Rect(x1, y1, x2-x1, y2-y1).contains(x, y):
                if option != "cancel":
                    self.parent.create_machine(self.center_x, self.center_y,
                                               self.conveyorInfo, option)

        self.kill()
