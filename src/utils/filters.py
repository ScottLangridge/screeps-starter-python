import config

FILTER_DAMAGED_PASSIVE_DEFENCES = {
    'filter': lambda s: (s.structureType == STRUCTURE_WALL or s.structureType == STRUCTURE_RAMPART) and s.hits < config.DEFENCE_HITPOINTS
}

FILTER_DAMAGED_INFRASTRUCTURE = {
    'filter': lambda s: (s.structureType == STRUCTURE_ROAD or s.structureType == STRUCTURE_EXTENSION) and s.hits < s.hitsMax
}

FILTER_NON_FULL_SPAWNS_AND_EXTENSIONS = {
    'filter': lambda s: (s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION) and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0
}

FILTER_CONTAINERS = {
    'filter': lambda s: s.structureType == STRUCTURE_CONTAINER
}

FILTER_TOWERS = {
    'filter': lambda s: s.structureType == STRUCTURE_TOWER
}


def filter_container_with_resource_quantity(resource, min_quantity):
    return {
       'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(resource) >= min_quantity
    }
