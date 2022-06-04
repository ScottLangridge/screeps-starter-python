from defs import *

from subcontrollers.structure.spawner import Spawner
from subcontrollers.structure.tower import Tower
from subcontrollers.creep.starter import Starter
from subcontrollers.creep.hauler import Hauler
from subcontrollers.creep.static_miner import StaticMiner
from subcontrollers.creep.builder import Builder
from subcontrollers.creep.upgrader import Upgrader

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def get_spawners():
    spawns = []
    for spawn_name in Object.keys(Game.spawns):
        spawns.append(Spawner(spawn_name))
    return spawns


def get_creeps():
    creeps = []
    for creep in Object.keys(Game.creeps):
        creeps.append(get_creep_from_name(creep))
    return creeps


# toOptimise: This runs every tick.
def get_my_towers():
    towers = []
    for s_id in Object.keys(Game.structures):
        if Game.getObjectById(s_id).structureType == STRUCTURE_TOWER:
            towers.append(Tower(s_id))
    return towers


def get_creeps_of_role(role):
    creeps = []
    for creep in Object.keys(Game.creeps):
        prefix = creep.split('_')[0]
        if prefix == role.__name__:
            creeps.append(get_creep_from_name(creep))
    return creeps


def get_creep_from_name(creep):
    prefix = creep.split('_')[0]
    if prefix == 'Starter':
        return Starter(creep)
    if prefix == 'Hauler':
        return Hauler(creep)
    if prefix == 'StaticMiner':
        return StaticMiner(creep)
    if prefix == 'Builder':
        return Builder(creep)
    if prefix == 'Upgrader':
        return Upgrader(creep)
