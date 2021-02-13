   
import cocos
from defineLevel import DefineLevel
 
 
def get_bounding_box(obj):
    # original breite hoehe fuer cocos node
    w, h = obj.width, obj.height
    return cocos.rect.Rect(obj.x - w / 2, obj.y - h / 2, w, h)


def get_tile_center(x, y):
    level_info = DefineLevel()
    cell_size = level_info.cell_size
    cell_size2 = cell_size / 2
    center_x = (x - cell_size2) // cell_size * cell_size + cell_size2
    center_y = (y - cell_size2) // cell_size * cell_size + cell_size2
    return center_x, center_y
