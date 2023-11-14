from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

from app.input_handler import get_comand
from app.comands import HANDLERS, ADDRESS_BOOK

def close():
    ADDRESS_BOOK.save_book()
    print("Thank you! Your dictionary is saved")

# створення списку підказок
from app.comands import CLOSE_COMANDS
variants = {}
for i in HANDLERS.keys():
    variants[i] = None
for i in CLOSE_COMANDS:
    variants[i] = None
# Створення об'єкта WordCompleter для автодоповнення
completer = NestedCompleter.from_nested_dict(variants)

GREEN = "\033[92m"     #for green greeting

def main():
    print(f'{GREEN}\r\nHello!!! \r\nYoy can use "help" comand ')
    while True:
        try:
            enter_string = (prompt (">>>", completer=completer )).strip()
            input_handler = get_comand(enter_string)
            is_close = next(input_handler)
            if is_close:
                close()
                break
            comand_exist, comand, args = next(input_handler)
            if comand_exist:
                result = HANDLERS[comand](args)
                print(f"{result}\n")
            else:
                print(f'Comand "{comand}" not found')
        except KeyboardInterrupt:
            close()
            break

if __name__ == "__main__":
    main()