from typing import Optional
from datetime import datetime
from app.Fields import NameField, PhoneField, BirthdayField, MailField, AdressField

class Record:
    def __init__(self, name: NameField, phones: list[PhoneField] = [], birthday: BirthdayField = None, mails: list[MailField] = [], adress: AdressField = None ) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday
        self.mails = mails
        self.adress = adress

    def __contains__(self, item):
        if item in self.name:
            return True
        else:
            return bool(list(filter(lambda phone: item in phone, self.phones)))
        
    def __str__(self) -> str:

        mails = '; '.join(m.value for m in self.mails)
        return f"Contact: {self.name.value}; \
phones: {'; '.join(p.value for p in self.phones)}\
{'; Birthday '+ str(self.birthday.value) if self.birthday else ''}\
{'; To birthday: '+str(Record.days_to_birthday(self))+' days' if self.birthday else ''}\
{'; Adress: '+ str(self.adress.value) if self.adress else ''}\
{'; Mail: '+mails if len(mails)>0 else '' }"

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

    def add_mail(self, mail: MailField) -> None:
        if mail not in self.mails:
            self.mails.append(mail)
            return True
        return False

    def add_adress(self, adress: AdressField) -> None:
        if not self.adress:
            self.adress = adress
            return True
        return False

    def add_birthday(self, birthday: BirthdayField) -> None:
        if  not self.birthday:
            self.birthday = birthday
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