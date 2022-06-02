import config

FILTER_DAMAGED_PASSIVE_DEFENCES = {
    'filter': lambda s: (s.structureType == STRUCTURE_WALL or s.structureType == STRUCTURE_RAMPART) and s.hits < config.DEFENCE_HITPOINTS
}
