from ...defs import *
from ...subcontrollers.creep.creep import Creep
from ...utils import filters
from ...utils import utils


class StaticMiner(Creep):
    SPAWN_CAP = 2
    DEFAULT_BODY = [MOVE, WORK, WORK, WORK, WORK, WORK]

    def __init__(self, name):
        super().__init__(name)
        self.station = self.memory.station
        self.source = self.memory.source

    def run(self):
        if self.memory.station is None:
            self._assign_station()

        if not self.pos.isEqualTo(self.station[0], self.station[1]):
            self.obj.moveTo(self.station[0], self.station[1])

        self.harvest(self.obj.room.lookForAt(LOOK_SOURCES, self.source[0], self.source[1]))

    def _assign_station(self):
        sources = self.room.find(FIND_SOURCES)
        for source in sources:
            source_taken = False
            for creep in utils.get_creeps_of_role(StaticMiner):
                if source.pos.isEqualTo(creep.memory.source[0], creep.memory.source[1]):
                    source_taken = True

            if not source_taken:
                adjacent_containers = source.pos.findInRange(FIND_MY_STRUCTURES, 1, filters.FILTER_CONTAINERS)
                if len(adjacent_containers) > 0:
                    station = adjacent_containers[0].pos
                    self.memory.station = [station.x, station.y]
                    self.memory.source = [source.x, source.y]
                    return

        self.obj.say("NO STATION")
