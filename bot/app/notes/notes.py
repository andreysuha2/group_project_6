import json
from collections import UserDict
from datetime import datetime
from pathlib import Path

class Note:
        
    def __init__(self, memo):
        self.tags = self.extract_tags(memo)
        self.memo = self.remove_tags(memo, self.tags)
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def extract_tags(self, memo):
        return [tag.strip("#") for tag in memo.split() if tag.startswith("#")]

    def remove_tags(self, memo, tags):
        for tag in tags:
            memo = memo.replace(f"#{tag}", "").strip()
        return memo

    def match(self, filter):
        return filter in self.memo or filter in self.tags

    def __str__(self):
        return f'Memo: "{self.memo}", Created: {self.creation_date}, Tags: {self.tags}'
    


class Notebook(UserDict):
    def __init__(self):
        super().__init__()
        self.note_id = 1
        self.load_notes()

    def add(self, note):
        self.data[self.note_id] = note
        self.save_notes()
        self.note_id += 1

    def delete(self, note_id):
        if note_id in self.data:
            del self.data[note_id]
            self.save_notes()

    def search(self, filter):
        lower_filter = filter.lower()
        return "\n".join(
            f'ID: {note_id}, Note: {note}' 
            for note_id, note in self.data.items() 
            if self.is_match(note, lower_filter)
        )

    @staticmethod
    def is_match(note, filter):
        # Check both the memo and tags for a partial, case-insensitive match
        return filter in note.memo.lower() or any(filter in tag.lower() for tag in note.tags)

    def save_notes(self):
        # Path to the directory of the current file
        current_dir = Path(__file__).parent

        # Path to the 'noteBook.json' file in the same directory
        file_path = current_dir / 'noteBook.json'

        with open(file_path, 'w') as file:
            json.dump({'notes': {note_id: self.note_to_dict(note) for note_id, note in self.data.items()},
                    'next_id': self.note_id+1}, file, indent=4)
        
    @staticmethod
    def note_to_dict(note):
        # Метод для конвертації об'єкта Note в словник
        return {
            'memo': note.memo,
            'tags': note.tags,
            'creation_date': str(note.creation_date)
        }

    def load_notes(self):
         # Path to the directory of the current file
        current_dir = Path(__file__).parent

        # Path to the 'noteBook.json' file in the same directory
        file_path = current_dir / 'noteBook.json'
        try:
            with open(file_path, 'r') as file:
                notebook_data = json.load(file)
                self.data = {}
                for note_id, note_attrs in notebook_data['notes'].items():
                    # Створюємо об'єкт Note тільки з memo
                    note = Note(note_attrs['memo'])
                    # Встановлюємо атрибути tags та creation_date вручну
                    note.tags = note_attrs['tags']
                    note.creation_date = note_attrs['creation_date']
                    # Додаємо нотатку в словник data
                    self.data[int(note_id)] = note
                self.note_id = notebook_data['next_id']
        except FileNotFoundError:
            self.data = {}
            self.note_id = 1
            self.save_notes()  # Це створить файл noteBook.json, якщо він не існує

    def modify(self):
        try:

        
            # Спершу виведемо список нотаток
            search_query = input("Enter search query to find notes to modify: ")
            matching_notes = self.search(search_query)
            if not matching_notes.strip():
                print("No matching notes found.")
                return
            print("Matching notes:\n", matching_notes)

            while True:
                # Запитаємо ID нотатки, яку треба змінити
                note_id = int(input("Enter the ID of the note to modify: "))
                if note_id in self.data:
                    # Виведемо існуючий вміст нотатки
                    print("Current note content:")
                    print(self.data[note_id])
                    
                    # Запитаємо новий вміст нотатки
                    new_memo = input("Enter new content for the note: ")
                    # Оновимо нотатку
                    self.data[note_id].memo = self.data[note_id].remove_tags(new_memo, self.data[note_id].tags)
                    self.data[note_id].tags = self.data[note_id].extract_tags(new_memo)
                    # Збережемо зміни
                    self.save_notes()
                    #print("Note updated successfully.")
                    break
                
                else:
                    print("Note ID not found.")
                

        except ValueError:
            print("Invalid input, please enter a valid number for note ID.")

            
    def modify2(self, note_id, new_content):
        if note_id in self.data:
            # Оновлюємо вміст нотатки
            self.data[note_id].memo = self.data[note_id].remove_tags(new_content, self.data[note_id].tags)
            self.data[note_id].tags = self.data[note_id].extract_tags(new_content)
            self.data[note_id].creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Оновлення часу редагування
            # Зберігаємо зміни
            self.save_notes()

if __name__ == "__main__":
    # Приклад використання класу Notebook
    notebook = Notebook()
    note1 = Note("My first note #example1")
    notebook.add(note1)
    note2 = Note("My first 2 note #example2")
    notebook.add(note2)
    note3 = Note("My first 3 0 note #exemple3")
    notebook.add(note3)
    print(notebook.search("ex"))  # Пошук нотатки за тегом або змістом
    #notebook.modify()
    notebook.delete(1)