from ...defs import *
from ...subcontrollers.creep.creep import Creep
from ...utils import filters


class Hauler(Creep):
    SPAWN_CAP = 1
    DEFAULT_BODY = [MOVE, MOVE, CARRY, CARRY, CARRY, CARRY]
    DEFAULT_MEMORY = {'refilling': True}

    def __init__(self, name):
        super().__init__(name)

    def run(self):
        self.decide_task()
        if self.memory.refilling:
            self.refill_energy()
        else:
            if len(self.obj.room.find(FIND_MY_STRUCTURES, filters.FILTER_NON_FULL_SPAWNS_AND_EXTENSIONS)) > 0:
                self.fill_spawn()
            else:
                self.fill_towers()

    def decide_task(self):
        if self.empty() and not self.memory.refilling:
            self.memory.refilling = True
        elif self.full() and self.memory.refilling:
            self.memory.refilling = False

    def fill_spawn(self):
        target = self.pos.findClosestByPath(FIND_MY_STRUCTURES, filters.FILTER_NON_FULL_SPAWNS_AND_EXTENSIONS)
        code = self.obj.transfer(target, RESOURCE_ENERGY)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def fill_towers(self):
        target = _.min(self.obj.room.find(FIND_MY_STRUCTURES, filters.FILTER_NON_FULL_TOWERS), lambda x: x.store.getUsedCapacity(RESOURCE_ENERGY))
        code = self.obj.transfer(target, RESOURCE_ENERGY)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def full(self):
        return self.obj.store.getFreeCapacity() == 0

    def empty(self):
        return self.obj.store.getUsedCapacity() == 0
