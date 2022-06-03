from ...defs import *
from ...subcontrollers.creep.creep import Creep
from ...utils import filters
from ...utils import utils

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class StaticMiner(Creep):
    SPAWN_CAP = 2
    DEFAULT_BODY = [MOVE, WORK, WORK, WORK, WORK, WORK]

    def __init__(self, name):
        super().__init__(name)
        self.station = self.memory.station
        self.source = self.memory.source

    def run(self):
        if self.memory.station == undefined:
            self._assign_station()

        if not self.pos.isEqualTo(self.station[0], self.station[1]):
            self.obj.moveTo(self.station[0], self.station[1])

        self.obj.harvest(Game.getObjectById(self.memory.source))

    def _assign_station(self):
        sources = self.obj.room.find(FIND_SOURCES)
        for source in sources:
            source_taken = False
            for creep in utils.get_creeps_of_role(StaticMiner):
                if creep.memory.source == source.id:
                    source_taken = True

            if not source_taken:
                adjacent_containers = source.pos.findInRange(FIND_STRUCTURES, 1, filters.FILTER_CONTAINERS)
                if len(adjacent_containers) > 0:
                    station = adjacent_containers[0].pos
                    self.memory.station = [station.x, station.y]
                    self.memory.source = source.id
                    return

        self.obj.say("NO STATION")
