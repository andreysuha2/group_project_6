import math

class AddressBookGenerator:
    def __init__(self, contacts_per_page: int, data: dict) -> None:
        self.CONTACTS_PER_PAGE = contacts_per_page
        self.next_page = 1
        self.data = data

    @property
    def total_pages(self):
        return math.ceil(len(self.data) / self.CONTACTS_PER_PAGE)

    def __next__(self):
        if self.next_page <= self.total_pages:
            start = (self.next_page - 1) * self.CONTACTS_PER_PAGE
            stop = start + self.CONTACTS_PER_PAGE
            self.next_page += 1
            return [ self.total_pages, self.next_page - 1, list(self.data.values())[start:stop] ]
        raise StopIteration