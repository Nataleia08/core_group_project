"""C H A T B O T"""

from .addressbook import main as ab_main
from .notes import main as nb_main
from .sort import main as sr_main


def main():
    """Main function"""

    while True:
        print(f"\n{'~' * 15}\nC H A T B O T\n{'~' * 15}")
        print(f"commands:\n{'-' * 15}\n0: Exit\n1: AddressBook\n2: Notebook\n3: Sort files\n{'-' * 15}")
        user_input = input("\nEnter command >>> ")
        if user_input == "1":
            ab_main()
        elif user_input == "2":
            nb_main()
        elif user_input == "3":
            sr_main()
        elif user_input == "0":
            print("\nGood bay!")
            break
        else:
            print(f"I don't understand you!")


if __name__ == "__main__":
    main()
