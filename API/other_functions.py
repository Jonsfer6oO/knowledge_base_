from . import table_models

def list_in_dict(lst: list[object], obj: object) -> dict[int, dict]:
    dct = {}
    for i in range(len(lst)):
        dct[i+1] = obj(**lst[i].__dict__).__dict__
    return dct
