"""A D D R E S S B O O K"""

from collections import UserDict
from datetime import datetime
from .information import start_info_ab, help_info_ab
import pickle
from prompt_toolkit import prompt
from .prompt_tool import Completer, RainbowLexer
import re


filename = "addressbook.bin"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        print(record)

    def iterator(self, n=1):
        index = 1
        print_block = '-' * 100 + '\n'
        for record in self.data.values():
            print_block += str(record) + '\n'
            if index < n:
                index += 1
            else:
                yield print_block
                index, print_block = 1, '-' * 100 + '\n'
        yield print_block


class Filed:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class Name(Filed):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value.title()


class Phone(Filed):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        new_value = (
            new_value.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if not new_value.isdigit():
            print(f"!!! Entered wrong phone: {new_value}, correct phone: 0674523698")
        elif len(new_value) == 12:
            new_value = "+" + new_value
            self._value = new_value
        elif len(new_value) == 10:
            new_value = "+38" + new_value
            self._value = new_value
        else:
            print(f"!!! Entered wrong phone: {new_value}, correct phone: 0674523698")


class Birthday(Filed):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, birthday):
        try:
            new_value = datetime.strptime(birthday, "%d.%m.%Y").date()
            self._value = new_value
        except ValueError:
            print("ValueError! Enter correct date %dd.%mm.%yyyy")


class Email(Filed):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, email):
        new_email = re.search(r"[a-zA-Z0-9][\w._]+@\w+\.\w{2,}", email)
        if new_email:
            self._value = email
        else:
            print(f"!!! You entered wrong email! {new_email}")


class Address(Filed):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_address):
        self._value = new_address.title()


class Record:
    def __init__(self, name, *phones):
        self.name = name
        self.phones = list(phones)
        self.birthday = "-"
        self.email = "-"
        self.address = "-"

    def __repr__(self):
        return f"name: {self.name}, phone: {self.phones}, email: {self.email}," \
               f" address: {self.address}, birthday: {self.birthday}"

    def add_phone(self, phones):
        self.phones.append(phones)

    def change_phone(self, phone_old, phone_new):
        self.phones.remove(phone_old)
        self.phones.append(phone_new)

    def remove_contact(self, phones):
        self.phones.remove(phones)

    def add_birthday(self, birthday):
        self.birthday = birthday

    def add_email(self, email):
        self.email = email

    def add_address(self, address):
        self.address = address

    def days_to_birthday(self, birthday):
        self.birthday = birthday
        date_now = datetime.now().date()
        corr_date = birthday.replace(year=date_now.year)
        if date_now > corr_date:
            corr_date = corr_date.replace(year=date_now.year + 1)
        delta = corr_date - date_now

        return int(delta.days)


def decor_error(func):
    """Decorator for exception handling"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "IndexError... Enter name or phone please"
        except KeyError:
            return "KeyError..."
        except ValueError:
            return "ValueError..."
        except AttributeError:
            return "AttributeError..."

    return wrapper


"""The handler functions are responsible for the direct execution of commands"""


@decor_error
def hello(*args, **kwargs: AddressBook):
    return "How can I help you?\n"


@decor_error
def add_phone(*args, **kwargs: AddressBook):
    """Adding a contact and phone, if there is a contact, it adds the phone"""

    ab = kwargs.get('ab')
    name = Name(args[0])
    phone = Phone(args[1])
    rec = ab.get(name.value)
    if rec:
        rec.add_phone(phone.value)
    else:
        rec = Record(name, phone.value)
    ab.add_record(rec)
    return f"Contact {name} was created. Phone: {phone}"


@decor_error
def change(*args, **kwargs: AddressBook):
    """Change phone"""

    ab = kwargs.get('ab')
    name = Name(args[0])
    phone_old = Phone(args[1])
    phone_new = Phone(args[2])
    rec = ab.get(name.value)
    if rec:
        rec.change_phone(phone_old.value, phone_new.value)
        ab.add_record(rec)
        return f"Contact {name} was change -> old phone: {phone_old} new phone: {phone_new}"
    else:
        return f"Name {name} isn't in the AddressBook"


@decor_error
def phone(*args, **kwargs: AddressBook):
    """Contact phone output"""

    name = Name(args[0])
    ab = kwargs.get('ab')
    rec = ab.get(name.value)
    if rec:
        for value in ab.values():
            return f'{name}: phone:{value.phones}'

    return f"Name {name} isn't in the AddressBook"


@decor_error
def delete(*args, **kwargs: AddressBook):
    """Delete contact"""

    ab = kwargs.get('ab')
    name = Name(args[0])
    rec = ab.get(name.value)
    if rec:
        ab.pop(name.value)
        return f"Contact {name} deleted"
    return f"Name {name} isn't in the AddressBook"


@decor_error
def add_birthday(*args, **kwargs: AddressBook):
    """Adding date of birth"""

    ab = kwargs.get('ab')
    name = Name(args[0])
    bir_day = Birthday(args[1])
    rec = ab.get(name.value)
    if rec:
        rec.add_birthday(bir_day.value)
        ab.add_record(rec)
        return f"Contact {name} was add birthday {bir_day}"
    return f"Name {name} isn't in the AddressBook"


@decor_error
def add_email(*args, **kwargs: AddressBook):
    """Adding email"""

    ab = kwargs.get('ab')
    name = Name(args[0])
    email = Email(args[1])
    rec = ab.get(name.value)
    if rec:
        rec.add_email(email.value)
        ab.add_record(rec)
        return f"Contact {name} was add email {email}"
    return f"Name {name} isn't in the AddressBook"


@decor_error
def add_address(*args, **kwargs: AddressBook):
    """Adding address"""

    ab = kwargs.get('ab')
    name = Name(args[0])
    address_row = ", ".join(args[1:])
    address = Address(address_row)
    rec = ab.get(name.value)
    if rec:
        rec.add_address(address.value)
        ab.add_record(rec)
        return f"Contact {name} was add address {address}"
    return f"Name {name} isn't in the AddressBook"


@decor_error
def next_birthdays(*args, **kwargs: AddressBook):
    """Displays a list of contacts whose birthday is between the current date and the specified number of days"""

    ab = kwargs.get('ab')
    days = int(args[0])
    bd_list = []
    for value in ab.values():
        if value.days_to_birthday(value.birthday) <= days:
            bd_list.append(value)
    if not bd_list:
        return f"No birthdays for the next {days} days"
    for contact in bd_list:
        print(contact)
    return f"Who to congratulate on his birthday!!!"


@decor_error
def show_all(*args, **kwargs: AddressBook):
    """Displaying the contents of the contact book"""

    ab = kwargs.get('ab')
    result = f'Contacts list:\n'
    print_list = ab.iterator()
    for item in print_list:
        result += f"{item}"
    return result


@decor_error
def search(*args, **kwargs: AddressBook):
    """Search the contents of the contact book by several digits of the phone number or letters of the name, etc"""

    ab = kwargs.get('ab')
    s_search = args[0]
    contacts = []
    for contact in ab.values():
        contact = str(contact)
        if s_search.lower() in contact.lower():
            contacts.append(contact)
    if not contacts:
        return f"On request <{s_search}> don't found contacts"
    for contact in contacts:
        print(contact)
    return f"On request <{s_search}> found these contacts"


def exit_save_change(ab: AddressBook):
    """Request to save information"""

    while True:
        user_input_save = input("Save change? y/n: ")
        if user_input_save == "y":
            save_contacts_to_file(ab)
            break
        elif user_input_save == "n":
            break
        else:
            continue
    print("Good bye!")


def save_contacts_to_file(contacts):
    """Save to file"""

    with open(filename, 'wb') as file:
        pickle.dump(contacts, file)
        print("Changes saved.")


def open_contacts_from_file():
    """Loading contacts from a file"""

    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


"""Dictionary with commands (key - function: value - command)"""

COMMANDS = {
    hello: "hello",
    add_phone: "add ",
    change: "change",
    phone: "phone",
    show_all: "show",
    delete: "del",
    add_birthday: "birth",
    add_email: "email",
    add_address: "address",
    next_birthdays: "nxbirth",
    search: "sear",
    help_info_ab: "info",
}


def parser_command(user_input: str):
    """The function parses the term entered by the user, divides it into a command and other information"""

    for command, key_word in COMMANDS.items():
        if user_input.lower().startswith(key_word):
            return command, user_input.replace(key_word, "").strip().split(" ")

    return None, None


def main():
    """Main function AddressBook"""

    print(start_info_ab())
    ab = open_contacts_from_file()

    while True:
        user_input = prompt("\nEnter command>>> ", completer=Completer, lexer=RainbowLexer())
        if user_input.lower() in ["close", "exit", "."]:
            exit_save_change(ab)
            break
        command, data = parser_command(user_input)
        if not command:
            print("\nSorry, I don't understand you!")
        else:
            print(command(*data, ab=ab))


if __name__ == "__main__":
    main()
