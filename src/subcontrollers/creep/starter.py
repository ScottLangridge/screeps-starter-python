from ...defs import *
from ...subcontrollers.creep.creep import Creep


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
            self.deposit()

    def decide_task(self):
        print(self.name)
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

    def deposit(self):
        target = self.get_target()
        code = self.obj.transfer(target, RESOURCE_ENERGY)
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
