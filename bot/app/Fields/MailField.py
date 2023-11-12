import re
from .Field import Field
from .Exceptions import MailValidationError

class MailField(Field):
    @Field.value.setter
    def value(self, mail):
        iterator = re.finditer(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", mail)
        for match in iterator:
            self._value = match.group()
        if not self._value:
            raise MailValidationError(
                f"{mail} isn't valid mail")

    def __eq__(self, other) -> bool:
        return self.value == other.value

