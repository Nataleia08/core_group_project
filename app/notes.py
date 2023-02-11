"""N O T E B O O K"""


from collections import UserDict, UserString
from .information import start_info_nb, help_info_nb
from .prompt_tool import Completer, RainbowLexer
from prompt_toolkit import prompt
import pickle


filename = "notebook.bin"


class Tag(UserString):
    pass


class Body(UserString):
    pass


class Title(UserString):
    pass


class Note:

    def __init__(self, title: Title, tag: Tag = None, body: Body = '-'):
        if len(title) > 0 and title[0].isalnum():
            self.title = title
        self.body = body
        self.tags = []
        if tag:
            self.tags.append(tag)

    def __repr__(self):
        return f'Title: {self.title}, Tags: {self.tags}, Body: {self.body}'

    def add_tag(self, tag: Tag):
        """Added tag in note"""

        if tag not in self.tags:
            self.tags.append(tag)
            print(f'tag {tag} added in note {self.note}')
        return self.tags


class NoteBook(UserDict):

    def add_note(self, note: Note):
        """Added note in notebook"""

        if note.title not in self.data:
            self.data[note.title] = note
            return f"Note '{note.title}' was created. {note}"
        else:
            return f'{note.title} alredy exist'

    def del_note(self, note: Note):
        """Deletes note from notebook"""

        if note.title in self.data:
            self.data.pop(note.title)
            return f'Note {note.title} successfully deleted'
        else:
            return f'note {note.title} is not in NoteBook'

    def change_note(self, note_old: Note, note_new: Note):
        """Replacing on note_old with a note_new in a notebook"""

        if note_old.title in self.data:
            self.data.pop(note_old.title)
            self.data[note_new.title] = note_new
            return f"Note {note_old.title} was change -> new note: {note_new}"
        else:
            return f"Note '{note_old.title}' is not in NoteBook"

    def find(self, find_str: str):
        """Find notes that contain the specified text"""

        str_ret = '\nBy the search key ' + '"' + \
            find_str + '":' + '\n' + '_' * 40 + '\n'
        for value in self.data.values():
            if find_str.lower() in str(value).lower():
                str_ret += str(value) + '\n'
        return str_ret

    def find_sort_tags(self, tags):
        """Search and sort notes by specified tags"""

        dict_ret = {}
        for tag in tags:
            dict_ret[tag] = []
            for value in self.data.values():
                if tag.lower() in value.tags:
                    dict_ret[tag].append(value)
        return dict_ret

    def save_to_file(self, filename):
        """Save notes to the file"""

        with open(filename, "wb") as fh:
            pickle.dump(self, fh)
            print("Notes saved in file")

    def note_iterator(self, n=2):
        """Pagination (page-by-page output) for NoteBook"""

        k = 1
        block = str(k) + '-' * 40
        string_counter = 0
        for note in self.data.values():
            string_counter += 1
            block += '\n' + str(note)
            if string_counter == n:
                k += 1
                block += '\n' + str(k) + '-' * 40
                yield block
                string_counter = 0
                block = ''
        yield block


def decor_error(func):
    """Decorator for handling exceptions """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "IndexError... Enter the correct numbers of attributes, please"
        except KeyError:
            return "KeyError..."
        except ValueError:
            return "ValueError..."
        except AttributeError:
            return "AttributeError... Enter the correct attribute, please"
    return wrapper


def read_from_file(filename) -> NoteBook:
    """Uploading data from a file"""

    try:
        with open(filename, "rb") as fh:
            result = pickle.load(fh)
            print('Read NoteBook from file')
            return result
    except FileNotFoundError:
        print(f'{filename} not exist')
        return NoteBook()


@decor_error
def add_note(*args, **kwargs: NoteBook):
    """Added note in notebook"""

    nb = kwargs.get('nb')
    title = Title(args[0])
    tag = None
    body = '-'
    if len(args) > 1:
        tag = Tag(args[1])
    if len(args) > 2:
        body = ' '.join(args[2:])
    note = Note(title, tag, body)
    return nb.add_note(note)


@decor_error
def del_note(*args, **kwargs: NoteBook):
    """Deletes note from notebook"""

    nb = kwargs.get('nb')
    note = Note(args[0])
    return nb.del_note(note)


@decor_error
def change_note(*args, **kwargs: NoteBook):
    """Replacing on note_old with a note_new in a notebook"""

    nb = kwargs.get('nb')
    note_old = Note(args[0])
    note_new = Note(args[1])
    return nb.change_note(note_old, note_new)


@decor_error
def add_tag(*args, **kwargs: NoteBook):
    """Added tag in note"""

    nb = kwargs.get('nb')
    note = nb[args[0]]
    tag = args[1]
    print(f'tag {tag} added in note {note}')
    return note.add_tag(tag)


@decor_error
def find(*args, **kwargs: NoteBook):
    """Find notes that contain the specified text"""

    nb = kwargs.get('nb')
    find_str = args[0]
    return nb.find(find_str)


@decor_error
def find_sort_tags(*args, **kwargs: NoteBook):
    """Search and sort notes by specified tags"""

    nb = kwargs.get('nb')
    tags = list(args)
    return nb.find_sort_tags(tags)


@decor_error
def show_all(*args, **kwargs: NoteBook):
    """Display the contents of a NoteBook"""

    nb = kwargs.get('nb')
    result = f'Notes list:\n'
    iter = nb.note_iterator()
    for item in iter:
        result += item
    return result


def exit_save_change(nb: NoteBook):
    """Request to save information"""

    while True:
        user_input_save = input("Save change? y/n: ")
        if user_input_save == "y":
            nb.save_to_file(filename)
            break
        elif user_input_save == "n":
            break
        else:
            continue
    print("Good bye!")


"""Dictionary with commands(key - function: value - command)"""

COMMANDS = {
    add_note: "add",
    del_note: "del",
    change_note: "change",
    add_tag: "tag+",
    find: "find",
    find_sort_tags: "tags",
    show_all: "show",
    help_info_nb: "info"
}


def parser_command(user_input: str):
    """The function parses the string entered by the user, splits it into a command and other arguments"""

    for command, key_word in COMMANDS.items():
        if user_input.lower().split()[0] == key_word:
            return command, user_input.replace(key_word, "").strip().split()
    return None, None


def main():
    """Main function"""

    print(start_info_nb())
    nb = read_from_file(filename)

    while True:
        user_input = prompt("Enter command>>>", completer=Completer, lexer=RainbowLexer())
        if user_input:
            if user_input.lower() in ["close", "exit", "."]:
                exit_save_change(nb)
                break
            command, data = parser_command(user_input)
            if not command:
                print("Sorry, I don't understand you!\n")
            else:
                print(command(*data, nb=nb))
        else:
            print("Sorry, I don't understand you!\nEnter: 'info'\n")


if __name__ == "__main__":
    main()