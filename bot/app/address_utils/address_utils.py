from typing import Callable

def find_index(handler: Callable, lst: list) -> int:
    index = -1
    for i, val in enumerate(lst):
        if handler(val):
            index = i
            break
    return index