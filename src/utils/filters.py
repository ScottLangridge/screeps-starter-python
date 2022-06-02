import config

FILTER_DAMAGED_PASSIVE_DEFENCES = {
    'filter': lambda s: (s.structureType == STRUCTURE_WALL or s.structureType == STRUCTURE_RAMPART) and s.hits < config.DEFENCE_HITPOINTS
}

FILTER_NON_FULL_SPAWNS_AND_EXTENSIONS = {
    'filter': lambda s: (s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION) and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0
}

FILTER_CONTAINERS = {
    'filter': lambda s: s.structureType == STRUCTURE_CONTAINER
}
