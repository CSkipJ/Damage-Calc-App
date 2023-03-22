import random
import math
import tkinter as tk
from statfield import StatField, inputs
from functools import partial


def calculate(_field_entries_dict: dict, _fields: list):
    entity_list = []
    for idx, field_entries in enumerate(_field_entries_dict):
        new_statfield = StatField(_fields[idx])
        entity_list.append(new_statfield)
        for _stat in new_statfield.stats:
            if type(new_statfield.get_stat(_stat)) is int:
                try:
                    new_statfield.change_stat(_stat, int(_field_entries_dict[field_entries][_stat].get()))
                except ValueError:
                    new_statfield.change_stat(_stat, 0)
            elif type(new_statfield.get_stat(_stat)) is float:
                try:
                    new_statfield.change_stat(_stat, float(_field_entries_dict[field_entries][_stat].get()))
                except ValueError:
                    new_statfield.change_stat(_stat, 0.0)

    #########################################
    ########### EDIT FIELDS HERE ############
    #########################################
    # Here you can grab the fields you entered into the inputs file
    # and get each stat from them. Below are the current stats that
    # are being used in the algorithm. There are currently a bunch
    # of extras being recorded in inputs. Change the actual damage
    # algorithm in this 'calculate' function. The app is now dynamic
    # and will automagically populate the window based on the info you
    # enter into inputs.

    attacker = entity_list[fields.index('Attacker Stats')]
    defender = entity_list[fields.index('Defender Stats')]
    weapon = entity_list[fields.index('Weapon Stats')]
    spell = entity_list[fields.index('Spell Stats')]
    environment = entity_list[fields.index('Environment Stats')]

    # Variables used in calculate algorithm
    attacker_strength = attacker.get_stat('strength')
    attacker_intelligence = attacker.get_stat('intelligence')
    attacker_agility = attacker.get_stat('agility')

    defender_defense = defender.get_stat('defense')
    defender_resistance = defender.get_stat('resistance')
    defender_agility = defender.get_stat('agility')

    weapon_damage = weapon.get_stat('damage')
    weapon_crit_chance = weapon.get_stat('crit_chance')
    weapon_crit_dmg = weapon.get_stat('crit_dmg')
    weapon_max_range = weapon.get_stat('max_range')

    spell_damage = spell.get_stat('damage')
    spell_crit_chance = spell.get_stat('crit_chance')
    spell_crit_dmg = spell.get_stat('crit_dmg')

    weather_condition_bonus = environment.get_stat('weather')
    terrain_bonus = environment.get_stat('terrain')
    distance = environment.get_stat('distance')

    distance_penalty = -0.5 * math.pow((distance - weapon_max_range), 2) * (1 + random.uniform(0, 0.1))

    # Movement
    agility_bonus = attacker_agility - defender_agility
    agility_multiplier = 1 + (0.05 * agility_bonus)

    # Attacker status effects
    status_effect_damage_bonus = 0
    if "enraged" in attacker_status_effects:
        status_effect_damage_bonus += 0.2
    if "bleeding" in attacker_status_effects:
        status_effect_damage_bonus += 0.1
    if "poisoned" in attacker_status_effects:
        status_effect_damage_bonus += 0.1
    if "burned" in attacker_status_effects:
        status_effect_damage_bonus += 0.1
    if "stunned" in attacker_status_effects:
        status_effect_damage_bonus += 0.05
    if "confused" in attacker_status_effects:
        status_effect_damage_bonus += 0.05
    if "disarmed" in attacker_status_effects:
        status_effect_damage_bonus -= 0.2

    # Defender status effects
    status_effect_defense_penalty = 0
    if "shielded" in defender_status_effects:
        status_effect_defense_penalty += 0.2
    if "armored" in defender_status_effects:
        status_effect_defense_penalty += 0.1
    if "regenerating" in defender_status_effects:
        status_effect_defense_penalty -= 0.1
    if "slowed" in defender_status_effects:
        status_effect_defense_penalty -= 0.05
    if "confused" in defender_status_effects:
        status_effect_defense_penalty -= 0.05
    if "disarmed" in defender_status_effects:
        status_effect_defense_penalty += 0.2

    # Calculate base damage
    physical_base_damage = ((attacker_strength * weapon_damage) / (defender_defense + 100))
    magical_base_damage = ((attacker_intelligence * spell_damage) / (defender_resistance + 100))

    # Apply critical hit
    physical_critical_hit = False
    magical_critical_hit = False
    crit_random = random.uniform(0, 0.1)
    if weapon_crit_chance > crit_random:
        physical_base_damage *= weapon_crit_dmg
        physical_critical_hit = True
    if spell_crit_chance > random.uniform(0, 0.1):
        magical_base_damage *= spell_crit_dmg
        magical_critical_hit = True

    # Apply environmental bonuses and penalties
    physical_base_damage *= (1 + weather_condition_bonus + terrain_bonus)
    magical_base_damage *= (1 + weather_condition_bonus + terrain_bonus)

    # Apply distance penalty
    physical_base_damage *= (1 + distance_penalty)
    magical_base_damage *= (1 + distance_penalty)

    # Apply movement agility bonus
    physical_base_damage *= agility_multiplier
    magical_base_damage *= agility_multiplier

    # Apply status effects bonuses and penalties
    physical_base_damage *= (1 + status_effect_damage_bonus)
    magical_base_damage *= (1 + status_effect_damage_bonus)
    defender_defense *= (1 - status_effect_defense_penalty)
    defender_resistance *= (1 - status_effect_defense_penalty)

    # # Apply weakness and resistance effects
    # if random.random(0, 0.1) < attacker_weakness_chance:
    #     physical_base_damage *= 1.5
    #     magical_base_damage *= 1.5
    # if randomize.random() < defender_weakness_resistance:
    #     physical_base_damage *= 0.5
    #     magical_base_damage *= 0.5

    total_damage = physical_base_damage + magical_base_damage

    print(total_damage)

    # Return information about the attack
    total_damage_label.config(text=f'Total damage: {total_damage:.2f}')
    physical_base_damage_label.config(text=f'Physical damage: {physical_base_damage:.2f}')
    magical_base_damage_label.config(text=f'Magical damage: {magical_base_damage:.2f}')
    physical_critical_hit_label.config(text=f'Physical Crit: {physical_critical_hit}')
    magical_critical_hit_label.config(text=f'Magical Crit: {magical_critical_hit}')
# END calculate


root = tk.Tk()
root.title('Stats Panel')
root.config(padx=10, pady=10)

fields = list(inputs.keys())
field_entries_dict = {}
for i, field in enumerate(fields):
    field_stats = inputs[field]
    new_stats_frame = tk.LabelFrame(root, text=field.title())
    new_stats_frame.grid(row=i//5, column=i%5, padx=10, pady=20, ipadx=10, ipady=2, sticky='N')
    entries = {}
    field_entries_dict[fields[i]] = entries

    for j, stat in enumerate(field_stats):
        label = tk.Label(new_stats_frame, text=stat.title())
        label.grid(row=j, column=0)
        entry = tk.Entry(new_stats_frame, width=10)
        entry.grid(row=j, column=1)
        entry.insert(tk.END, field_stats[stat])
        entries[stat] = entry

results_frame = tk.LabelFrame(root, text='Results')
results_frame.grid(row=0, column=6, padx=10, pady=20, ipadx=10, ipady=2, rowspan=2, sticky='N')

calculate_button = tk.Button(results_frame, text="Calculate", command=partial(calculate, field_entries_dict, fields))
calculate_button.grid(row=0, column=2, sticky='S')

total_damage_label = tk.Label(results_frame, text='Total damage: 0')
total_damage_label.grid(row=1, column=0)
physical_base_damage_label = tk.Label(results_frame, text='Physical damage: 0')
physical_base_damage_label.grid(row=2, column=0)
magical_base_damage_label = tk.Label(results_frame, text='Magical damage: 0')
magical_base_damage_label.grid(row=3, column=0)
physical_critical_hit_label = tk.Label(results_frame, text='Physical Crit: ')
physical_critical_hit_label.grid(row=4, column=0)
magical_critical_hit_label = tk.Label(results_frame, text='Magical Crit: ')
magical_critical_hit_label.grid(row=5, column=0)

child = tk.Toplevel()
child.title('Status Panel')

attacker_status_effects = {
    "enraged": tk.BooleanVar(),
    "bleeding": tk.BooleanVar(),
    "poisoned": tk.BooleanVar(),
    "burned": tk.BooleanVar(),
    "stunned": tk.BooleanVar(),
    "confused": tk.BooleanVar(),
    "disarmed": tk.BooleanVar(),
}

defender_status_effects = {
    'shielded': tk.BooleanVar(),
    'armored': tk.BooleanVar(),
    'regenerating': tk.BooleanVar(),
    'slowed': tk.BooleanVar(),
    'confused': tk.BooleanVar(),
    'disarmed': tk.BooleanVar(),
}

attacker_frame = tk.LabelFrame(child, text="Attacker Status")
defender_frame = tk.LabelFrame(child, text="Defender Status")

for i, status in enumerate(attacker_status_effects.keys()):
    cb = tk.Checkbutton(attacker_frame, text=status, variable=attacker_status_effects[status])
    cb.grid(row=i, column=0, sticky="w")

for i, status in enumerate(defender_status_effects.keys()):
    cb = tk.Checkbutton(defender_frame, text=status, variable=defender_status_effects[status])
    cb.grid(row=i, column=0, sticky="w")

attacker_frame.pack(side="left", padx=10, pady=10)
defender_frame.pack(side="left", padx=10, pady=10)

root.mainloop()
