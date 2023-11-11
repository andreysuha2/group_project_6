from app.AddressBook import AddressBook
from app.Fields import NameField, PhoneField, BirthdayField, Exceptions
from app.Record import Record

ADDRESS_BOOK = AddressBook(2)

def input_error(handler):
    def inner(args):
        try:
            result = handler(*args)
            return result
        except KeyError:
            return f"Contact {args[0]} doesn't exist!"
        except ValueError:
            return "You are trying to set invalid value"
        except IndexError:
            return "You are sending invalid count of parameters. Please use help comand for hint"
        except Exceptions.PhoneValidationError as err:
            return str(err)
        except Exceptions.BirthdayValidationError as err:
            return str(err)
    return inner

@input_error
def search(*args):
    search_str = args[0]
    result = ADDRESS_BOOK.search(search_str)
    output = f'Results for "{search_str}" not found'
    if len(result):
        output = f'For "{search_str}" found {len(result)} results:\n'
        for record in result:
            output += f"{record}\n"
    return output

@input_error
def add_contact(*args):
    name, fields = args[0], args[1:]
    if name in ADDRESS_BOOK:
        return f'Contact with name "{name}" already exists.'
    name_field = NameField(name)
    phones_list = []
    errors = []
    birthday = None
    for field in fields:
        try:
            phone = PhoneField(field)
            phones_list.append(phone)
        except Exceptions.PhoneValidationError as phone_error:
            try:
                birthday = BirthdayField(field)
            except Exceptions.BirthdayValidationError as birthday_error:
                errors.append(str(phone_error) + '\n')
                errors.append(str(birthday_error) + '\n')
    if not len(errors):
        record = Record(name_field, phones_list, birthday)
        ADDRESS_BOOK.add_record(record)
        return f'Contact "{name}" added to conctacts.'
    return f'Contact "{name}" can\'t be added:\n{"".join(errors)}'

@input_error
def add_phones(*args):
    name, phones = args[0], args[1:]
    record = ADDRESS_BOOK.get_record(name)
    if record and len(phones):
        added_phones = []
        missed_phones = []
        invalid_phones = []
        response = ''
        for phone in set(phones):
            try:
                result = record.add_phone(PhoneField(phone))
                added_phones.append(phone) if result else missed_phones.append(phone)
            except Exceptions.PhoneValidationError:
                invalid_phones.append(phone)
        if len(added_phones):
            response += f'Phones {", ".join(added_phones)} added to contact "{name}"\n'
        if len(missed_phones):
            response += f'Phones {", ".join(missed_phones)} already exists for contact "{name}"\n'
        if len(invalid_phones):
            response += f'Phones {", ".join(invalid_phones)} are invalid. For add phone please use format +380XXXXXXXXX'
        return response
    elif record and not len(phones):
        return "You send empty phones list"
    return f'Contact with name {name} doesn\'t exist'

@input_error
def change(*args):
    name, old_phone, new_phone = args[0], PhoneField(args[1]), PhoneField(args[2])
    record = ADDRESS_BOOK.get_record(name)
    if record:
        return record.update_phone(old_phone, new_phone)
    return f'Contact with name "{name}" doesn\'t exist.'

@input_error
def phones (*args):
    name = args[0]
    return ADDRESS_BOOK.get_record(name) or f'Contact with name "{name}" doesn\'t exist.'

@input_error
def remove_phone(*args):
    name, phone = args[0], PhoneField(args[1])
    record = ADDRESS_BOOK.get_record(name)
    if record:
        return record.remove_phone(phone)
    return f'Contact with "{name}" doesn\'t exist.'

@input_error
def remove_contact(*args):
    name = args[0]
    if name in ADDRESS_BOOK:
        ADDRESS_BOOK.pop(name)
        return f'Contact "{name}" removed from address book'
    return f'Contact "{name}" does\'t exists in address book'

@input_error
def days_to_birthday(*args):
    name = args[0]
    if name in ADDRESS_BOOK:
        days = ADDRESS_BOOK[name].days_to_birthday()
        return f'{name} birthday in {days} days' if days else f'You haven\'t record about {name} birthday'
    return f'Contact "{name}" does\'t exists in address book'

@input_error
def show_all(*args):
    print(args)
    if len(args):
        raise IndexError
    if len(ADDRESS_BOOK):
        output = "---CONTACTS--- (Tap enter for next page or print stop for exit)\n"
        for page in ADDRESS_BOOK:
            total_pages, current_page, data = page[0], page[1], page[2]
            page_output = f"Page {current_page} of {total_pages}:\n"
            for record in data:
               page_output += f"{record}\n"
            print(output)
            print(page_output)
            if current_page < total_pages:
                inpt = input("pages >>> ")
                if inpt == 'exit':
                    break
        return "Address book is closed"
    else:
        output += "Contacts are empty"
        return output
    
@input_error    
def help(*args):
    return """
        --- CONTACTS HELP ---
        syntax: add contact {name} {phone(s)}
        description: adding number to contacts list 
        example: add contact ivan +380999999999 +380777777777

        syntax: add phones {name} {phone(s)}
        description: adding number to contacts list 
        example: add phones ivan +380999999999 +380777777777

        syntax: change {name} {old_phone_number} {new_phone_number}
        description: changing phone number for contact
        example: change ivan +380777777777 +380999999999

        syntax: phones {name}
        description: finding phones numbers by contact name
        example: phones ivan

        syntax: remove contact {name}
        description: removing contact from contacts list
        example: remove ivan

        syntax: remove phone {name} {phone_number}
        description: removing contact from contacts list
        example: remove ivan +380999999999

        syntax: show all
        description: showing list of contacts
        example: show all
    """

CLOSE_COMANDS = ("good bye", "close", "exit")
HANDLERS = {
    "search": search,
    "add contact": add_contact,
    "add phones": add_phones,
    "change": change,
    "phones": phones,
    "remove phone": remove_phone,
    "remove contact": remove_contact,
    "days to birthday": days_to_birthday,
    "show all": show_all,
    "help": help
}