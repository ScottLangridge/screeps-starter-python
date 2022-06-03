from ...defs import *
from ...subcontrollers.creep.creep import Creep
from ...utils import filters


class Starter(Creep):
    SPAWN_CAP = 0
    DEFAULT_BODY = [MOVE, MOVE, WORK, CARRY, CARRY]
    DEFAULT_MEMORY = {'mining': True}

    def __init__(self, name):
        super().__init__(name)

    def run(self):
        self.decide_task()
        if self.memory.mining:
            self.collect()
        else:
            if len(self.obj.room.find(FIND_MY_STRUCTURES, filters.FILTER_NON_FULL_SPAWNS_AND_EXTENSIONS)) > 0:
                self.fill_spawn()
            elif self.obj.room.controller.level < 2 or self.obj.room.controller.ticksToDowngrade < 1000:
                self.upgrade_controller()
            elif len(self.obj.room.find(FIND_MY_CONSTRUCTION_SITES)) > 0:
                self.build()
            elif len(self.obj.room.find(FIND_STRUCTURES, filters.FILTER_DAMAGED_PASSIVE_DEFENCES)) > 0:
                self.repair_defences()
            else:
                self.upgrade_controller()

    def decide_task(self):
        if self.empty() and not self.memory.mining:
            self.memory.mining = True
        elif self.full() and self.memory.mining:
            self.memory.mining = False
            self._move_away_from_source()

    def collect(self):
        target = self.pos.findClosestByPath(FIND_SOURCES_ACTIVE)
        code = self.obj.harvest(target)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def fill_spawn(self):
        target = self.pos.findClosestByPath(FIND_MY_STRUCTURES, filters.FILTER_NON_FULL_SPAWNS_AND_EXTENSIONS)
        code = self.obj.transfer(target, RESOURCE_ENERGY)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def upgrade_controller(self):
        target = self.obj.room.controller
        code = self.obj.transfer(target, RESOURCE_ENERGY)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

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

    def full(self):
        return self.obj.store.getFreeCapacity() == 0

    def empty(self):
        return self.obj.store.getUsedCapacity() == 0

    def _move_away_from_source(self):
        target = self.pos.findClosestByPath(FIND_SOURCES_ACTIVE)
        delta_x = self.pos.x - target.pos.x
        delta_y = self.pos.y - target.pos.y
        self.obj.moveTo(self.pos.x + delta_x, self.pos.y + delta_y)
