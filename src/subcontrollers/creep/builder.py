from ...defs import *
from ...subcontrollers.creep.creep import Creep
from ...utils import filters


class Builder(Creep):
    SPAWN_CAP = 8
    DEFAULT_BODY = [MOVE, MOVE, CARRY, CARRY, WORK, WORK]
    DEFAULT_MEMORY = {'refilling': True}

    def __init__(self, name):
        super().__init__(name)

    def run(self):
        self.decide_task()
        if self.memory.refilling:
            self.refill_energy()
        else:
            if len(self.obj.room.find(FIND_MY_CONSTRUCTION_SITES)) > 0:
                self.build()
            elif len(self.obj.room.find(FIND_STRUCTURES, filters.FILTER_DAMAGED_PASSIVE_DEFENCES)) > 0:
                self.repair_defences()
            else:
                self.repair_infrastructure()

    def decide_task(self):
        if self.empty() and not self.memory.refilling:
            self.memory.refilling = True
        elif self.full() and self.memory.refilling:
            self.memory.refilling = False

    def build(self):
        target = self.pos.findClosestByPath(FIND_MY_CONSTRUCTION_SITES)
        code = self.obj.build(target)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def repair_defences(self):
        target = _.min(self.obj.room.find(FIND_STRUCTURES, filters.FILTER_DAMAGED_PASSIVE_DEFENCES), lambda x: x.hits)
        code = self.obj.repair(target)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def repair_infrastructure(self):
        target = _.min(self.obj.room.find(FIND_STRUCTURES, filters.FILTER_DAMAGED_INFRASTRUCTURE), lambda x: x.hits)
        code = self.obj.repair(target)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def full(self):
        return self.obj.store.getFreeCapacity() == 0

    def empty(self):
        return self.obj.store.getUsedCapacity() == 0