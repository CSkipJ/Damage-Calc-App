from inputs import inputs


class StatField:
    def __init__(self, fieldname: str, **kwargs):
        if fieldname in inputs:
            self.stats = inputs[fieldname]
            self.name = fieldname
        else:
            raise KeyError('StatField with that fieldname cannot be created, no corresponding entry in classes.inputs')
        for key, val in kwargs.items():
            if key in self.stats:
                self.stats[key] = val
            elif key not in self.stats:
                raise ValueError('Stat type does not exist in class')

    def change_stat(self, stat: str, val: int | float) -> None:
        if stat in self.stats and (type(val) is type(self.stats[stat])):
            self.stats[stat] = val
        elif type(val) is not type(self.stats[stat]):
            raise TypeError('Stat type can only take data of type int or float')
        elif stat not in self.stats:
            raise ValueError('Stat type does not exist in class')

    def get_stat(self, stat: str) -> int | float:
        if stat in self.stats:
            return self.stats[stat]
        elif stat not in self.stats:
            raise ValueError('Stat type does not exist in class')

    def __str__(self):
        retval = []
        for stat in self.stats:
            retval.append(f'{stat}: {self.stats[stat]}')
        return ', '.join(retval)
