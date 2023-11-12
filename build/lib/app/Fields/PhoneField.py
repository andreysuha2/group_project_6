import re
from .Field import Field
from .Exceptions import PhoneValidationError

class PhoneField(Field):    
    @Field.value.setter
    def value(self, phone):
        if re.search('(\+38)?\(?0\d{2}\)?\d{7}$', phone):
            self._value = phone
        else:
            raise PhoneValidationError(f"Phone {phone} isn't valid. Please use format +380XXXXXXXXX")
        
    def __eq__(self, other) -> bool:
        return self.value == other.value
