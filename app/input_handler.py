import re
from app.comands import HANDLERS, CLOSE_COMANDS

def has_comand(entry_comand, comands_list):
        has_comand = None
        for comand in comands_list:
            entry = re.search(f"^({comand}(\s|$))", entry_comand)
            if entry:
                has_comand = comand
                break
        return has_comand

def get_comand(entry_comand):
    close_comand = has_comand(entry_comand, CLOSE_COMANDS)
    yield close_comand
    comand = has_comand(entry_comand, HANDLERS.keys())
    if comand:
         args = entry_comand[len(comand) + 1:].split(' ')
         yield (True, comand, filter(lambda i: i, args))
    else:
         yield (False, entry_comand.split(' ')[0], [])

