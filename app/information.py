"""Information output functions"""


def help_info_ab(*args, **kwargs):
    """help info for AddressBook"""

    return f"I N F O:" \
           f"\n{'~' * 50}" \
           f"\ncommands:" \
           f"\n{'~' * 50}" \
           f"\n>hello<" \
           f"\n>add<: add name and phone, if there is a name add phone. example:  >command< >name< >phone<" \
           f"\n>change<: change phone. example:  >command< >name< >old_phone< >new_phone<" \
           f"\n>show<: show all AddressBook. example:  >command<" \
           f"\n>phone<: show phone. example:  >command< >name<" \
           f"\n>del<: del contact. example:  >command< >name<" \
           f"\n>birth<: add birthday. example:  >command< >name< >date<" \
           f"\n>email<: add email. example:  >command< >name< >email<" \
           f"\n>address<: add address. example:  >command< >name< >address<" \
           f"\n>search<: search by matches. example:  >command< >target<" \
           f"\n>nxbirt<: next birthday for >n< number of days. example:  >command< >name< >next number days<" \
           f"\n>info<: information. example:  >command<" \
           f"\n>., close, exit<: exit. example:  >command<" \
           f"\n{'~' * 50}" \
           f"\nContact is created with the phone!"


def help_info_nb(*args, **kwargs):
    """help info for NoteBook"""

    return f"I N F O:" \
           f"\n{'~' * 50}" \
           f"\ncommands:" \
           f"\n{'~' * 50}" \
           f"\n>add<: add new not. example:  >command< >title< >tag< >body<" \
           f"\n>del<: delete note. example:  >command< >note<" \
           f"\n>change<: change note. example:  >command< >note_old< >note_new<" \
           f"\n>show<: show all NoteBook. example:  >command<" \
           f"\n>tag+<: add tag. example:  >command< >note< >tag<" \
           f"\n>find<: find notes. example:  >command< >title< >target<" \
           f"\n>tags<: find and sort by tegs:  >command< >tags<" \
           f"\n>., close, exit<: exit:  >command<" \
           f"\n{'~' * 50}"


def start_info_ab():
    """start info for AddressBook"""

    return f"\n{'~' * 23}" \
           f"\n A D D R E S S B O O K " \
           f"\n{'~' * 23}" \
           f"\nenter: info"


def start_info_nb():
    """start info for NoteBook"""

    return f"\n{'~' * 17}" \
           f"\n N O T E B O O K " \
           f"\n{'~' * 17}" \
           f"\nenter: info"
