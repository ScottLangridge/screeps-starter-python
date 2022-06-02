from ...defs import *
from ...subcontrollers.creep.creep import Creep
from ...utils import filters

class Starter(Creep):
    SPAWN_CAP = 9
    DEFAULT_BODY = [MOVE, MOVE, WORK, CARRY, CARRY]
    DEFAULT_MEMORY = {'mining': True}

    def __init__(self, name):
        super().__init__(name)

    def run(self):
        self.decide_task()
        if self.memory.mining:
            self.collect()
        else:
            if Game.spawns['Spawn1'].store.getFreeCapacity(RESOURCE_ENERGY) > 0:
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
            self.obj.say('Mining')
            self.memory.mining = True
        elif self.full() and self.memory.mining:
            self.obj.say('Depositing')
            self.memory.mining = False

    def collect(self):
        target = self.pos.findClosestByPath(FIND_SOURCES_ACTIVE)
        code = self.obj.harvest(target)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def fill_spawn(self):
        target = Game.spawns['Spawn1']
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

    def get_target(self):
        spawn = Game.spawns['Spawn1']
        controller = self.obj.room.controller
        if spawn.energy < spawn.energyCapacity:
            return spawn
        else:
            return controller

    def full(self):
        return self.obj.store.getFreeCapacity() == 0

    def empty(self):
        return self.obj.store.getUsedCapacity() == 0
