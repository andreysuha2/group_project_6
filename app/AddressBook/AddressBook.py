from collections.abc import Iterator
import json
import os
from pathlib import Path
from typing import Optional
from collections import UserDict
from app.Record import Record
from app.Fields import NameField, PhoneField, BirthdayField
from .AddressBookGenerator import AddressBookGenerator

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
DICTIONARY_PATH = Path(os.path.join(__location__, "data.json"))

class AddressBook(UserDict):
    def __init__(self, contacts_per_page):
        super().__init__()
        self.CONTACTS_PER_PAGE = contacts_per_page
        dictionary = {}
        try:
            with open(DICTIONARY_PATH, 'r', encoding='utf-8') as dictionary_file:
                dictionary = json.load(dictionary_file)
        except FileNotFoundError:
            print('Dictionary file not found, file will be create when you finishing your work!')
        for name, fields in dictionary.items():
            name_field = NameField(name)
            phones = [ PhoneField(phone) for phone in fields["phones"] ]
            birthday = BirthdayField(fields["birthday"]) if fields["birthday"] else None
            record = Record(name_field, phones, birthday)
            self.add_record(record)

    def search(self, search_str: str):
        return list(filter(lambda record: search_str in record, list(self.data.values())))

    def save_book(self):
        dictionary = {}
        for record in self.data.values():
            dictionary[record.name.value] = {
                "phones": [ phone.value for phone in record.phones ],
                "birthday": record.birthday.value if record.birthday else None 
            }
        with open(DICTIONARY_PATH, "w") as dictionary_file:
            json.dump(dictionary, dictionary_file) 

    def add_record(self, record: Record) -> None:
        if not record.name.value in self.data:
            self.data[record.name.value] = record

    def get_record(self, name: str) -> Optional[Record]:
        if name in self.data:
            return self.data[name]
        
    def __iter__(self) -> Iterator:
        return AddressBookGenerator(self.CONTACTS_PER_PAGE, self.data)