import inspect

def validate_json(data: dict, cls: classmethod):
    atributos = list(inspect.signature(cls.__init__).parameters.keys())
    if 'self' in atributos:
        del atributos[0]
    return all(key in data for key in list(atributos))