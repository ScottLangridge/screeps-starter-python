from ...defs import *


class Structure:
    def __init__(self, obj_id):
        self.obj = Game.getObjectById(obj_id)
