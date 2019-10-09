#!/usr/bin/env python
from functions import *

def main():

    check_for_database()

    if len(sys.argv) > 1:

        if sys.argv[1] == "start":
            dl_start()
            
        elif sys.argv[1] == "custom":
            if len(sys.argv) > 2:
                custom_dl(sys.argv[2])
            else:
                how_to_use("Missing item")

        elif sys.argv[1] == "add":
            if len(sys.argv) > 2:
                add_check(sys.argv[2])
            else:
                how_to_use("Missing item")

        elif sys.argv[1] == "delete":
            if len(sys.argv) > 2:
                type_check(sys.argv[2])
                list_items(sys.argv[2])
                u_input = input("Please enter the ID to delete (or c to cancel): ")
                if u_input == "c":
                    print("Operation canceled.")
                else:
                    delete_item(u_input)
            else:
                how_to_use("Missing item")

        elif sys.argv[1] == "list":
            if len(sys.argv) > 2:
                type_check(sys.argv[2])
                list_items(sys.argv[2])
            else:
                how_to_use("Missing item")

        elif sys.argv[1] == "help":
            help_command()

        else:
            how_to_use("Command not found!")

    else:
        how_to_use("Missing command.")


if __name__ == '__main__':
    main()
