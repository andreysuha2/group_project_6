# GROUP_6.py BOT

To use the BOT you need to:

1. Download it [**here**](https://github.com/andreysuha2/group_project_6/releases/tag/assistant)
2. To install it, you need to run the following command in the source folder: 
        pip install assistant-1.2.2-py3-none-any.whl or py/python3 -m pip install assistant-1.2.2-py3-none-any.whl.
3. To run the bot, just type the command "assistant".
<br/>
<br/>


# --- CONTACTS HELP ---

        syntax: search {query_string}
        description: searching contact by any field
        example: search Ivan
        
        syntax: add contact {name} {phone(s)}
        description: adding number and birthday(optional) to contacts list 
        example: add contact ivan +380999999999 +380777777777 01-01-1990
        
        syntax: add address {name} {address}
        description: adding address to contact name 
        example: add address ivan Kyiv
        
        syntax: add birthday {name} {birthday}
        description: add birthday to contact name 
        example: add birthday Ivan 01-01-1970
        
        syntax: add mail {name} {email}
        description: add mail to contact name
        example: add mail Ivan ivan@mail.com

        syntax: add phones {name} {phone(s)}
        description: adding number to contacts list 
        example: add phones ivan +380999999999 +380777777777

        syntax: change phone {name} {old_phone_number} {new_phone_number}
        description: changing phone number for contact
        example: change phone ivan +380777777777 +380999999999

        syntax: info {name}
        description: finding all info by contact name
        example: info ivan

        syntax: remove contact {name}
        description: removing contact from contacts list
        example: remove ivan

        syntax: remove phone {name} {phone_number}
        description: removing contact from contacts list
        example: remove ivan +380999999999

        syntax: show all
        description: showing list of contacts
        example: show all

        syntax: birthdays range {X - number of days}
        description: show all contacts during next X days
        example: birthdays range 10
        
        syntax: days to birthday {name}
        description: show count days to name birthday
        example: days to birthday Ivan

        --- NOTES HELP ---

        syntax: add note {note} {#hashtag}
        description: This function creates a new note
        example: add note Tim birthday #holiday

        syntax: delete note {ID}
        description: This function deletes a note by it`s ID
        example: delete note 5

        syntax: searh note {text or tag}
        description: This function searches for notes by part or all word
        example: search birthday

        syntax: change note
        description: This function modifies a note by it`s ID
        example: change note