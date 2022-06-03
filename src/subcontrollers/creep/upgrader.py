from ...defs import *
from ...subcontrollers.creep.creep import Creep
from ...utils import filters


class Upgrader(Creep):
    SPAWN_CAP = 2
    DEFAULT_BODY = [MOVE, MOVE, CARRY, CARRY, WORK, WORK]
    DEFAULT_MEMORY = {'refilling': True}

    def __init__(self, name):
        super().__init__(name)

    def run(self):
        self.decide_task()
        if self.memory.refilling:
            self.refill_energy()
        else:
            self.upgrade_controller()

    def decide_task(self):
        if self.empty() and not self.memory.refilling:
            self.memory.refilling = True
        elif self.full() and self.memory.refilling:
            self.memory.refilling = False

    def upgrade_controller(self):
        target = self.obj.room.controller
        code = self.obj.transfer(target, RESOURCE_ENERGY)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def full(self):
        return self.obj.store.getFreeCapacity() == 0

    def empty(self):
        return self.obj.store.getUsedCapacity() == 0