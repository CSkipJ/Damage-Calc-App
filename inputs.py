######### READ ME ##########
# Use the data structure below called 'inputs' to set the default
# stats that each class is going to instantiate. The classes will
# do this automagically. All you need to do is go into the 'calculate'
# method in main and tweak the algorithm to calculate however you
# want. If you add a new stat here, you will be able to call it
# over there.

inputs = {
    'Attacker Stats': {
        # stat name: default level
        'level': 15,
        'strength': 5,
        'intelligence': 5,
        'dexterity': 5,
        'agility': 5,
        'stamina': 5,
        'willpower': 5,
        'perception': 5,
        'focus': 5,
        'luck': 5,
        'charisma': 5,
        'wisdom': 5,
    },
    'Defender Stats': {
        'level': 1,
        'defense': 5,
        'resistance': 5,
        'agility': 5,
    },
    'Weapon Stats': {
        'damage': 1,
        'crit_dmg': float(0.2),
        'crit_chance': float(0.2),
        'max_range': 5,
    },
    'Spell Stats': {
        'damage': 1,
        'crit_dmg': float(0.2),
        'crit_chance': float(0.2),
    },
    'Environment Stats': {
        'weather': float(0.0),
        'terrain': float(0.0),
        'distance': float(1.0),
    },
}
