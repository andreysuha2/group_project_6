import re
from .Field import Field
from .Exceptions import AdressValidationError


class AdressField(Field):
    @Field.value.setter
    def value(self, adress):
        if len(adress)>2:
            self._value = adress
        if not self._value:
            raise AdressValidationError(
                f"{adress} to short")

    def __eq__(self, other) -> bool:
        return self.value == other.value
