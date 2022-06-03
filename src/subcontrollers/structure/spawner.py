from ...defs import *
from ...utils.utils import get_creeps_of_role

from subcontrollers.creep.starter import Starter
from subcontrollers.creep.hauler import Hauler
from subcontrollers.creep.static_miner import StaticMiner
from subcontrollers.creep.builder import Builder


class Spawner:
    def __init__(self, name):
        self.name = name
        self.obj = Game.spawns[name]

    def run(self):
        if self.obj.spawning is None:
            for role in [Starter, Hauler, StaticMiner, Builder]:
                if len(get_creeps_of_role(role)) < role.SPAWN_CAP:
                    self._spawn_creep(role.DEFAULT_BODY, role)

    def _spawn_creep(self, body, role):
        result = self.obj.spawnCreep(body, self._next_name(role), {'memory': role.DEFAULT_MEMORY})

    def _next_name(self, role):
        prefix = role.__name__ + '_'
        i = 1
        while prefix + str(i) in Game.creeps:
            i += 1
        return prefix + str(i)
