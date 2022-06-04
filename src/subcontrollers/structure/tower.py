from ...defs import *
from config import TOWERS_REPAIR_PASSIVE_DEFENCES

from subcontrollers.structure.structure import Structure
from utils import filters

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Tower(Structure):
    def __init__(self, obj_id):
        super().__init__(obj_id)

    def run(self):
        if self._hostiles_in_room():
            self.attack()
        elif TOWERS_REPAIR_PASSIVE_DEFENCES and len(self.obj.room.find(FIND_STRUCTURES, filters.FILTER_DAMAGED_PASSIVE_DEFENCES)) > 0:
            self.repair_defences()
        else:
            self.repair_infrastructure()

    def attack(self):
        self.obj.attack(self._get_attack_target())

    def _hostiles_in_room(self):
        return len(self.obj.room.find(FIND_HOSTILE_CREEPS)
                   + self.obj.room.find(FIND_HOSTILE_POWER_CREEPS)
                   + self.obj.room.find(FIND_HOSTILE_STRUCTURES)) > 0

    def _get_attack_target(self):
        # todo: Attack the nearest creep with healing
        target = self.obj.pos.findClosestByRange(FIND_HOSTILE_CREEPS)
        if target != undefined:
            return target

        target = self.obj.pos.findClosestByRange(FIND_HOSTILE_POWER_CREEPS)
        if target != undefined:
            return target

        target = self.obj.pos.findClosestByRange(FIND_HOSTILE_STRUCTURES)
        if target != undefined:
            return target

    def repair_defences(self):
        target = _.min(self.obj.room.find(FIND_STRUCTURES, filters.FILTER_DAMAGED_PASSIVE_DEFENCES), lambda x: x.hits)
        self.obj.repair(target)

    def repair_infrastructure(self):
        target = _.min(self.obj.room.find(FIND_STRUCTURES, filters.FILTER_DAMAGED_INFRASTRUCTURE), lambda x: x.hits)
        self.obj.repair(target)
