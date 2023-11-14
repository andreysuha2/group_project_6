from .AddressBook import AddressBook
from .Fields import NameField, PhoneField, BirthdayField, Exceptions, MailField, AdressField
from .Record import Record
from .notes import Notebook, Note
from datetime import datetime, timedelta
from .sort_file import SortFile

ADDRESS_BOOK = AddressBook(5)
NOTEBOOK = Notebook()

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
        except Exceptions.MailValidationError as err:
            return str(err)
    return inner


@input_error
# iter in book and compare with FIND_text
def search(text = ''):
    text = text.lower()
    if not len(text) > 2:
        return 'Enter more then 2 simbols to find'
    list = ''
    for cont in AddressBook(1):
        if text in str(cont[2]).lower():
            list += str(cont[2])[1:-1] + '\r\n'
    return list if len(list) > 1 else 'Cant find it'



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
def add_note(*args):
    
    note_content = ' '.join(str(arg) for arg in args)
    new_note = Note(note_content)
    NOTEBOOK.add(new_note)
    return 'Note added'

@input_error
def change(*args):
    name, old_phone, new_phone = args[0], PhoneField(args[1]), PhoneField(args[2])
    record = ADDRESS_BOOK.get_record(name)
    if record:
        return record.update_phone(old_phone, new_phone)
    return f'Contact with name "{name}" doesn\'t exist.'

@input_error
def delete_note(*args):
    note_id = int(args[0])
    if note_id in NOTEBOOK.data:
        NOTEBOOK.delete(note_id)
        return 'Note deleted'
    else:
        return 'Note not found'
    

@input_error
def show_info (*args):
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
    print(name)
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
def search_note(*args):
   
    search_query = ' '.join(str(arg) for arg in args)

    if search_query:
        
        results = NOTEBOOK.search(search_query)
        return results if results else 'No matching notes found.'
    else:
        return 'No search query provided.'

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
def birthdays_range(*args):
    current_list = []
    users_range = timedelta(days=int(args[0]))
    today_date = datetime.now().date()
    max_date = today_date + users_range
    birthdays_list = ADDRESS_BOOK.get_birthdays()
    for i in birthdays_list:
        date_formated = datetime.strptime(i.birthday.value, '%d-%m-%Y').date()
        if (date_formated.month < today_date.month) or (date_formated.month == today_date.month and date_formated.day <= today_date.day):
            date_formated = datetime.strptime(i.birthday.value, '%d-%m-%Y').date().replace(year=today_date.year + 1)
        else:
            date_formated = datetime.strptime(i.birthday.value, '%d-%m-%Y').date().replace(year=today_date.year)
        if today_date < date_formated <= max_date:
            current_list.append(i)
    if current_list:
        print(f'In the range from {today_date} to {max_date} birthdays has next user(s):')
        for user in current_list:
            print(user)
    else:
        print(f'There is no birthdays in next {args[0]} days.')

    return 'Please, enter next command.'

@input_error    
def modify_note(*args):
        
    NOTEBOOK.modify()
    
    return "Note updated successfully."

@input_error
def add_birthday(*args):
    birthday = args[1]
    name = args[0]
    obj = BirthdayField(birthday)
    if not ADDRESS_BOOK.get_record(name):
        return name + " not in book" 
    name = ADDRESS_BOOK.get_record(name)
    name.add_birthday(obj)
    ADDRESS_BOOK.add_record(name)
    return name.name.value + ' add birthday ' + birthday


@input_error
def add_mail(*args):
    mail = args[1]
    name = args[0]
    mail = mail.lower()
    obj = MailField(mail)
    if not ADDRESS_BOOK.get_record(name):
        return name + " not in book"
    name = ADDRESS_BOOK.get_record(name)
    name.add_mail(obj)
    ADDRESS_BOOK.add_record(name)
    return name.name.value + ' add mail ' + mail


@input_error
def add_adress(*args):
    adress = args[1]
    name = args[0]
    obj = AdressField(adress)
    if not ADDRESS_BOOK.get_record(name):
        return name + " not in book "
    name = ADDRESS_BOOK.get_record(name)
    name.add_adress(obj)
    ADDRESS_BOOK.add_record(name)
    return name.name.value + ' add adress  ' + adress

@input_error
def sort_file(*args):
    default_path = args[0]
    organizer = SortFile(default_path)
    organizer.create_directories(organizer.DEFAULT_PATH)
    organizer.arrange(organizer.DEFAULT_PATH)
    return f"folder {default_path} sorted."

@input_error    
def help(*args):
    return """
        --- CONTACTS HELP ---
        syntax: search {query_string}
        description: searching contact by any field
        example: search Ivan
        
        syntax: add contact {name} {phone(s)}
        description: adding number and birthday(optional) to contacts list 
        example: add contact ivan +380999999999 +380777777777 01-01-1990
        
        syntax: add address {name} {address}
        description: adding address to contact name 
        example: add address ivan Kyiv
        
        syntax: add birthday {name} {birthday}
        description: add birthday to contact name 
        example: add birthday Ivan 01-01-1970
        
        syntax: add mail {name} {email}
        description: add mail to contact name
        example: add mail Ivan ivan@mail.com

        syntax: add phones {name} {phone(s)}
        description: adding number to contacts list 
        example: add phones ivan +380999999999 +380777777777

        syntax: change phone {name} {old_phone_number} {new_phone_number}
        description: changing phone number for contact
        example: change phone ivan +380777777777 +380999999999

        syntax: info {name}
        description: finding all info by contact name
        example: info ivan

        syntax: remove contact {name}
        description: removing contact from contacts list
        example: remove ivan

        syntax: remove phone {name} {phone_number}
        description: removing contact from contacts list
        example: remove ivan +380999999999

        syntax: show all
        description: showing list of contacts
        example: show all

        syntax: birthdays range {X - number of days}
        description: show all contacts during next X days
        example: birthdays range 10
        
        syntax: days to birthday {name}
        description: show count days to name birthday
        example: days to birthday Ivan

        --- NOTES HELP ---

        syntax: add note {note} {#hashtag}
        description: This function creates a new note
        example: add note Tim birthday #holiday

        syntax: delete note {ID}
        description: This function deletes a note by it`s ID
        example: delete note 5

        syntax: searh note {text or tag}
        description: This function searches for notes by part or all word
        example: search birthday

        syntax: change note
        description: This function modifies a note by it`s ID
        example: change note
    """

CLOSE_COMANDS = ("good bye", "close", "exit")
HANDLERS = {
    "search": search,
    "add contact": add_contact,
    "add address": add_adress,
    "add phones": add_phones,
    "add birthday": add_birthday,
    "add mail": add_mail,
    "change phone": change,
    "info": show_info,
    "remove phone": remove_phone,
    "remove contact": remove_contact,
    "days to birthday": days_to_birthday,
    "show all": show_all,
    "add note": add_note,
    "delete note": delete_note,
    "find note": search_note,
    "change note": modify_note,
    "birthdays range": birthdays_range,
    "sort-file": sort_file,
    "help": help
}