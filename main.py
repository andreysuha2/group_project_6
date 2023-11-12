from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

from app.input_handler import get_comand
from app.comands import HANDLERS, ADDRESS_BOOK

def close():
    ADDRESS_BOOK.save_book()
    print("Thank you! Your dictionary is saved")

# створення списку підказок
from app.comands import CLOSE_COMANDS
variants = []  
variants.extend(list(CLOSE_COMANDS))
for i in HANDLERS.keys():
    variants.append(i)
# Створення об'єкта WordCompleter для автодоповнення
completer = WordCompleter(variants)

GREEN = "\033[92m"

def main():
    print(f'{GREEN}Hello!!! \r\nYoy can use "help" comand ')
    while True:
        try:
            enter_string = (prompt (">>>", completer=completer ))
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