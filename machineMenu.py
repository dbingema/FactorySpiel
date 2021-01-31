#
# Menu fuer Optionen zum Auswaehlen welche Maschine man bauen moechte
#
       # zeige alle Maschinen die man hin bauen kann (Maschinen Menu):
            # wieviele Maschinen Optionen gibt es? --> Level Info
            # finde Positionen fuer Maschinen Optionen (center: x,y)
            # speichere Positionen fuer Optionen (und cancel) - temporaer - und Breite, Hoehe (als rect: x1, y1, x2, y2)
            # male Maschinen Optionen auf x,y +/- Kreis um Maus Klick

import math

import cocos
# from gameLayer import GameLayer.create_machine
from pyglet.image import load




class MachineMenu(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, conveyorInfo, levelInfo):

        super(MachineMenu, self).__init__()
        self.conveyorInfo = conveyorInfo
        self.levelInfo = levelInfo        

        # Positionen
        x1, y1, x2, y2 = self.conveyorInfo['Corners']
        self.center_x, self.center_y = (x1+x2)/2, (y1+y2)/2
        cancelDimensions = 16
        cancel = cocos.sprite.Sprite('cancel.png', position=(self.center_x, self.center_y), opacity=200)
        self.add(cancel)

        circle = cocos.sprite.Sprite('blackCircle.png', position=(self.center_x, self.center_y), opacity=100, scale=0.7)
        self.add(circle)
            
        # fuer jede Option plus Cancel ein Ding in die Liste einbauen:
 #       self.machineOptions = {"cancel": (x-cancelDimensions, y-cancelDimensions, x+cancelDimensions, y+cancelDimensions), 
 #                              "machine1": (x+offsetRight-w2, y-h2, x+offsetRight+w2, y+h2)}
        
        self.machineOptions = {"cancel": (self.center_x-cancelDimensions, self.center_y-cancelDimensions, 
                                          self.center_x+cancelDimensions, self.center_y+cancelDimensions)}
        numMachines = len(self.levelInfo.machines)
        menuRadius = 40

        angleIncrease = 2*math.pi/numMachines

        for index, machine in enumerate(self.levelInfo.machines):
            # liste enthaelt die images: machine = ein pfad und bild
            image = load(machine)
            # w,h, = groesse von bild = 32 breit, 96 hoch
            w2, h2 = image.width/2, image.height/2
            # bild hin malen
            # neue position 
            xi = self.center_x + menuRadius * math.cos(index * angleIncrease + 0.5*math.pi)
            yi = self.center_y + menuRadius * math.sin(index * angleIncrease + 0.5*math.pi)
            self.add(cocos.sprite.Sprite(image, (xi, yi)))
            # optin hinzufuegen
            # durch winkel und radius position rechnen
            self.machineOptions[machine] = (xi-w2, yi-h2, xi+w2, yi+h2)
            
        
    def on_mouse_release(self, x, y, buttons, mod):
        # hier wird das pop up menu ausgewertet
        # schauen welches man ausgwewaehlt hat
        for option, rect in self.machineOptions.items():
            x1, y1, x2, y2 = rect
            if cocos.rect.Rect(x1, y1, x2-x1, y2-y1).contains(x, y):
                if not option == "cancel":
                    self.parent.create_machine(self.center_x, self.center_y, self.conveyorInfo, option)
        
        self.kill()


            
            


    