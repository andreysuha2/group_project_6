from datetime import datetime
from .Field import Field
from .Exceptions import BirthdayValidationError

class BirthdayField(Field):
    birthday_format = '%d-%m-%Y'

    @Field.value.setter
    def value(self, val):
        if val:
            try:
                now = datetime.now()
                bday = datetime.strptime(val, BirthdayField.birthday_format)
                if (now - bday).days > 0:
                    self._value = val
                else:
                    raise BirthdayValidationError
            except ValueError:
                raise BirthdayValidationError(f"{val} isn't valid birthday. Please use format dd-mm-yyyy. Also birthday can't be late then today.")
    
    @property
    def in_datetime(self):
        return datetime.strptime(self.value, BirthdayField.birthday_format)