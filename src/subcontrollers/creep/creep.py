from ...defs import *

from ...utils import filters

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

class Creep:
    SPAWN_CAP = 0
    DEFAULT_BODY = [MOVE, MOVE, WORK, CARRY, CARRY]
    DEFAULT_MEMORY = {}

    def __init__(self, name):
        self.obj = Game.creeps[name]
        self.memory = self.obj.memory
        self.pos = self.obj.pos
        self.store = self.obj.store

    def run(self):
        pass

    def me(self):
        return self.ojb

    def get_next_name(self):
        prefix = type(self).__name__ + '_'
        i = 1
        while i in Game.creeps:
            i += 1
        return str(prefix + str(i))

    def refill_energy(self):
        target = None

        energy_goals = [self.store.getFreeCapacity(RESOURCE_ENERGY), self.store.getFreeCapacity(RESOURCE_ENERGY) / 2, 1]
        for energy_goal in energy_goals:
            target = self._get_nearest_container_with_energy(energy_goal)
            if target != undefined:
                break

        code = self.obj.withdraw(target, RESOURCE_ENERGY)
        if code == ERR_NOT_IN_RANGE:
            self.obj.moveTo(target)

    def _get_nearest_container_with_energy(self, target_energy):
        return self.pos.findClosestByPath(
            FIND_STRUCTURES,
            filters.filter_container_with_resource_quantity(
                RESOURCE_ENERGY,
                target_energy
            )
        )
