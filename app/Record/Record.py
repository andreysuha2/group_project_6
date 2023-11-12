from typing import Optional
from datetime import datetime
from app.Fields import NameField, PhoneField, BirthdayField

class Record:
    def __init__(self, name: NameField, phones: list[PhoneField] = [], birthday: BirthdayField = None) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __contains__(self, item):
        if item in self.name:
            return True
        else:
            return bool(list(filter(lambda phone: item in phone, self.phones)))
        
    def __str__(self) -> str:
        return f"{self.name.value}: {'|'.join([ phone.value for phone in self.phones ])}"

    def __repr__(self) -> str:
        return str(self)

    def days_to_birthday(self) -> Optional[int]:
        if not self.birthday:
            return None
        now = datetime.now()
        def get_diff(year):
            birthday = datetime(year, self.birthday.in_datetime.month, self.birthday.in_datetime.day)
            dif = birthday - now
            return dif.days if dif.days >= 0 else get_diff(year + 1)
        return get_diff(now.year)

    def add_phone(self, phone: PhoneField) -> None:
        if phone not in self.phones:
            self.phones.append(phone)
            return True
        return False

    def remove_phone(self, searching_phone: PhoneField) -> None:
        if searching_phone in self.phones:
            self.phones.pop(self.phones.index(searching_phone))
            return f'Phone "{searching_phone}" was removed from contact "{self.name}"!'
        return f'Phone "{searching_phone}" doen\'t exist for contact {self.name}'

    def update_phone(self, searching_phone: PhoneField, phone_number: PhoneField) -> None:
        if phone_number in self.phones:
            return f'Phone {searching_phone} already exists for this record'
        if searching_phone in self.phones:
            self.phones[self.phones.index(searching_phone)] = phone_number
            return f'Phone "{searching_phone}" was changed to {phone_number} for contact "{self.name}"!'
        return f'Phone "{phone_number}" doen\'t exist for contact {self.name}'