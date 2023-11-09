class Field:
    def __init__(self, value: str) -> None:
        self._value = None
        self.value = value

    def __str__(self) -> str:
        return self.value
    
    def __contains__(self, item) -> bool:
        return item in self.value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value